from mcpi.minecraft import Minecraft


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


if __name__ == "__main__":
    # set up broadcast server
    # wait for 3 players to connect
    print("Waiting for 3 players to connect...")

    input("All players have connected. Press any key to begin.")

    # start accepting movement commands
