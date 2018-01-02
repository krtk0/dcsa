from src.twitter_app import TweetsGetter
import logging

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TweetsGetter.harvest_tweets(num_of_tweets=20000, lang='en', geo='-122.995004,32.323198,-67.799695,49.893813')
