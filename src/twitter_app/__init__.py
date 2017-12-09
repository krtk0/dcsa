# -*- coding: utf-8 -*-

from twitter import OAuth, TwitterStream
from tqdm import tqdm
import logging

__author__ = "Yevhen Dukhno"

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class TweetsGetter:
    @staticmethod
    def _get_settings(file):
        """
        Get api and access-token keys from the settings file
        :param file: name of the file containing api and access-token keys in order
                     "api_key", "api_secret", "access_token_key", "access_token_secret"
        :return: {api_key_name: api_key_value}
        """
        with open(file, "r") as settings:
            values = [line.strip() for line in settings]
        return dict(zip(["api_key", "api_secret", "access_token_key", "access_token_secret"], values))

    @classmethod
    def harvest_tweets(cls, num_of_tweets, lang, geo):
        """
        Get text of the tweets in specific language and location
        :param num_of_tweets: number of needed tweets
        :param lang: languages of the needed tweets
        :param geo: location of needed tweets
        Writes tweet-messages into the file PROJECT_LOCATION/output_files/tweets.txt
        """
        params = cls._get_settings('../settings.txt')
        auth = OAuth(params["access_token_key"], params["access_token_secret"], params["api_key"], params["api_secret"])
        stream = TwitterStream(auth=auth)
        logging.info('stream: {}'.format(stream))

        tweet_iter = stream.statuses.filter(
            locations=geo,
            languages=lang
        )
        logging.info('tweet_iter: {}'.format(tweet_iter))

        with open('../output_files/tweets.txt', 'w') as file:
            count = 0
            for tweet in tqdm(tweet_iter):
                if count >= num_of_tweets:
                    break
                file.write(tweet["text"] + '\n\n')
                count += 1
