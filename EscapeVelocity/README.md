# Intro
Escape Velocity (the minimum speed needed for a body (or set of files) to pull away from an Orbit) is designed to pull zip files from specified Boston Dynamics Orbit servers. At the moment it also extracts jpgs from each zip file for AI model training

## Requirements
- Be on the Intel VPN
- Be an admin or Data Reviewer in the targeted Orbit servers

## How to
1. Install all files in a common directory, keeping their original structure
2. API key setup
    Since API keys can not be openly shared, you must gather your own from each respective Orbit server
    a. Open Orbit server via URL
    b. Go to user settings by clicking on the account button on the top right
    c. Select the "API Access Tokens"
    d. Click on the Create New API Access Token (+ sign)
    e. Give the token a unique name and check the Data Reviewer box
    f. Copy the token (it will not show up again!)
    g. Repeat for all existing servers, storing the token for each
    h. Create a file under the /config directory named "keys.json"
    i. Copy the following json code into that file and replace the "paste token...." with the respective API token from step f
    ```json
    {
        "OC_A": {
        "token": "paste_token_for_OC_A_here"
        },
        "OC_B": {
        "token": "paste_token_for_OC_B_here"
        }
    }
    ```
    j. Save the file
3. Use the preferences.json file to edit mission name, start time, end time, filter and hourly step
   **{All JSON parameters must be strings in double quotes}**
    - **mission_name**: Go to Orbit Server and copy exactly as it shows in the UI. Default: "OC23 - BCD Levels"
    - **start_time**: Must be in isostring format. Default "2024-06-05T12:00:00.00"
    - **end_time**: Must be in isostring format. Default "datetime.now()" *hard-coded at the moment*
    - **hourly_step**: Hourly range to run. Only change if you see more than 20 missions are being returned. Must be int. Default = 6
    - **filter**: catch-all filter that can be used to only save images with certain string. Must be string. Recommend it to be long to actually work. Default = "" (allow all)
4. Run the main.py (make sure you saved the preferences.json before running)
5. I would recommend clearing out the zipFiles and output folders after use as it might try to go through those files and return spurious results

## To do (development)
- OOP the target server selection....sub-class or dictionary
- Clear out the empty folders created by the extract
- Add CA cert authentication instead of hard-code token
- Make preferences.json templates
- Make a better filter (filter by action, filetype, etc). Add an anti-filter (discards anything containing (for example ptz))
- Integrate azcopy


