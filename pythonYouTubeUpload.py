# Sean Heisey
# 1/13/2024
# Python YouTube Video Upload
# basic version

import os
import sys
import requests
import datetime
import shutil
from rapid_tags import RapidTags
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

class youtube:
    apiName = 'youtube'
    apiVersion = 'v3'
    scopes = ['https://www.googleapis.com/auth/youtube',
              'https://www.googleapis.com/auth/youtube.force-ssl']
    def __init__(self, clientFile):
        self.service = None
        self.client_file = clientFile
    def initService(self):        
        self.service = createService(self.client_file, self.apiName, self.apiVersion, self.scopes)

def createService(clientSecretFile, apiName, apiVersion, *scopes, prefix=''):
    allScopes = [scope for scope in scopes[0]]
    creds = None
    workingDir = os.getcwd()
    tokenDir = 'token files'
    tokenFile = f'token_{apiName}_{apiVersion}{prefix}.json'
    if not os.path.exists(os.path.join(workingDir, tokenDir)):
        os.mkdir(os.path.join(workingDir, tokenDir))
    if os.path.exists(os.path.join(workingDir, tokenDir, tokenFile)):
        creds = Credentials.from_authorized_user_file(os.path.join(workingDir, tokenDir, tokenFile), allScopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(clientSecretFile, allScopes)
            creds = flow.run_local_server(port=0)
        with open(os.path.join(workingDir, tokenDir, tokenFile), 'w') as token:
            token.write(creds.to_json())
    try:
        service = build(apiName, apiVersion, credentials=creds, static_discovery=False)
        print(apiName, apiVersion, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {apiName}')
        os.remove(os.path.join(workingDir, tokenDir, tokenFile))
        return None

# input    
title = ""
while(1):
    print("Enter YouTube Video Title: ")
    title = sys.stdin.readline() # sys input, example: [FREE] Drake Type Beat | Rod Wave Type Beat "Name"
    if len(title) > 100:
        print("ERROR: title exceeds 100 characters, try again!")
    else:
        break

# rapidtags
rapidtagsSearchString = "this is whats being entered into rapidtags"
tags = str(RapidTags.get_tags_cls(rapidtagsSearchString)).replace("'", "").replace("[", "'").replace("]", "'").replace("'", "") # removes unwanted characters

# YouTube description
description = "this is your YouTube video description"

# YouTube category
category = 0 # this is your YouTube video category (int)

# handling large mp4 files using requests
requests.get('http://google.com', timeout=(30, 120)) # 60 seconds to connect to server, 300 seconds until timeout
requests.get('http://youtube.com', timeout=(30, 120))# 60 seconds to connect to server, 600 seconds until timeout

# if Google Cloud Platform token expires (expires every 7 days)
try:
    clientFile = 'clientSecret/file/directory.json!'
    service = createService(clientFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube'])
except RefreshError as e: # refresh token
    if os.path.exists('token/file/directory.json!'):
        os.remove('token/file/directory.json!')
    shutil.copy2('clientSecret/file/directory.json!', 'clientSecret/file/CHANGENAME.json!')
    time.sleep(1)
    os.remove('clientSecret/file/directory.json!')
    time.sleep(2)
    os.rename('CHANGENAME.json!', 'directory.json!')
    time.sleep(1)
    service = createService(clientFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube'])

# upload video json
requestBody = {
    'snippet': {
        'title': title,
        'description': description,
        'categoryId': category,
        'tags': [tags]
    },
    'status': {
        'privacyStatus': 'private', # public videos don't work so don't change this
        'publishedAt': (datetime.datetime.now() + datetime.timedelta(days=0)).isoformat() + '.000Z', # time video is published (ASAP)
        'selfDeclaredMadeForKids': False # true or false
    },
    'notifySubscribers': True # true or false
}

# upload video from computer
responseVideoUpload = service.videos().insert(
    part='snippet,status',
    body=requestBody,
    media_body=MediaFileUpload('choose/video/file/directory.mp4!')
).execute()

# add video to playlist
yt = youtube(clientFile)
yt.initService()

# playlist json
requestBody = {
    'snippet': {
        'playlistId': 'choose playlist id!',
        'resourceId': {
            'kind': 'youtube#video',
            'videoId': responseVideoUpload.get('id')
        }
    }
}

# add video to playlist
response = yt.service.playlistItems().insert(
    part='snippet',
    body=requestBody
).execute()
videoTitle = response['snippet']['title']

# code complete with 0 errors
print('Video inserted to playlist')
exit()
