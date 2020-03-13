import requests
import json
from datetime import date
import time
import pygame

def play_sound():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def fetch_data(): return json.loads(requests.get('https://www.vg.no/spesial/2020/corona-viruset/data/norway/').text)[
        "timeseries"]["total"]["confirmed"][str(date.today())]

pygame.mixer.init()
pygame.mixer.music.load("toilet.mp3")
play_sound()

number = fetch_data()
while(True):
    time.sleep(5)
    new_number = fetch_data()
    if(number < new_number):
        number = new_number
        print("updated: " + str(number))
        play_sound()
    else:
        print("not updated: " + str(number))
