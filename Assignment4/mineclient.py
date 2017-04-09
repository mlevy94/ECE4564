import argparse
from time import sleep
import asyncio
from aiocoap import Context, Message, PUT, GET
import pickle

blocks = [5, 57, 1]

async def runGame(client):
  # join game and get token
  myToken = client.joinGame()
  # wait for 3 players to join
  while client.getPlayers() < 3:
    sleep(1)
  # determine starting block placement
  top = myToken % 2 == 0
  while True:
    # check to see if it's my turn
    token, x, y, z = client.getGameState()
    if token == 0:
      break  # end game
    elif token == myToken:
      if top:  # place a block on the top of this column or bottom of next column
        client.placeBlock(myToken, x, y + 1, z, blocks[myToken])
      else:
        client.placeBlock(myToken, x + 1, y, z, blocks[myToken])
    sleep(1)

class Client:
  
  def __init__(self, addr):
    self.addr = addr
    
  async def joinGame(self):
    return pickle.loads(await self.mine_get(b'Assign'))[0]
    
  async def getGameState(self):
    return pickle.loads(await self.mine_get())
  
  async def placeBlock(self, token, x, y, z, block):
    await self.mine_put((token, x, y, z, block))
    
  async def getPlayers(self):
    return pickle.loads(await self.mine_get(b'Players'))[0]

  async def mine_get(self, payload=b''):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://{}/Main/Minecraft'.format(self.addr), payload=payload)
  
    try:
      response = await protocol.request(request).response
    except Exception as e:
      print('Failed to fetch resource:')
      print(e)
    else:
      return request.payload
  
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
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runGame(client))
    loop.close()


