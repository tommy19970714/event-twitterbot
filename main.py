import time
import tweepy
import os
import sys
from src.twitter import get_api, consumer_key, consumer_secret, access_token, access_token_secret
from src.database import Database


if __name__ == "__main__":
    api = get_api(consumer_key, consumer_secret,
                  access_token, access_token_secret)
    db = Database()

    for row in db.read_users():
        screen_name = row[1]
        friends = row[2]
        followers = row[3]
        if not friends and not followers:
            # already collected data
            continue
        user = api.get_user(screen_name)
        ffrate = friends / followers
        try:
            if ffrate > 1.0:
                user.follow()
                db.update_user(user.screen_name, 'followed', 1)
                print('followed {}'.format(user.screen_name))
            else:
                db.update_user(user.screen_name, 'followed', 0)
                print('skipped {}'.format(user.screen_name))
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except Exception as e:
            raise e
