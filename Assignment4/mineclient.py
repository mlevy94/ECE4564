import argparse
from time import sleep

blocks = [5, 57, 1]

def getGameState():
  return 0, 0, 0, 0

def placeBlock(token, x, y, z, block):
  pass


def runGame(myToken):
  top = myToken % 2 == 0
  while True:
    token, x, y, z = getGameState()
    if token == 0:
      break
    elif token == myToken:
      if top:
        placeBlock(myToken, x, y + 1, z, blocks[myToken])
      else:
        placeBlock(myToken, x + 1, y, z, blocks[myToken])
    sleep(1)



if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("server", nargs='?', default="localhost")
    fields = parser.parse_args()
    
    # get initial token
    myToken = 1
    runGame(myToken)

