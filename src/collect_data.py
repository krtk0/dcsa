# -*- coding: utf-8 -*-

from twitter import OAuth, TwitterStream
from tqdm import tqdm
from nltk.tokenize import TweetTokenizer
import logging
import re

__author__ = "Yevhen Dukhno"

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

url_pattern = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop
              |info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax
              |az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|
              cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|
              gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|
              kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|
              mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|
              rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|
              tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\(
              [^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\
              [\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|c
              at|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|
              au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|
              cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|
              gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|
              ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|
              mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|
              ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|
              tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


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
        """
        params = cls._get_settings('../settings.txt')
        auth = OAuth(params["access_token_key"], params["access_token_secret"], params["api_key"], params["api_secret"])
        stream = TwitterStream(auth=auth)
        tweet_iter = stream.statuses.filter(
            locations=geo,
            languages=lang
        )
        with open("../output_files/tweets.txt", "w") as tweets:
            with open("../output_files/hashtags.txt", "w") as hashtags:
                count = 0
                for tweet in tqdm(tweet_iter):
                    if count > num_of_tweets:
                        break
                    if not 'text' in tweet:
                        print('No text in tweet ', tweet)
                        continue
                    new_tweet = TweetTokenizer().tokenize(tweet["text"].lower())
                    for word in new_tweet:
                        if not re.match(re.compile(url_pattern), word):
                            tweets.write(word + " ")
                    for ht in tweet["entities"]["hashtags"]:
                        hashtags.write(ht["text"].lower() + " ")
                    count += 1

    @classmethod
    def get_from_file(cls, tweets=None, hashtags=None):
        """
        Get a list of tokenized tweets or hashtags from file. Exactly one of tweets or hashtags param should be True
        :param tweets: set True to get tweets
        :param hashtags: set True to get hashtags
        :return: list of str
        """
        if tweets:
            filename = "tweets"
            hashtags = False
        if hashtags:
            filename = "hashtags"

        with open("../output_files/{}.txt".format(filename), "r") as file:
            output = ""
            for line in file:
                output += line
        return output.split(" ")


if __name__ == '__main__':
    TweetsGetter.harvest_tweets(num_of_tweets=20000, lang='en', geo='-122.995004,32.323198,-67.799695,49.893813')
