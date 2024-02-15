# Sean Heisey
# 2/14/2024
# Python YouTube Video Upload & SEO Formatting for Type Beats

import os
import sys
import requests
import datetime
import random
import shutil
import time
from rapid_tags import RapidTags
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# enter credentials
clientSecretName = 'client_secret name'
clientSecretFilePath = 'client_secret file path/.json'
tokenFilePath = 'token file path/.json'
tokenFilePathExcludeJSON = 'token file path/'
videoFilePath = 'video file path/.mp4'
youtubePlaylistID 'playlist ID'

# premote your socials for video description 
youtubeChannelLink = 'provide link'
youtubePlayListLink = 'provide link'
instagramLink = 'provide link'
beatstarsLink = 'provide link'
email = 'provide email you want fans to message you on'

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
title = ''
while(1): # gets correct input
    print('Enter YouTube Video Title: ')
    title = sys.stdin.readline() # sys input, example: [FREE] Drake Type Beat | Rod Wave Type Beat "Name"
    if len(title) > 100:
        print('ERROR: title exceeds 100 characters, try again!')
    elif title.count('\"') != 2 or title.count('[FREE]') != 1 or title.count('Type Beat') < 1 or title.count('-') == 1:
        print('\nERROR: title format incorrect, try again!\nCheck for:\n[FREE],\nType Beat,\n\"placeholder name\",\ndelete \"-\",\n')
    else:
        break
print("Enter Key: ")
key = sys.stdin.readline() # key input
print("Enter BPM: ")
bpm = sys.stdin.readline() # bpm input

# rapidtags search string and hashtags
year = str(time.localtime().tm_year)
name = title[title.find('"'):title.rfind('"')+1]
rapidtags = title.replace('[FREE] ', '').replace('|', 'x').replace(name, year).lower()
if rapidtags.count('type beat') == 2:
    rapidtags = rapidtags.replace('type beat ', '', 1)
if rapidtags.count('type beat') == 3:
    rapidtags = rapidtags.replace('type beat ', '', 2)
if rapidtags.count('type beat') == 4:
    rapidtags = rapidtags.replace('type beat ', '', 3)
if rapidtags.find(' x ') != -1 and (rapidtags.find('type beat') == -1 or rapidtags.find(' x ') < rapidtags.find('type beat')):
    stopping_index = rapidtags.find(' x ')
elif rapidtags.find('type beat') != -1:
    stopping_index = rapidtags.find('type beat')
else:
    stopping_index = len(rapidtags)
hashtags = "#" + rapidtags[:stopping_index].replace(" ", "")
hashtags = hashtags + "typebeat " + hashtags + "typebeat" + year + " " + hashtags + "typebeatfree "

# makes tags readable when inserted into youtube
tags = str(RapidTags.get_tags_cls(rapidtags)).replace("'", "").replace("[", "'").replace("]", "'").replace("'", "") 

# YouTube description (SEO optimized) and formatted
description = (title +
               '\nBEATS ARE FREE FOR NON-PROFIT USE ONLY' +
               '\nMUST CREDIT: \"' + producerName + '\" In Song & Video Title' +
               '\n\nKey: ' + key +
               'BPM: ' + bpm +
               '\nYouTube - ' + youtubeChannelLink +
               '\nPlaylist - ' + youtubePlayListLink +
               '\nInstagram - ' + instagramLink +
               '\BeatStars - ' + beatstarsLink +
               '\nEmail - ' + email +
               '\n\nignore tags:\n' + 
               tags +
               '\n\n' + hashtags)

# handling large mp4 files using requests
requests.get('http://google.com', timeout=(30, 120)) # 60 seconds to connect to server, 300 seconds until timeout
requests.get('http://youtube.com', timeout=(30, 120))# 60 seconds to connect to server, 600 seconds until timeout

# upload video credentials
secondaryClientSecretName = 'client_secret.json'
try:
    clientFile = clientSecretName
    service = createService(clientFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube'])
except RefreshError as e: # error, attempting to refresh token
    if os.path.exists(tokenFilePath):
        os.remove(tokenFilePath)
    shutil.copy2(clientSecretFilePath, tokenFilePathExcludeJSON + secondaryClientSecretName)
    time.sleep(1)
    os.remove(clientSecretFilePath)
    time.sleep(2)
    os.rename(secondaryClientSecretName, clientSecretName)
    time.sleep(1)
    service = createService(clientFile, 'youtube', 'v3', ['https://www.googleapis.com/auth/youtube'])

# upload video json
requestBody = {
    'snippet': {
        'title': title,
        'description': description,
        'categoryId': '10', # music category
        'tags': [tags]
    },
    'status': {
        'privacyStatus': 'private',
        'publishedAt': (datetime.datetime.now() + datetime.timedelta(days=0)).isoformat() + '.000Z',
        'selfDeclaredMadeForKids': False # keep this false to not restrict views
    },
    'notifySubscribers': True
}

# upload video from computer
responseVideoUpload = service.videos().insert(
    part='snippet,status',
    body=requestBody,
    media_body=MediaFileUpload(videoFilePath)
).execute()

# add video to playlist
yt = youtube(clientFile)
yt.initService()

# playlist json
requestBody = {
    'snippet': {
        'playlistId': youtubePlaylistID,
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
