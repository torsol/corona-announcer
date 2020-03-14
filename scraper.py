import requests
import json
import time
import pygame
from datetime import datetime

def play_sound(case_type):
    load_sound(case_type)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def load_sound(case_type):
    sounds = {
        'confirmed': 'toilet.mp3',
        'dead': 'lacrimosa.mp3',
    }
    pygame.mixer.music.load(sounds[case_type])

def fetch_data():
    endpoint_url = 'https://www.vg.no/spesial/2020/corona-viruset/data/norway/'
    body = requests.get(endpoint_url).text
    root = json.loads(body)
    totals = root["totals"]
    confirmed = totals["confirmed"]
    dead = totals["dead"]
    return (confirmed, dead)

pygame.mixer.init()
play_sound('confirmed')

print()

ran_once = False
confirmed, dead = fetch_data()

while True:
    time.sleep(5)
    new_confirmed, new_dead = fetch_data()

    if [confirmed, dead] == [new_confirmed, new_dead] and ran_once:
        continue

    print(datetime.now())
    print(f"Total confirmed cases: {new_confirmed}")
    print(f"Total death toll: {new_dead}")

    if confirmed < new_confirmed:
        print(f"New confirmed cases: {new_confirmed - confirmed}")
        confirmed = new_confirmed
        play_sound('confirmed')

    if dead < new_dead:
        print(f"New mortalities: {new_dead - dead}")
        dead = new_dead
        play_sound('dead')

    print()

    ran_once = True

