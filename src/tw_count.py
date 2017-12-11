from src.twitter_app import TweetsGetter
from mrjob.job import MRJob
import logging

tweets = TweetsGetter.get_from_file(tweets=True)


class TweetMRJob(MRJob):

    def mapper(self, _, line):
        for word in tweets:
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
    TweetMRJob.run()
