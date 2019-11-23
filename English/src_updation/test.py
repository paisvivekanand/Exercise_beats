import numpy as np
import pygame
import time, librosa
from pydub import AudioSegment

# pygame.init()
# # sound = pygame.mixer.Sound('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
# # sound.play()
# pygame.mixer.Channel.play('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
# while True:
#     time.sleep(10)
y, sr = librosa.load(librosa.util.example_audio_file())
onset_env = librosa.onset.onset_strength(y, sr=sr)
dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
print(dtempo)
print(len(dtempo))
times = librosa.frames_to_time(np.arange(len(onset_env)),
                               sr=sr, hop_length=512)
print(len(times))
print(times[9020])
print("************")
pygame.init()

trial = pygame.mixer.Sound('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
lengt_song = trial.get_length()
print(lengt_song)
pygame.quit()
print("********")
sound = AudioSegment.from_wav('/home/ubuntu/headphones/resource/Alan_Walker_Faded.wav')
print(len(sound))
print("************")
