import argparse
from time import sleep
import asyncio
from aiocoap import Context, Message, PUT, GET
import pickle

blocks = [5, 57, 1]

async def runGame(client):
  myToken = client.joinGame()
  top = myToken % 2 == 0
  while True:
    token, x, y, z = client.getGameState()
    if token == 0:
      break
    elif token == myToken:
      if top:
        client.placeBlock(myToken, x, y + 1, z, blocks[myToken])
      else:
        client.placeBlock(myToken, x + 1, y, z, blocks[myToken])
    sleep(1)

class Client:
  
  def __init__(self, addr):
    self.addr = addr
    self.payload = None
    
  async def joinGame(self):
    await self.mine_get(b'Assign')
    return pickle.loads(self.payload)[0]
    
  async def getGameState(self):
    await self.mine_get()
    return pickle.loads(self.payload)
  
  async def placeBlock(self, token, x, y, z, block):
    await self.mine_put((token, x, y, z, block))
    

  async def mine_get(self, payload=b''):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://{}/Main/Minecraft'.format(self.addr), payload=payload)
  
    try:
      response = await protocol.request(request).response
    except Exception as e:
      print('Failed to fetch resource:')
      print(e)
    else:
      self.payload = request.payload
  
  
  async def mine_put(self, payload):
    context = await Context.create_client_context()
    
    await asyncio.sleep(2)
    
    request = Message(code=PUT, payload=pickle.dumps(payload))
    request.opt.uri_host = self.addr
    request.opt.uri_path = ("Main", "Minecraft")
    
    response = await context.request(request).response
    
    print('Result: {0}\n{1}'.format(response.code, response.payload))

if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("server", nargs='?', default="localhost")
    fields = parser.parse_args()
    
    client = Client(fields.server)
    
    asyncio.get_event_loop().run_until_complete(runGame(client))


