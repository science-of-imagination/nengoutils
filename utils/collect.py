'''Utility to collect data on simulations'''

import os
import gzip as gz
from cPickle import dump
from time import strftime
from numpy import mean, dot, subtract, sqrt
from numpy.linalg import norm
    

def _compose_name(path, time, index, data):
    return path+'_'.join([time+'%02d' % index, data.label+'.pkl.gz'])


def file_name(path, data):
    """Return a time-stamped file name to record Data object data at given a
    path."""
    time = strftime('%Y%m%d%H%M%S')
    index = 0
    while os.path.isfile(_compose_name(path, time, index, data)):
        index += 1
    return _compose_name(path, time, index, data)
    

def save_data(path, data):
    """Pickle and compress data, save the result to path."""
    if not os.path.exists(path):
        os.makedirs(path)
    with gz.open(file_name(path, data), 'wb') as f:
        dump(data, f)


class Data:
    """A struct to save simulation results in."""
    def __init__(self, label=None, params=None, data=None, dims=None,
                 other=None):

        self.label = label
        self.params = params
        self.data = data
        self.dims = dims
        self.other = other
