import socket
import pickle
import threading
import queue
import logging


# Base class. Do not use directly.
class SocketComm:
  
  header = b'\x00\xff'  # used for start of message.
  headerSize = len(header)  # saves recalculating this multiple times.
  lengthBytes = 2  # increase if trying to send too large of an object.
  
  def __init__(self, *args, **kargs):
    self.logger = logging.getLogger(__name__)  # Using logging module for synchronized printing.
    self.socket = socket.socket()
    self.queue = queue.Queue()
  
  # Abstraction. Should be called by user.
  def recv(self):
    return self.queue.get()
      
  # read thread for each client connected.
  def _threadRead(self, client, addr, readQ):
    try:
      readData = b''
      while True:
        readData += client.recv(4096)
        while readData:
          start = readData.find(self.header)
          if start == -1:  # don't have any data left.
            break
          readData = readData[start:]  # clear initial stuff as an error recovery method
          length = int.from_bytes(readData[self.headerSize:self.headerSize + self.lengthBytes], "big")
          if length + self.headerSize + self.lengthBytes < len(readData):  # don't have all data for next message
            break
          readData = readData[self.headerSize + self.lengthBytes:]  # remove header information. Simplifies next line
          serialData = readData[:length]
          data = pickle.loads(serialData)
          readQ.put((client, data))
          self.logger.info("[{}]Message Received: {}".format(addr, data))
          readData = readData[length:]  # remove data just read
    except OSError:  # socket closed. Remove client references.
      self._cleanup(client, addr)
      
  # Prepares and sends data.
  def _write(self, message, client, addr):
    try:
      serialData = pickle.dumps(message)
    except TypeError:
      print("Message could not be serialized")
      return
    client.sendall(self.header + len(serialData).to_bytes(self.lengthBytes, "big") + serialData)
    self.logger.info("[{}]Message Sent: {}".format(addr, message))
    
  # Write thread for each client connected.
  def _threadWrite(self, client, addr, writeQ):
    try:
      while True:
        data = writeQ.get()
        self._write(data, client, addr)
    except OSError:  # socket closed. Remove client references.
      self._cleanup(client, addr)
      
  # Allows for special cleanup needs.
  def _cleanup(self, client, addr):
    pass


##
#  Client object.
#
#  Useful functions:
#  -send(message)
#  -(client, message) = recv()
#  -getIP()
class SockClient(SocketComm):
  
  def __init__(self, addr="localhost", port=55000, daemon=True, *args, **kargs):
    super().__init__(*args, **kargs)
    self.socket.connect((addr, port))
    self.logger.info("Connecting to ({}:{})".format(addr, port))
    self.readThread = threading.Thread(target=self._threadRead, args=[self.socket, addr, self.queue], daemon=daemon)
    self.readThread.start()
    
  # Abstraction. Should be called by user.
  def send(self, message):
    self._write(message, self.socket, self.getIP)

  # Abstraction.
  def getIP(self):
    self.socket.gethostname()
    
  # Make sure we clean up nicely.
  def _cleanup(self, client, addr):
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    self.logger.info("Client Disconnected: {}".format(addr))


##
# Server Object.
#
# Useful functions:
# -send(message, client)
# -clients  (list object holding all connected clients)
# -(client, message) = recv()
class SockServer(SocketComm):
  
  def __init__(self, addr="localhost", port=55000, daemon=True, *args, **kargs):
    super().__init__(*args, **kargs)
    listenerSock = socket.socket()
    listenerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows for rapid reconnect.
    listenerSock.bind((addr, port))
    listenerSock.listen(0)
    self.logger.info("Listening on ({}:{}).".format(addr, port))
    self.clients = [] # list of all connected clients.
    self.clientThreads = {}  # client socket : ( read thread, write thread)
    self.clientQueues = {}  # client socket : send queue
    self.listenerThread = threading.Thread(target=self._listener, args=(listenerSock, daemon), daemon=daemon)
    self.listenerThread.start()

  # Used to send messages. clients can be found in self.clients list.
  def send(self, message, client):
    try:
      writeQ = self.clientQueues[client]
      writeQ.put(message)
    except KeyError:
      raise KeyError("Client {} not connected.".format(client))
    except Exception:
      raise Exception("Failed to send {} to client {}".format(message, client))
    
  # Listener thread. Automatically connects clients and generates threads.
  def _listener(self, listenerSock, daemon):
    try:
      while True:
        client, addr = listenerSock.accept()
        self.logger.info("Client Connected: {}".format(addr))
        self.clients.append(client)
        clientQueue = queue.Queue()
        self.clientQueues[client] = clientQueue
        clientReadThread = threading.Thread(target=self._threadRead, args=[client, addr, self.queue], daemon=daemon)
        clientWriteThread = threading.Thread(target=self._threadWrite, args=[client, addr, clientQueue], daemon=daemon)
        clientReadThread.start()
        clientWriteThread.start()
        self.clientThreads[client] = (clientReadThread, clientWriteThread)
    except OSError:
      for client in self.clients:
        try:
          client.shutdown(socket.SHUT_RDWR)
          client.close()
        except OSError:
          pass  # client already closed
      self.clients = []
      self.clientThreads = {}
      self.clientQueues = {}
      
  # Remove clients from lists when they have disconnected.
  def _cleanup(self, client, addr):
    try:
      self.clients.pop(self.clients.index(client))
      self.clientQueues.pop(client)
      self.clientThreads.pop(client)
      self.logger.info("Client Disconnected: {}".format(addr))
    except (ValueError, KeyError, NameError):
      pass  # already removed

# Used for testing.
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  serv = SockServer()
  client = SockClient()
  cmd = ""
  while cmd != "quit":
    cmd = input(">>>")
    print(eval(cmd))  # very bad idea.
