import socket
import pickle
import threading
import queue
import logging


class SocketComm:
  
    header = b'\x00\xff'
    headerSize = len(header)
    lengthBytes = 2
    
    def __init__(self, *args, **kargs):
      self.logger = logging.getLogger(__name__)
      self.socket = socket.socket()
      self.queue = queue.Queue()
    
    def recv(self):
      return self.queue.get()
        
    def _threadRead(self, client, addr, readQ):
      try:
        while True:
          readData = client.recv(4096)
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
        
    def _write(self, message, client, addr):
      try:
        serialData = pickle.dumps(message)
      except TypeError:
        print("Message could not be serialized")
        return
      client.sendall(self.header + len(serialData).to_bytes(self.lengthBytes, "big") + serialData)
      self.logger.info("[{}]Message Sent: {}".format(addr, message))
      
    def _threadWrite(self, client, addr, writeQ):
      try:
        while True:
          data = writeQ.get()
          self._write(data, client, addr)
      except OSError:  # socket closed. Remove client references.
        self._cleanup(client, addr)
        
    def _cleanup(self, client, addr):
      pass


class SockClient(SocketComm):
  
  def __init__(self, addr="localhost", port=55000, daemon=True, *args, **kargs):
    super().__init__(*args, **kargs)
    self.socket.connect((addr, port))
    self.logger.info("Connecting to ({}:{})".format(addr, port))
    self.readThread = threading.Thread(target=self._threadRead, args=[self.socket, addr, self.queue], daemon=daemon)
    self.readThread.start()
    
  def send(self, message):
    self._write(message, self.socket, self.socket.getsockname()[0])
    
  def _cleanup(self, client, addr):
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    self.logger.info("Client Disconnected: {}".format(addr))

      
class SockServer(SocketComm):
  
  def __init__(self, addr="localhost", port=55000, daemon=True, *args, **kargs):
    super().__init__(*args, **kargs)
    listenerSock = socket.socket()
    listenerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenerSock.bind((addr, port))
    listenerSock.listen(0)
    self.logger.info("Listening on ({}:{}).".format(addr, port))
    self.clients = []
    self.clientThreads = {}
    self.clientQueues = {}
    self.listenerThread = threading.Thread(target=self._listener, args=(listenerSock, daemon), daemon=daemon)
    self.listenerThread.start()

  def send(self, message, client):
    try:
      writeQ = self.clientQueues[client]
      writeQ.put(message)
    except KeyError:
      raise KeyError("Client {} not connected.".format(client))
    except Exception:
      raise Exception("Failed to send {} to client {}".format(message, client))
    
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
      
  def _cleanup(self, client, addr):
    try:
      self.clients.pop(self.clients.index(client))
      self.clientQueues.pop(client)
      self.clientThreads.pop(client)
      self.logger.info("Client Disconnected: {}".format(addr))
    except (ValueError, KeyError, NameError):
      pass  # already removed

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  serv = SockServer()
  client = SockClient()
  cmd = ""
  while cmd != "quit":
    cmd = input(">>>")
    print(eval(cmd))
