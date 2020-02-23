from grab import *
from config import *
import random

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    videoLinks = get_video_links(service, 'UCWzhcucSYsGdPhfqUvC_qlQ')
    videoId = random.choice(list(videoLinks))
    retries = 0
    while True and retries <= maxRetries:
        try:
            download_video('https://youtu.be/' + videoId)
            break
        except:
            print('Failed to download video ' + videoId)
            videoId = random.choice(list(videoLinks))

        retries += 1
    
    