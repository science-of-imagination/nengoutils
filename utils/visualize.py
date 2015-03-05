"""This module provides utilities for displaying data.

Provides:
mk_imgs -- Creates and saves an image for each data point in a
    utils.collect.Data object."""

import os
from numpy import reshape
from matplotlib.pyplot import imsave


def mk_imgs(path, data, dims):
    """For each data point in collect.Data() object data, create an image
    representing the data point and save it in a dedicated folder located at
    path.

    Warning: If data does not have a specified dims attribute, mk_imgs will
    fail.

    Keyword arguments:
    path -- str, path at which to save data. path must be a path to a
        directory, save_data generates its own date stamped filename based on
        data.label.
    data -- utils.collect.Data object, the data to be saved."""

    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(len(data)):
        name = path+'%03d.png' % (i+1)
        img = reshape(data[i], dims, 'F')
        imsave(name, img.T, cmap='gray')
        print 'Saved img %d of %d' % (i+1, len(data))
    print 'Done.'