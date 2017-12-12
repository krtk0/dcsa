from mrjob.job import MRJob
import re
import logging

WORD_RE = re.compile(r"[\w']+")


class CountMRJob(MRJob):

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
    CountMRJob.run()
