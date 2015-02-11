'''Tools for displaying data.'''

import os
from numpy import reshape
from matplotlib.pyplot import imsave


def mk_imgs(path, data):
    """For each data point in collect.Data() object data, create an image
    representing the data point and save it in a dedicated folder located at
    path.

    Warning: If data does not have a specified dims attribute, mk_imgs will
    fail."""

    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(len(data.data)):
        name = path+'%03d.png' % (i+1)
        img = reshape(data.data[i], data.dims, 'F')
        imsave(name, img.T, cmap='gray')
        print 'Saved img %d of %d' % (i+1, len(data.data))
    print 'Done.'