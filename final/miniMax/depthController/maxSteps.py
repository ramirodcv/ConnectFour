from miniMax.optimizers import *


# recurse a certain amount of steps
class MaxSteps(DepthController):
    def __init__(self, maxSteps):
        self.steps = maxSteps

    # returns True if the maximum amount of steps have not been taken
    def __bool__(self):
        return self.steps >= 0

    # reduce the number of steps by 1
    def next(self, move=None, score=None, optimizing=False):
        if optimizing:
            return MaxSteps(self.steps - 1)
        return self

