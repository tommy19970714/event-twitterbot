from database import Database
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
    db = Database()

    for row in db.read_users():
        screen_name = row[1]
        friends = row[2]
        followers = row[3]
        if friends or followers:
            # already collected data
            continue
        user = api.get_user(screen_name)
        db.update_user(user.screen_name, 'friends', user.friends_count)
        db.update_user(user.screen_name, 'followers', user.followers_count)
