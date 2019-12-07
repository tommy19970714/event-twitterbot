import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

# Twitter CommentScreen secrets
consumer_key = os.getenv("TW_CS_CONSUMERKEY")
consumer_secret = os.getenv("TW_CS_CONSUMERSECRET")
access_token = os.getenv("TW_CS_ACCESSTOKEN")
access_token_secret = os.getenv("TW_CS_ACCESSTOKENSECRET")


def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


if __name__ == '__main__':
    api = get_api(consumer_key, consumer_secret,
                  access_token, access_token_secret)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
