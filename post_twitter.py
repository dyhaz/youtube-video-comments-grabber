import twitter
import json
with open('twitter_api_credentials.json', 'r') as f:
    credentials_dict = json.load(f)
    
    for cred in credentials_dict: 
        api = twitter.Api(consumer_key=cred['consumer_key'],
                          consumer_secret=cred['consumer_secret'],
                          access_token_key=cred['access_token_key'],
                          access_token_secret=cred['access_token_secret'])

        api.PostUpdate('once')