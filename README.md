#admin-sdk
python script that generates a list of users that are members in the specified group

#Execution parameters
--group mygroup@xyz.com

#Prerequisites
1. Enable Admin sdk API from via GCP console
2. Create a GCP service account
..1. Create service account key
..2. Enable GSuite domain-wide delegation
3. GSuite Account with Admin API Privileges
..1. Custom Admin role (ie Directory Reader) 
..2. Users-Read
..3. Groups-Read
4. Create / Identify GSuite Folder as the destination for the reports
5. Grant appropriate end users view access to the folder
6. Grant GSuite Account (item 3) write access to the folder


#Disclaimer
The code contained in this repo is not an official Google products
Statements or claims are my own and do not represent my employer(s) past or present.
I release this source code under Apache License, Version 2.0 .


#THE END
