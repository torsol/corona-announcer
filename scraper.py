
# Std libs
import time
import os
from io import BytesIO

from datetime import date

# 3rd party libs
import pygame
from gtts import gTTS

# Custom Libraries
from data_source import DataSource


def play_text(text, language="en"):
    speech = gTTS(text=text, lang=language, slow=False)
    buf = BytesIO()
    speech.write_to_fp(buf)
    buf.seek(0)
    play_sound(buf)


def play_sound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue


def get_timestamp():
    return time.strftime("%H:%M:%S", time.localtime())


log_info = True
is_raspi = False
play_first = True

# Run soundcheck
pygame.mixer.init()
play_text("Startup")

if is_raspi: time.sleep(20)

source = DataSource("config.json")

while True:

    source.refresh_data()

    if log_info:
        print(f"---{get_timestamp()}---")

    for value, last_value, announce in source:

        if log_info:
            print(f"{announce}{value}")
        
        if value != last_value:

            if last_value == None and play_first:
                play_text(f"{announce} initialized to {value}")
                continue
                
            denominator = "increased" if value > last_value else "decreased"
            delta = abs(value - last_value)
            play_text(f"{announce} {denominator} by {delta}")

    time.sleep(5)
