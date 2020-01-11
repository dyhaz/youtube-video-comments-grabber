import credentials as cred
import os
import pickle
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


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
    results = service.commentThreads().list(part='snippet',videoId=video_id,maxResults=100,textFormat='plainText').execute()
 
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

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    print(get_video_comments(service=service, video_id='https://youtu.be/kOHB85vDuow'))


#YouTube('https://youtu.be/kOHB85vDuow').streams.first().download()
print(cred.API_VERSION)
