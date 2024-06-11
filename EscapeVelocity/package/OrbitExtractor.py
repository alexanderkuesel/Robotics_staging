import requests
import urllib3
from datetime import date
from datetime import timedelta
from datetime import datetime
import zipfile
import os
import re


urllib3.disable_warnings() ##insecure but need to ignore
##Directory that will contain zip files
outputDir = os.path.dirname(os.path.abspath(__file__))

class targetOrbit(): 

    def __init__(self, server_name, description, robot_list, url, token, campus):
        """init function that holds server attributes which makes it easier to call later

        Args:
            name (str): Server Name
            description (str): Description
            robot_list (tuple): Hostname of contained robots
            url (str): API url
            token (str): OAuth2.0 token
            campus (str): Campus Code
        """
        self.server_name = server_name
        self.description = description
        self.robot_list = robot_list
        self.url = url
        self.token = token
        self.campus = campus

    ##gets runs and return dictionary-> Mission Name: UUID
    def get_runs(self, start_date, end_date, missionName):
        """Gets list of runs, pulls respective JSON and converts
        Args:
            -datetime_: _Start_timedate (isostring format): 2023-06-05T19:29:35.066Z
            -datetime_: _End_timedate (isostring format): 2023-06-05T19:29:35.066Z
            -string_: missionName
        Returns:
            _list_: list of tuples (#, runID)
        """
        runIDList = []
        payload = {'startTime':start_date, 'endTime':end_date, 'missions':missionName}
        headers = {'Authorization': f'Bearer {self.token}'} ##uses OAuth 2.0 w/ Bearer token
        r = requests.get(self.url+'runs', headers=headers, verify=False, params=payload) ##add 
        if r.status_code == 200:
            out = r.json()
            i=0
            for each in out['resources']:
                runIDList.append(out['resources'][i]['uuid']) ##add tuple to list
                #print(runIDList[i])
                i = i+1
        else:
            print(f'Failed to retrieve data. Status code: {r.status_code}')
        
        return runIDList

    def get_run_zip(self, run_id, missionName):
        """Downloads zip file for specific run using the run id
        Args:
            run_id (_string_): _UUID identifying specific run_
            mission_name (_string_): _Name of Mission containing run_
        Return:
            Writes zip file to uppermost directory
        """
        headers = {'Authorization': f'Bearer {self.token}' } ##authorize via hard-coded API token (different for each server)
        r = requests.get(self.url+f'run_archives/{run_id}', headers=headers, verify=False)
        if r.status_code == 200:
            # Define the directory to save the downloaded ZIP file
            zip_dir = 'zipFiles'
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the 'zips' directory
            zip_dir_path = os.path.join(current_dir, zip_dir)
            # Create the 'zips' directory if it does not exist
            if not os.path.exists(zip_dir_path):
                os.makedirs(zip_dir_path)
            # Define the local filename to save the downloaded ZIP file
            local_filename = f'{missionName}_{date.today()}_{run_id[:6]}.zip'
            # Construct the full path to the local file
            local_file_path = os.path.join(zip_dir_path, local_filename)
            # Open a local file with write-binary ('wb') permission
            with open(local_file_path, 'wb') as file:
                # Write the content of the response to the file in chunks
                for chunk in r.iter_content(chunk_size=128):
                    file.write(chunk)
        return zip_dir_path

    def crawler(self, missionName, startTime, endTime = datetime.now(), hourly_step=6):
        """_summary_
        Iterates through time ranges specified by hourly_step (6) and pulls zip files
        Args:
            missionName (_str_): name of mission
            hourly_step: how long time ranges to run query
        Returns:
            masterList (_list_): list of lists
        """
        start = datetime.fromisoformat(startTime) ##removed offset awareness (Z at end)
        runCount = 0 #runs related to requested mission
        span = endTime - start #how much time since first capture date
        print(f"Time Span: {span}") 
        step = start 
        ##starts at the first step and increments by hourly_step until it reaches 
        #i = 0
        while step <= endTime:
            print(step)
            stepper = step + timedelta(hours=hourly_step) #divide into step time ranges to avoid run api limit of 20
            runIDList = self.get_runs(step, stepper, missionName) ##list
            for runID in enumerate(runIDList):
                #print(type(runID))
                print(runID[1])
                self.get_run_zip(runID[1], missionName) ##just print the id in the tuple 
                runCount += 1
            step += timedelta(hours=hourly_step) #create an hourly time range for the pull
        print(f"Missions found: {runCount}")
        print(len(runIDList))
            #self.get_run_zip(runID[i])

    def jpg_extract(self, dir, filter, outputFolder = 'output'):
        """Extract images from zip files and outputs to specified filename

        Args:
            dir (string): Directory containing zip files
        """
        regexDT = r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}'
        output_dir = os.path.join(dir, outputFolder)  # output Folder

        for subdir, dirs, files in os.walk(dir):
            for filename in files:
                if filename.endswith(".zip"):
                    # Construct the full file path
                    filepath = os.path.join(subdir, filename)
                    # Open the zip file
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        # List all the file names in the zip
                        for file in zip_ref.namelist():
                            # Extract the datetime from the file name
                            match = re.search(regexDT, file)
                            if match:
                                newName = match.group()
                                # Check if the file is a JPG
                                if file.lower().endswith(".jpg"):
                                    if filter in file: #applies positive filter to search to only return files with filter in name
                                        # Construct the new file name with the datetime appended
                                        file_basename = os.path.basename(file)  # Get the base name of the file
                                        new_file_name = f"{file_basename}_{newName}.jpg"  # Append datetime to the base name
                                        # Extract the file to a temporary path
                                        extracted_path = zip_ref.extract(file, output_dir)
                                        # Construct the new file path in the output directory
                                        new_file_path = os.path.join(output_dir, new_file_name)
                                        # Rename and move the extracted file to the new path
                                        os.rename(extracted_path, new_file_path)
                                        print(f"Extracted and renamed {file} to {new_file_path}")


