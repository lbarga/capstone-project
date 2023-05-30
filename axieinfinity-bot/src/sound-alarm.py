import os

duration = 999

freq = 440

os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))