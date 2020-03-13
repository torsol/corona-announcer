import requests
import json
from datetime import date
import time
import pygame

pygame.mixer.init()
pygame.mixer.music.load("toilet.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue

number = json.loads(requests.get('https://www.vg.no/spesial/2020/corona-viruset/data/norway/').text)[
    "timeseries"]["total"]["confirmed"][str(date.today())]
while(True):
    time.sleep(5)
    new_number = json.loads(requests.get('https://www.vg.no/spesial/2020/corona-viruset/data/norway/').text)["timeseries"]["total"]["confirmed"][str(date.today())]
    if(number < new_number):
        number = new_number
        print("updated: " + str(number))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    else:
        print("not updated: " + str(number))
