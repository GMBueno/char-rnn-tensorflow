import numpy as np
import time
import threading
import sys

import mido
from pprint import pprint as pp

time_elapsed = 0
tps = 50_000.0

class Decoder():
    def __init__(self, mid):
        # port to play music so we can hear results
        self.mid = mid
        self.port = mido.open_output()  # system default (IAC Driver (must be on) on Mac)
        self.track = self.create_midi()

    def create_midi(self):
        track = []
        with open(self.mid, "r") as file:
            for line in file:
                words = line.split()
                # print(words)
                time = int(words[0])
                note = int(words[1])
                if note > 127:
                    note = 127
                vel = int(words[2])
                if vel > 127:
                    vel = 127
                msg = mido.Message('note_on', time=time/tps, note=note, velocity=vel)
                track.append(msg)
        return track

    def play(self):
        for msg in self.track:
            time.sleep(msg.time)
            # print(f'{msg} time={128*msg.time}')
            self.port.send(msg)

    def print_duration(self):
        duration = 0
        for msg in self.track:
            duration += msg.time
        print(f"music lenght:\t{int(duration)}s")


def print_elapsed_time():
  threading.Timer(1.0, print_elapsed_time).start()
  global time_elapsed
  ''' overwrites previous line
  Prefix your output with carriage return symbol '\r' and do not end it
  with line feed symbol '\n'. This will place cursor at the beginning of the
  current line, so output will overwrite previous its content.
  Pad it with some trailing blank space to guarantee overwrite
  '''
  sys.stdout.write('\r' + f"time elapsed:\t{time_elapsed}s" + ' ' * 20)
  sys.stdout.flush() # important
  time_elapsed += 1



file = input("Do you want to play file 1, 2 or 3?\t")
dec = Decoder(f"results/2018_20_56k_trained/{file}.txt")
dec.print_duration()
print_elapsed_time()
dec.play()
