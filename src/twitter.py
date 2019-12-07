import os
import time
import tweepy
from dotenv import load_dotenv
load_dotenv()
if __name__ != "__main__":
    from src.database import Database

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


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


if __name__ == '__main__':
    from database import Database
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
        friends = user.friends_count
        followers = user.followers_count
        db.update_user(user.screen_name, 'friends', friends)
        db.update_user(user.screen_name, 'followers', followers)
