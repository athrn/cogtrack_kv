
class Stats(object):
    def __init__(self,
                 count=0,
                 sum=0,
                 sum2=0):
        self.count = count
        self.sum = sum
        self.sum2 = sum2

    def add(self, x):
        self.count += 1
        self.sum += x
        self.sum2 += x**2
        return self

    def __iadd__(self, x):
        self.add(x)
        return self

    def __add__(self, x):
        return Stats(count=self.count,
                     sum=self.sum,
                     sum2=self.sum2).add(x)

    @property
    def avg(self):
        return self.sum / float(self.count)

    # TODO: Review. Would divide by N-1 be better?
    @property
    def stdev(self):
        return (self.sum2 / float(self.count) - self.avg**2) ** 0.5

    def __str__(self):
        return "N:{0.count} Sum:{0.sum} Avg:{0.avg} Stdev:{0.stdev}".format(self)

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='teststats', failfast=True, exit=False)
