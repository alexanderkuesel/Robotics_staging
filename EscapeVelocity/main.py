import json
import os
from datetime import datetime
from package.OrbitExtractor import targetOrbit

# Load json config
current_dir = os.path.dirname(os.path.abspath(__file__))
zip_dir = os.path.join(current_dir, '/zips')

##Hard-coded settings file (server info)
config_path = os.path.join(current_dir, 'config/settings.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

##user changeable settings (mission name, etc)
pref_path = os.path.join(current_dir, 'config/preferences.json')
with open(pref_path, 'r') as pref_file:
    pref = json.load(pref_file)

## Instance creation with each server (using settings.json)
OC_A = targetOrbit(**config['OC_A'])
OC_B = targetOrbit(**config['OC_B'])
OC_SCOUT = targetOrbit(**config['OC_SCOUT'])

##Get user preferences from json
target_server = pref['User_input']['target_server']
mission_name = pref['User_input']['mission_name']
start_time = pref['User_input']['start_time']
end_time = pref['User_input']['end_time']
hourly_step = pref['User_input']['hourly_step']
filter = pref['User_input']['filter']

##HATE this way of doing it, not modular at all
match target_server:
    case 'OC_A':
        print(f'Gathering all zip files from {target_server} for: {mission_name} in range {start_time} to {end_time}')
        OC_A.crawler(mission_name, start_time, datetime.now(), 24)
        print(f'Extracting jpgs from {current_dir}')
        OC_A.jpg_extract(current_dir, filter,'jpgOutput')
    case 'OC_B':
        print(f'Gathering all zip files from {target_server} for: {mission_name} in range {start_time} to {end_time}')
        OC_B.crawler(mission_name, start_time, datetime.now(), 24)
        print(f'Extracting jpgs from {current_dir}')
        OC_B.jpg_extract(current_dir, filter,'jpgOutput')
    case 'OC_SCOUT':
        print(f'Gathering all zip files from {target_server} for: {mission_name} in range {start_time} to {end_time}')
        OC_SCOUT.crawler(mission_name, start_time, datetime.now(), 24)
        print(f'Extracting jpgs from {current_dir}')
        OC_SCOUT.jpg_extract(current_dir, filter,'jpgOutput')

