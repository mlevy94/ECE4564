from mcpi.minecraft import Minecraft
import RPi.GPIO as GPIO
import pickle
import asyncio
import aiocoap.resource as resource
import aiocoap


class MinePlayer:

  def __init__(self):
    #Connect to minecraft server
    self.mc = Minecraft.create()
    self.mc.postToChat("I'm Alive!!!")
    
    #Render flat world on position player on top and center
    self.mc.setBlocks(-258, 0, -256, 256, 64, 256, 0)
    bid = 2
    self.mc.setBlocks(-256, 0, -256, 256, -64, 256, bid)
    self.mc.player.setTilePos(0, 1, 0)
    self.mc.postToChat("BRING ME PLAYERS!!!")
  
  #Reset player position to cooridinates recieved by autmation
  def playerPosition(self):
    # Find block player is standing on returns (x,y,z) coordinates
    playerPos = self.mc.player.getTilePos()
    return playerPos.x, playerPos.y, playerPos.z
  
  #Function used to build the wall at coordinates recieved from automation
  def setBlock(self, x, y, z, block):
    # Set position and block
    self.mc.player.setTilePos(x, 1, z)
    self.mc.setBlock(x, y, z + 2, block)



class Game:
  
  endGame = 20  # turns game lasts
  
  # initialize everything
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    self.game = MinePlayer()
    self.initX, self.initY, self.initZ = self.game.playerPosition()
    
  # put block and increment player token
  def putBlock(self, token, x, y, z, block):
    # make sure the correct player is moving
    if token != self.tokenizer.gettoken():
      print("Wrong token trying to move! Expected: {} Received: {}".format(self.tokenizer.gettoken(), token))
      return
    self.game.setBlock(x, y, z, block)
    self.tokenizer.incrementturn()
    # end game
    if self.tokenizer.getturn() >= self.endGame:
      self.tokenizer.turn = -1
      self.tokenizer.color()
      self.tokenizer.numplayers = 0
      
  # get the state of the game including coordinates and player turn
  def getState(self):
    x, y, z = self.game.playerPosition()
    self.tokenizer.color()
    return x, y, z, self.tokenizer.gettoken()
    
  # add a player to the game
  def addPlayer(self):
    ret =  self.tokenizer.addplayer()
    print("Player {} Connected.".format(self.tokenizer.getplayers()))
    return ret
  
  # get the number of players in the game
  def getPlayers(self):
    return self.tokenizer.getplayers()
#setting up the resources to aces with and get and put
class MinecraftResource(resource.Resource):
  def __init__(self, game, *args, **kargs):
    super().__init__(*args, **kargs)
    self.game = game
  #the GET resurces available. depending on payload passed get different values
  async def render_get(self, request):
    if request.payload == b'Assign':
      playerToken = (self.game.addPlayer(),)
      return aiocoap.Message(payload=pickle.dumps(playerToken))
    elif request.payload == b'Players':
      players = (self.game.getPlayers(),)
      return aiocoap.Message(payload=pickle.dumps(players))
    else:
      gameState = self.game.getState()
      return aiocoap.Message(payload=pickle.dumps(gameState))
  #the Put resource. only used for block placement.
  async def render_put(self, request):
    blockPlace = pickle.loads(request.payload)
    self.game.putBlock(*blockPlace)
    return aiocoap.Message()

class playerLed:

#returns the value of the current token
  def gettoken(self):
    try:
      return (self.turn % self.numplayers) + 1
    except ZeroDivisionError:
      return -1

#increments the turn count by one and updates LED color
  def incrementturn(self):
    self.turn += 1
    self.color()

#returns the current turn number
  def getturn(self):
    return self.turn

#adds one player and returns the number of players
  def addplayer(self):
    self.numplayers += 1
    return self.numplayers

#returns the number of players
  def getplayers(self):
    return self.numplayers

#turns off LEDs once program terminates
  def __del__(self):
    GPIO.cleanup()

#initilaizes class member variables and prepares GPIO pins for output
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    self.turn = 0
    self.numplayers = 0

#updates LED color based on token
  def color(self):
    col = self.gettoken()
  
    if col == -1:
      GPIO.output(4, GPIO.HIGH)
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(27, GPIO.HIGH)
  
    elif col == 1:
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.LOW)
      GPIO.output(4, GPIO.HIGH)
  
    elif col == 2:
      GPIO.output(4, GPIO.LOW)
      GPIO.output(27, GPIO.LOW)
      GPIO.output(17, GPIO.HIGH)
  
    elif col == 3:
      GPIO.output(4, GPIO.LOW)
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.HIGH)
  
    else:
      GPIO.output(4, GPIO.LOW)
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.LOW)

if __name__ == "__main__":
    tokenizer = playerLed()
    game = Game(tokenizer)
    
    root = resource.Site()
    root.add_resource(('Main', 'Minecraft'), MinecraftResource(game))
    asyncio.Task(aiocoap.Context.create_server_context(root))
    print("Waiting for 3 players to connect...")
    asyncio.get_event_loop().run_forever()
