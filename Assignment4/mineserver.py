from mcpi.minecraft import Minecraft
import RPi.GPIO as GPIO
import pickle
import asyncio
import aiocoap.resource as resource
import aiocoap


class MinePlayer:

  def __init__(self):
    self.mc = Minecraft.create()
    self.mc.postToChat("I'm Alive!!!")
  
  def playerPosition(self):
    # Find block player is standing on returns (x,y,z) coordinates
    playerPos = self.mc.player.getTilePos()
    return playerPos.x, playerPos.y, playerPos.z
  
  def setBlock(self, x, y, z, block):
    # Set position and block
    self.mc.player.setPos(x, y, z)
    self.mc.setBlock(x + 1, y, z, block)



class Game:
  
  endGame = 40
  
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    self.game = MinePlayer()
    self.initX, self.initY, self.initZ = self.game.playerPosition()
    
  def putBlock(self, x, y, z, block):
    self.game.setBlock(x, y, z, block)
    self.tokenizer.incrementturn()
    if self.tokenizer.getturn() >= self.endGame:
      self.tokenizer.turn = -1
      self.tokenizer.numplayers = 0
      
  def getState(self):
    x, y, z = self.game.playerPosition()
    return x, y, z, self.tokenizer.gettoken()
    
  def addPlayer(self):
    return self.tokenizer.addplayer()

class MinecraftResource(resource.Resource):
  def __init__(self, game, *args, **kargs):
    super().__init__(*args, **kargs)
    self.game = game

  async def render_get(self, request):
    await asyncio.sleep(3)
    if request.payload == b'Assign':
      playerToken = (self.game.addPlayer(),)
      return aiocoap.Message(payload=pickle.dumps(playerToken))
    else:
      gameState = self.game.getState()
      return aiocoap.Message(payload=pickle.dumps(gameState))

  async def render_put(self, request):
    blockPlace = pickle.loads(request.payload)
    self.game.putBlock(*blockPlace)
    return aiocoap.Message()

class playerLed:

  def gettoken(self):
    if self.turn == -1:
      return -1
    else:
      return (self.turn % self.numplayers) + 1

  def incrementturn(self):
    self.turn += 1
    self.color()

  def getturn(self):
    return self.turn

  def addplayer(self):
    self.numplayers += 1
    return self.numplayers

  def getplayer(self):
    return self.numplayers

  def __del__(self):
    GPIO.cleanup()

  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    self.turn = 0
    self.numplayers = 0

  def color(self):
    try:
      col = self.gettoken()
    except ZeroDivisionError:
      col = 0
  
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
    # set up broadcast server
    # wait for 3 players to connect
    print("Waiting for 3 players to connect...")
    tokenizer = playerLed()
    game = Game(tokenizer)
    root = resource.Site()
    root.add_resource(('Main', 'Minecraft'), MinecraftResource(game))

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()
