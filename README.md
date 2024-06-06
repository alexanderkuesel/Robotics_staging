# Intro
Escape Velocity (the minimum speed needed for a body (or set of files) to pull away from an Orbit) is designed to pull zip files from specified Boston Dynamics Orbit servers. At the moment it also extracts jpgs from each zip file for AI model training

## Requirements
- Be on the Intel VPN
- Future: access to orbit server


## How to
1. Install all files in a common directory, keeping their original structure
2. Start by opening main.py
3. Use the preferences.json file to edit mission name, start time, end time and hourly step


### To do
- Add CA cert authentication instead of hard-code token
- Add more user friendly input method
- Extend settings.json to include all user input

