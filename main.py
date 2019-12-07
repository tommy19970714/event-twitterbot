import tweepy
import src.eventpage as eventpage

if __name__ == "__main__":
    user = api.get_user(username)
    db.save_twitter_user(user)

    for user in db.users.ffrate():
        if user.is_good_to_follow():
            me.follow(user)
    