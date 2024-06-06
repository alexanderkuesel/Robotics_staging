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
mission_name = pref['User_input']['mission_name']
start_time = pref['User_input']['start_time']
end_time = pref['User_input']['end_time']
hourly_step = pref['User_input']['hourly_step']


##Execution Space
print(f'Gathering all zip files for: {mission_name} in range {start_time} to {end_time}')
OC_B.crawler(mission_name, start_time)

print(f'Extracting jpgs from {current_dir}')
OC_B.jpg_extract(current_dir, 'jpgOutput')