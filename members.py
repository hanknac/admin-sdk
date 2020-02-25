##########################################################################################
#  Disclaimer                                                                            #
#                                                                                        #
# This code is not an official Google product. The code is in an open-source project,    #
# which is available under the Apache License, Version 2.0. You can use the code as a    #
# starting point and configure it to fit your requirements. You are responsible for      #
# ensuring that the environment and applications that you build on top of Google Cloud   #
# are properly configured and secured.                                                   #
#                                                                                        #
##########################################################################################

from __future__ import print_function
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import csv
import json
from datetime import datetime
from apiclient.http import MediaFileUpload
import argparse

creds = None

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

SCOPES = ['https://www.googleapis.com/auth/admin.directory.group','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/admin.directory.user']
SERVICE_ACCOUNT_FILE = config["service-account"]

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
d_creds = creds.with_subject(config["gsuite-account"])

service = build('admin', 'directory_v1', credentials=d_creds)
drive_service = build('drive', 'v3', credentials=d_creds)
user_service = build('admin', 'directory_v1', credentials=d_creds)

filename = 'members-' + datetime.now().strftime("%b-%d-%Y:%H:%M:%S")+'.csv'

members_list = []
header = ['member of', 'full name', 'email', 'type', 'status', 'creationTime', 'lastLogin', 'suspended', 'Change Password Flag']
members_list.append(header)

class UserAccount:
    fullName = ''
    lastLoginTime = ''
    creationTime = ''
    suspended = ''
    changePasswordAtNextLogin = ''

#print(filename)

def listmembers(groupId):
    try:
        results = service.members().list(groupKey=groupId).execute()
        members = results.get('members', [])

        if not members:
            print('No members in the group.')
        else:
            for member in members:
                u = getUser(member)
                newrow = [groupId, u.fullName, member['email'], member['type'], member['status'], u.creationTime, u.lastLoginTime, u.suspended, u.changePasswordAtNextLogin]
                members_list.append(newrow)
                #print(u'{0} {1} {2} {3}'.format(groupId, member['email'], member['type'], member['status']))
                with open(filename, 'w') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(members_list)
                writeFile.close()

                if member['type'] == 'GROUP':
                    listmembers(member['email'])
    except Exception as e:
        print('Error: ' + str(e))
        newrow = [str(e)]
        members_list.append(newrow)
        with open(filename, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(members_list)
        writeFile.close()


def getUser(member):
    try:
        userkey = member['email']
        UserObj = UserAccount()

        if member['type'] == 'USER':

            user = user_service.users().get(userKey=userkey).execute()
            #user = results.get('user',[])

            if not user:
                print('user not found')
            else:
                #print(u'{0} {1} {2}'.format(user['name']['fullName'], user['lastLoginTime'], user['creationTime'], user['suspended'], user['changePasswordAtNextLogin']))
                UserObj.fullName = user['name']['fullName']
                UserObj.lastLoginTime = user['lastLoginTime']
                UserObj.creationTime = user['creationTime']
                UserObj.suspended = user['suspended']
                UserObj.changePasswordAtNextLogin = user['changePasswordAtNextLogin']
                #print(user.keys())

        return UserObj
    except Exception as e:
        print('Error: ' + str(e))
        newrow = [str(e)]
        members_list.append(newrow)
        with open(filename, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(members_list)
        writeFile.close()

def uploadcsv():
    try:
        csv_metadata = {
            'name' : 'Members Report',
            'parents' : config["drive-folderId"],
            'mimeType' : 'application/vnd.google-apps.spreadsheet'
        }

        media = MediaFileUpload(filename,
                            mimetype='text/csv')

        file = drive_service.files().create(body=csv_metadata,media_body=media,fields='id').execute()
    except Exception as e:
        print('Error: ' + str(e))
        newrow = [str(e)]
        members_list.append(newrow)
        with open(filename, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(members_list)
        writeFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', required=True, help="group email address")
    args = parser.parse_args()

    listmembers(args.group)

    if os.path.exists(filename):
        uploadcsv()
