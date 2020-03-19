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
def get_total_contaminated(data): return data["metadata"]["confirmed"]["total"]
def get_total_dead(data): return data["metadata"]["dead"]["total"]


log_info = True

sources = {
    "hospital_data": {
        'getter':fetch_hospital_data,
        'data': "None"
    },
    "population_data": {
        'getter':fetch_population_data,
        'data': "None"
    },
}


# Run soundcheck
pygame.mixer.init()
play_text("Startup")

# Get data
for source in sources:
    sources[source]['data']=sources[source]['getter']()

statistics = {
    "contaminated": {
        "total": 0,
        "data_source": 'population_data',
        "getter": get_total_contaminated,
        "announce": 'Contaminated: '
    },
    "dead": {
        "total": 0,
        "data_source": 'population_data',
        "getter": get_total_dead,
        "announce": 'Total dead: '
    },
    "hospitalized": {
        "total": 0,
        "data_source": 'hospital_data',
        "getter": get_hospitalized_data,
        "announce": 'Hospitalized: '
    },
    "respiratory": {
        "total": 0,
        "data_source": 'hospital_data',
        "getter": get_respiratory_data,
        "announce": 'People in respiration: '
    },
    "infected_employees": {
        "total": 0,
        "data_source": 'hospital_data',
        "getter": get_infectedEmployees_data,
        "announce": 'Infected hospital employees: '
    },
    "quarantine_employees": {
        "total": 0,
        "data_source": 'hospital_data',
        "getter": get_quarantineEmployees_data,
        "announce": 'Quarantied hospital employees: '
    },
    
}

while(True):
    # Run checks every 5 seconds
    time.sleep(5)

    # Get data
    for source in sources:
        sources[source]['data']=sources[source]['getter']()

    if(log_info): print('---' + time.strftime("%H:%M:%S", time.localtime()) + '---')

    for statistic in statistics:
        if(log_info): print(statistics[statistic]['announce']+str(statistics[statistic]['total']))

        # get datasource
        data = sources[statistics[statistic]['data_source']]['data']

        if(statistics[statistic]['total'] < statistics[statistic]['getter'](data)):
            statistics[statistic]['total'] = statistics[statistic]['getter'](data)
            play_text(statistics[statistic]['announce']+str(statistics[statistic]['total']))
