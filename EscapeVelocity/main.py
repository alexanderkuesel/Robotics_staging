import json
import os
from datetime import datetime
from OrbitExtractor import targetOrbit

# Load json config
current_dir = os.path.dirname(os.path.abspath(__file__))
zip_dir = os.path.join(current_dir, '/zips')
config_path = os.path.join(current_dir, 'config/settings.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

## Instance creation with each server (using settings.json)
OC_A = targetOrbit(**config['OC_A'])
OC_B = targetOrbit(**config['OC_B'])
OC_SCOUT = targetOrbit(**config['OC_SCOUT'])


##!!!!User input space!!!!!
#mission_name = 'OC23 - BCD Levels' ##make sure it is the EXACT name, including any accidental spaces
mission_name = config['User_input']['mission_name']
start_time = '2024-05-27T12:00:00.00' ##needs to be in isostring format
end_time = datetime.now() ##default is to pull everything up to NOW
hourly_step = 6 ##only change if your results are seemingly limited by the 20 run id call limit in Orbit. 


##Execution Space
print(f'Gathering all zip files for: {mission_name} in range {start_time} to {end_time}')
OC_B.crawler(mission_name, start_time)

print(f'Extracting jpgs from {current_dir}')
OC_B.jpg_extract(current_dir, 'jpgOutput')