from copy import copy

# TODO: Review. Consider removing + operations
class Stats(object):
    def __init__(self,
                 count=0,
                 sum=0,
                 sum2=0,
                 max=float('-inf'),
                 min=float('inf')):
        self.count = count
        self.sum = sum
        self.sum2 = sum2
        self.max = max
        self.min = min

    def add(self, x):
        self.count += 1
        self.sum += x
        self.sum2 += x**2
        self.max = max(self.max, x)
        self.min = min(self.min, x)
        return self

    # +=
    def __iadd__(self, x):
        self.add(x)
        return self

    # Left add only
    def __add__(self, x):
        return copy(self).add(x)

    @property
    def avg(self):
        return self.sum / float(self.count)

    # TODO: Review. Would divide by N-1 be better?
    @property
    def stdev(self):
        return (self.sum2 / float(self.count) - self.avg**2) ** 0.5

    def __repr__(self):
        return "Stats(count={0.count}, sum={0.sum}, sum2={0.sum2})".format(self)

    def __str__(self):
        return "n={0.count} sum={0.sum} avg={0.avg} stdev={0.stdev:0.2} min={0.min} max={0.max}".format(self)

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_stats', failfast=True, exit=False)
