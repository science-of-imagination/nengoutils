"""This module provides utilities to collect data on simulations.

Provides:
Data -- Struct-like class for saving simulation data.
save_data -- Saves data to a given path."""


import os
import gzip as gz
from cPickle import dump
from time import strftime


def _compose_name(path, time, index, data):
    return path+'_'.join([time+'%02d' % index, data.label+'.pkl.gz'])


def _file_name(path, data):
    time = strftime('%Y%m%d%H%M%S')
    index = 0
    while os.path.isfile(_compose_name(path, time, index, data)):
        index += 1
    return _compose_name(path, time, index, data)
    

def save_data(path, data):
    """Pickle and compress data, save the result to path.

    Keyword arguments:
    path -- str, path at which to save data. path must be a path to a
        directory, save_data generates its own date stamped filename based on
        data.label.
    data -- utils.collect.Data object, the data to be saved."""

    if not os.path.exists(path):
        os.makedirs(path)
    with gz.open(_file_name(path, data), 'wb') as f:
        dump(data, f)


class Data:
    """A struct which houses simulation results."""
    def __init__(self, label='', params=None, data=None, dims=None,
                 other=None):
        """Initialize a Data object.

        Keyword args:
        label -- str (defalut=''), a label for the data.
        params -- any (default=None), a representation of the model
            parameters.
        data -- any (default=None), a representation of the model output.
        dims -- (w, h) (default=None), w,h are ints representing the width and
            height of the canvas used by the model respectively.
        other -- any (default=None), any other data associated with the model
            that you want to save."""

        self.label = label
        self.params = params
        self.data = data
        self.dims = dims
        self.other = other
