# Disclaimer
- The code contained in this repo is not an official Google product
- Statements or claims are my own and do not represent my employer(s) past or present.
- I release this source code under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

# Overview
python script that generates a list of users that are members in the specified group

# Prerequisites
1. Enable Admin sdk API from via GCP console

2. Create a GCP service account
  - Create service account key
  - Enable GSuite domain-wide delegation

3. Create GSuite Account with Admin API Privileges
  - Custom Admin role (ie Directory Reader) 
  - Users-Read
  - Groups-Read

4. Create / Identify GSuite Folder as the destination for the reports
  - Grant appropriate end users view access to the folder
  - Grant GSuite Account (item 3) write access to the folder

# Setup
1. Clone the repo
  - git clone

2. Navigate to the admin-sdk directory
  - cd admin-sdk

3. Install python dependencies
  - pip3 install -r requirements.txt
  
4. Place the key file created in Prereq step #2 to the admin-sdk directory

5. Update the config.json file using your favorite text editor (ie vim)
  - GCP service account key file
  - GSuite user account that had API access
  - Destination folderID for the report
  
# Execution
- cd admin-sdk
- python3 members.py --group **group@abc**.com


# THE END
