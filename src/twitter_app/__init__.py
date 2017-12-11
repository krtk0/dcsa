# -*- coding: utf-8 -*-

from twitter import OAuth, TwitterStream
from tqdm import tqdm
from nltk.tokenize import TweetTokenizer
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
        Writes hashtags from collected tweets into the file PROJECT_LOCATION/output_files/hashtags.txt
        :return {tweets: list of words from tokenized tweets, hashtags: list of hashtags from collected tweets}
        """
        params = cls._get_settings('../settings.txt')
        auth = OAuth(params["access_token_key"], params["access_token_secret"], params["api_key"], params["api_secret"])
        stream = TwitterStream(auth=auth)
        tweet_iter = stream.statuses.filter(
            locations=geo,
            languages=lang
        )
        result = {"tweets": [], "hashtags": []}
        with open("../output_files/tweets.txt", "w") as tweets:
            with open("../output_files/hashtags.txt", "w") as hashtags:
                count = 0
                for tweet in tqdm(tweet_iter):
                    if count > num_of_tweets:
                        break
                    tweets.write(str(tweet) + "\n\n")
                    result["tweets"].extend(TweetTokenizer().tokenize(tweet["text"].lower()))
                    for ht in tweet["entities"]["hashtags"]:
                        hashtags.write(ht["text"].lower() + ", ")
                        result["hashtags"].append(ht["text"].lower())
                    count += 1
        return result
