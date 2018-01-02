from mrjob.job import MRJob, MRStep
import re


WORD_RE = re.compile(r"[\w']+")


class CountMRJob(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.final)
        ]

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield None, (word, sum(counts))

    def final(self, word, counts):
        self._result = []
        for v in counts:
            self._result.append(v)
        self._result.sort(key=lambda x: x[1])
        count = len(self._result)
        for m in range(count - 10, count):
            yield self._result[m]


if __name__ == '__main__':
    CountMRJob.run()
