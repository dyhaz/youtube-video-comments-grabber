import credentials as cred
import gifsearch as gif
import mux
import post_twitter as tw
import os
import pickle
import random
import urllib.request
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from moviepy.editor import *

def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred.CLIENT_SECRETS_FILE, cred.SCOPES)
            credentials = flow.run_console()
 
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
 
    return build(cred.API_SERVICE_NAME, cred.API_VERSION, credentials = credentials)

def get_video_comments(service, video_id):
    comments = []
    video_id = video_id.replace('https://youtu.be/', '')
    kwargs = {'part':'snippet','videoId':video_id,'maxResults':20,'textFormat':'plainText'}
    results = service.commentThreads().list(**kwargs).execute()
 
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
 
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
 
    return comments

def get_video_informations(service, video_id):
    informations = {}
    video_id = video_id.replace('https://youtu.be/', '')
    kwargs = {'part':'snippet,contentDetails,statistics','id':video_id,'maxResults':20}
    results = service.videos().list(**kwargs).execute()

    while results:
        for item in results['items']:
            contentDetails = item['contentDetails']
            statistics = item['statistics']
            informations['duration'] = contentDetails['duration']
            informations['viewCount'] = statistics['viewCount']
 
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.videos().list(**kwargs).execute()
        else:
            break
 
    return informations

def get_video_links(service, channel_id):
    links = []
    channel = service.channels().list(id=channel_id, part="contentDetails,contentOwnerDetails", maxResults=1).execute()
    uploadsID = channel['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    kwargs = {'part':'snippet,contentDetails', 'playlistId':uploadsID, 'maxResults':50}
    results = service.playlistItems().list(**kwargs).execute()
    
    while results:
        for item in results['items']:
            contentDetails = item['contentDetails']
            links.append(contentDetails['videoId'])
 
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.playlistItems().list(**kwargs).execute()
        else:
            break

    return links
    
    
def search_video(service, keyword):
    links = []
    i = 0
    kwargs = {'q':keyword, 'part':'snippet', 'type':'video', 'maxResults':25}
    results = service.search().list(**kwargs).execute()

    while results:
        for item in results['items']:
            links.append(item['id']['videoId'])
 
        if 'nextPageToken' in results and i < 10:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break

    return links

def convert_to_mp3(mp4_file):
    video = VideoFileClip(mp4_file)
    video.audio.write_audiofile(mp4_file.replace('mp4', 'mp3'))

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    # videoLinks = get_video_links(service, 'UCzgxx_DM2Dcb9Y1spb9mUJA')
    videoLinks = search_video(service, 'twice color coded')
    videoId = random.choice(list(videoLinks))

    while True:
        try:
            YouTube('https://youtu.be/' + videoId).streams.first().download()
            break
        except:
            print('Failed to download video')
            videoId = random.choice(list(videoLinks))

    if not os.path.exists('downloads/' + videoId + '.mp4'):
        for filename in os.listdir("."):
            if '.mp4' in filename or '.webm' in filename:
                dst = 'downloads/' + videoId + ".mp4"
                src = filename
                os.rename(src, dst)
        convert_to_mp3('downloads/' + videoId + '.mp4')

    while True:
        keyword = 'dance'
        image_set = gif.get_gifs_by_keyword(keyword)['results']
        image_result = random.choice(list(image_set))
        duration = image_result['media'][0]['loopedmp4']['duration']
        if duration >= 3.0:
            urllib.request.urlretrieve(image_result['media'][0]['loopedmp4']['url'], 'downloads/' + keyword + videoId + '.mp4')
            mux.combine(videoId, keyword)
            tw.post_video('downloads/output' + videoId + '.mp4')
            break
