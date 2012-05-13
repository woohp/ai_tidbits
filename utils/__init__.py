from itertools import *

def argmax(col, valFunc, condFunc=None):
    if condFunc == None:
        return max(((x, valFunc(x)) for x in col), key=lambda x: x[1])[0]
    else:
        return max(((x, valFunc(x)) for x in col if condFunc), key=lambda x: x[1])[0]

def argmin(col, valFunc, condFunc=None):
    if condFunc == None:
        return min(((x, valFunc(x)) for x in col), key=lambda x: x[1])[0]
    else:
        return min(((x, valFunc(x)) for x in col if condFunc), key=lambda x: x[1])[0]
