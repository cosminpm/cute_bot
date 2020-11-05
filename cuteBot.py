# tweepy-bots/bots/config.py
import tweepy
import logging
import random
import os
from PIL import Image
import time



TIME_WAITING = 60

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_api():
    consumer_key = "-----"
    consumer_secret = "-----"
    access_token = "-----"
    access_token_secret = "-----"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api



def check_mentions(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        # Para eliminar directamente los tuits de la timeline, se eliminan aquellos tuits simplemente dando "fav" al tuit.
        if not tweet.favorited:
            new_since_id = max(tweet.id, new_since_id)
            tweet.favorite()
            stat = "@"+str(tweet.author.screen_name)
            imagen = randomPhoto()
            api.update_with_media(imagen,status= (stat), in_reply_to_status_id=tweet.id)
            logger.info("Respondiendo a "+stat)
    return new_since_id


def randomPhoto():
	path = "./ImagesCuteBot/"
	files = os.listdir(path)
	imagen = random.choice(files)
	return "./ImagesCuteBot/"+imagen

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        time.sleep(TIME_WAITING)
main()
