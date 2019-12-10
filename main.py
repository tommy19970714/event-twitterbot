import time
import tweepy
import os
import sys
from src.twitter import get_api, consumer_key, consumer_secret, access_token, access_token_secret
from src.database import Database
import src.eventpage
import datetime
import schedule

def calc_date(days=14):
    today = datetime.today()
    next_n_day = today + timedelta(days=days)
    return int(next_n_day.strftime('%Y%m%d'))

def save_user(api, screen_name, db):
    user = api.get_user(screen_name)
    friends = user.friends_count
    followers = user.followers_count
    ffrate = friends / followers
    tweets = api.user_timeline(screen_name=screen_name, count=1)
    if not tweets:
        update_at = result[0].created_at
    db.add_user(screen_name, friends, followers,
                None, False, update_at)

def crawling_job(api, db):
    day = calc_date(days=14)

    events = Event().from_date([day])
    for event in events:
        url = participation_url(event)
        page = Page(url)

        organizers = page.organizers()
        for name in organizers:
            save_user(api, name, db)

        presenters = page.presenters()
        for name in presenters:
            save_user(api, name, db)


def follow_job(api, db, follow_lim_daily=20, follow_lim_once=5):
    today_count = db.follow_count_today()
    if today_count > follow_lim_daily:
        return
    users = db.read_users(count=follow_lim_once)
    try:
        for u in users:
            user = api.get_user(u.screen_name)
            user.follow()
            update_user(user.screen_name, "followed", True)
            update_user(user.screen_name, "followed_at",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(10)
    except tweepy.RateLimitError:
        time.sleep(15 * 60)
    except Exception as e:
        raise e


 def unfollow_job(api, db, unfollow_lim_daily=20, unfollow_lim_once=5):
    today_count = db.unfollow_count_today()
    if today_count > unfollow_lim_daily:
        return
    users = db.read_unfollow_users(count=unfollow_lim_once)
    followers = api.followers_ids()
    try:
        for u in users:
            user = api.get_user(u.screen_name)
            if user.id in followers:
                user.unfollow()
                update_user(user.screen_name, "unfollowed", True)
                update_user(user.screen_name, "unfollowed_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                time.sleep(10)
    except tweepy.RateLimitError:
        time.sleep(15 * 60)
    except Exception as e:
        raise e

if __name__ == "__main__":
    api = get_api(consumer_key, consumer_secret,
                  access_token, access_token_secret)
    db = Database()

    schedule.every(2).hours.do(follow_job, api=api, db=db,
                               follow_lim_daily=100, follow_lim_once=5)

    schedule.every().day.at("10:00").do(crawling_job, api=api, db=db))

    while True:
        schedule.run_pending()
        time.sleep(1)
