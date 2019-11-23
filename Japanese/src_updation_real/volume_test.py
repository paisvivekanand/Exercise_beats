import numpy as np
import pygame
import time, librosa
from pydub import AudioSegment
import time

pygame.init()

trial = pygame.mixer.Sound('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
print(trial.get_volume())
sound = pygame.mixer.Sound('/home/ubuntu/headphones/resource/David_Guetta_Play_Hard.wav')
print(sound.get_volume())
trial.play()
sound.set_volume(0)
sound.play()
for i in range(0,4):
    time.sleep(4)
    vol1 =trial.get_volume()
    vol2 = sound.get_volume()
    print("vol1:",vol1," vol2: ", vol2)
    trial.set_volume(vol1 - 0.2)
    sound.set_volume(vol2+.1)
trial.set_volume(0)
time.sleep(5)
sound.set_volume(1)
time.sleep(5)