import twitter
import json

def get_authenticated_service():
    with open('twitter_api_credentials.json', 'r') as f:
        credentials_dict = json.load(f)
        
        for cred in credentials_dict: 
            api = twitter.Api(consumer_key=cred['consumer_key'],
                              consumer_secret=cred['consumer_secret'],
                              access_token_key=cred['access_token_key'],
                              access_token_secret=cred['access_token_secret'])

    return api

def post_video(filename):
    file = open(filename, 'rb')
    kwargs = {'media':file}
    get_authenticated_service().PostUpdate('#TWICE #ONCE #트와이스 ', **kwargs)