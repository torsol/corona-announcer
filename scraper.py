import requests
import json
from datetime import date
import time
import pygame
import os 

from gtts import gTTS

def play_text(text):
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("temp.mp3")
    play_sound('temp.mp3')

def play_sound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


# API for hospital-info
def fetch_hospital_data(): return json.loads(requests.get(
    'https://redutv-api.vg.no/corona/v1/hospitalized').text)

# Get specific data from hospital-info
def get_hospitalized_data(data): return data["current"]["total"]["hospitalized"] 
def get_respiratory_data(data): return data["current"]["total"]["respiratory"]
def get_infectedEmployees_data(data): return data["current"]["total"]["infectedEmployees"]
def get_quarantineEmployees_data(data): return data["current"]["total"]["quarantineEmployees"]

# API for general norway-info
def fetch_population_data(): return json.loads(requests.get(
    'https://redutv-api.vg.no/corona/v1/sheets/norway-region-data/').text)

# Get specific data from norway-info
def get_total_contaminated(data):
    return data["metadata"]["confirmed"]["total"]

def get_total_dead(data):
    return data["metadata"]["dead"]["total"]



pygame.mixer.init()
play_text("Startup")

# Hospital data
hospital_data = fetch_hospital_data()
total_hospitalized = get_hospitalized_data(hospital_data)
total_respiratory = get_respiratory_data(hospital_data)
total_infectedEmployees = get_infectedEmployees_data(hospital_data)
total_quarantineEmployees = get_quarantineEmployees_data(hospital_data)



# Population data
population_data = fetch_population_data()
total_contaminated = get_total_contaminated(population_data)
total_dead = get_total_dead(population_data)

print('{:>15}  {:>15}  {:>15}  {:>15}'.format('Contaminated:', 'Confirmed dead:', 'Hospitalized:', 'Respiratory:'))

while(True):
    # Run checks every 5 seconds
    time.sleep(5)

    # Population data
    population_data = fetch_population_data()
    new_total_contaminated =  get_total_contaminated(population_data)
    new_total_dead = get_total_dead(population_data)

    # Hospital data
    hospital_data = fetch_hospital_data()
    new_total_hospitalized = get_hospitalized_data(hospital_data)
    new_total_respiratory = get_respiratory_data(hospital_data)
    new_total_infectedEmployees = get_infectedEmployees_data(hospital_data)
    new_total_quarantineEmployees = get_quarantineEmployees_data(hospital_data)

    # Print current values
    print('{:>15}  {:>15}  {:>15}  {:>15}'.format(new_total_contaminated, new_total_dead, new_total_hospitalized, new_total_respiratory))

    # Check for update of the totals
    if(total_contaminated < new_total_contaminated):
        total_contaminated = new_total_contaminated
        play_text("Contaminated: " + str(total_contaminated))
    if(total_dead < new_total_dead):
        total_dead = new_total_dead
        play_text("Dead: " + str(total_dead))
    if(total_hospitalized < new_total_hospitalized):
        total_hospitalized = new_total_hospitalized
        play_text("Hospitalized: " + str(total_hospitalized))
    if(total_respiratory < new_total_respiratory):
        new_total_respiratory = new_total_respiratory
        play_text("Respiratory: " + str(total_respiratory))
