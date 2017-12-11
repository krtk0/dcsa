from src.twitter_app import TweetsGetter
from mrjob.job import MRJob
import logging

hashtags = TweetsGetter.get_from_file(hashtags=True)


class HashtagMRJob(MRJob):

    def mapper(self, _, line):
        for word in hashtags:
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
    HashtagMRJob.run()
