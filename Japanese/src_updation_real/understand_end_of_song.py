import numpy as np
import pygame
import time, librosa

pygame.init()
# pygame.mixer.music.load('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
# pygame.mixer.music.set_volume(0)
# pygame.mixer.music.play()
sound = pygame.mixer.Sound('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
sound.play()
while True:
    time.sleep(1)
    print(pygame.mixer.get_busy())
    if pygame.mixer.get_busy():
        pass
    else:
        sound = pygame.mixer.Sound('/home/ubuntu/headphones/resource/David_Guetta_Play_Hard.wav')
        sound.play()