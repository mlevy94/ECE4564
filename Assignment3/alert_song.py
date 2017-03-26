import pygame


def play(songname):
    pygame.mixer.init()
    pygame.mixer.music.load(songname)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

if __name__ == "__main__":
    play("trap.wav")
