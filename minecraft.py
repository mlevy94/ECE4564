import mcpi.minecraft as minecraft
import mcpi.block as block
import time 

mc =  minecraft.Minecraft.create()

mc.postToChat("Hola Bitches")

def playerPosition():
	#Find block player is standing on returns (x,y,z) coordinates
	playerPos = mc.player.getTilePos()
	return playerPos


def setBlock(x, y, z, block):
	#Set position and block
	mc.player.setPos(x, y, z)
	mc.setBlock(x + 1, y, z, block)
