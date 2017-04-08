from mcpi.minecraft import Minecraft


class MinePlayer:
    def __init__(self):
        self.mc = Minecraft.create()
        self.mc.postToChat("I'm Alive!!!")

    def playerPosition(self):
        # Find block player is standing on returns (x,y,z) coordinates
        playerPos = self.mc.player.getTilePos()
        return playerPos

    def setBlock(self, x, y, z, block):
        # Set position and block
        self.mc.player.setPos(x, y, z)
        self.mc.setBlock(x + 1, y, z, block)


def incrementToken():
    pass


if __name__ == "__main__":
    # set up broadcast server
    # wait for 3 players to connect
    print("Waiting for 3 players to connect...")

    input("All players have connected. Press any key to begin.")

    # start accepting movement commands