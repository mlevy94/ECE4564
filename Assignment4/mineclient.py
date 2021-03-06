import argparse
from time import sleep
import asyncio
from aiocoap import Context, Message, PUT, GET
import pickle

blocks = [5, 57, 1]  # wood, diamond, stone

# main game loop. Each client does its own thing
async def runGame(client):
  # join game and get token
  myToken = await client.joinGame()
  print("Connected. Token Recieved: {}".format(myToken))
  # wait for 3 players to join
  while await client.getPlayers() < 3:
    print("Waiting for 3 players to connect...")
    sleep(1)
  # determine starting block placement
  top = myToken % 2 == 0
  while True:
    # check to see if it's my turn
    x, y, z, token = await client.getGameState()
    if token == -1:
      print("Game Over!")
      break  # end game
    elif token == myToken:
      print("My Turn to move.")
      if top:  # place a block on the top of this column
        await client.placeBlock(myToken, x, y + 1, z, blocks[myToken - 1])
      else:    # place a block on the bottom of the next column
        await client.placeBlock(myToken, x + 1, y, z, blocks[myToken - 1])
      top = not top  # alternate block placement
    else:
      print("Not my turn to move.")
    sleep(1)
#The client used to connect to the server for the GET and Put protocols
class Client:
  
  def __init__(self, addr):
    self.addr = addr
  #get token of player that has joined
  async def joinGame(self):
    return pickle.loads(await self.mine_get(b'Assign'))[0]
    #get the current turn
  async def getGameState(self):
    return pickle.loads(await self.mine_get())
  #place a block using PUT
  async def placeBlock(self, token, x, y, z, block):
    await self.mine_put((token, x, y, z, block))
    #get which player is active
  async def getPlayers(self):
    return pickle.loads(await self.mine_get(b'Players'))[0]
  #the GET protocol using asyncio and coap.
  async def mine_get(self, payload=b''):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://{}/Main/Minecraft'.format(self.addr), payload=payload)
    #in the event that the call fails
    try:
      response = await protocol.request(request).response
    except Exception as e:
      print('Failed to fetch resource:')
      print(e)
    else:
      return response.payload
  #the PUT protocol using coap.
  async def mine_put(self, payload):
    context = await Context.create_client_context()
    
    await asyncio.sleep(2)
    #requesting the put query
    request = Message(code=PUT, payload=pickle.dumps(payload))
    request.opt.uri_host = self.addr
    request.opt.uri_path = ("Main", "Minecraft")
    
    response = await context.request(request).response

if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("server", nargs='?', default="localhost")
    fields = parser.parse_args()
    
    client = Client(fields.server)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runGame(client))
    loop.close()


