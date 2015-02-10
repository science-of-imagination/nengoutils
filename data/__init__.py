'''
This module provides functions for loading modeling data.
'''


import gzip as gz
from cPickle import load, dump
import Image
from numpy import array, subtract, meshgrid, linspace, cos, sin, pi
from numpy.random import uniform
from numpy.linalg import norm


def mk_gratings(canvas_size,filename):
    '''Create stimulus gratings for a square canvas of size canvas_size. Save
    gratings to filename.

    Creates gratings at each of the following frequencies (in cycles per
    width):
    2**3, 2**2, 2, 1, 2**-1, 2**-2, 2**-3.

    And in each of the following orientations:
    0, 2*pi/3, 4*pi/3.

    Output is a .pkl.gz (see load_data). The pickle is a list of sub-lists.
    Each sub-list is a pair [params, grating] where params are the parameters
    used to create the grating and grating is an array representing the grating
    in raster format.
    '''

    gratings = []
    lambds = [2**3,2**2,2,1,2**-1,2**-2,2**-3]
    thetas = [0,2*pi/3,4*pi/3]    
    for theta in thetas:
        for lambd in lambds:
            #uniform(0,2*pi)
            psi = uniform(0,2*pi)
            g = grating(canvas_size,lambd,theta,psi)
            gratings.append([[canvas_size,lambd,theta,psi],g])
            #gratings.append(g)
            #imshow(gratings[(canvas_size,lambd,theta,psi)], cmap='gray')
            #plt.show()

    #if not os.path.exists(filename):
    #    os.makedirs(filename)
    with gz.open(filename, 'wb') as f:
        dump(gratings, f)


def grating(canvas_size, lambd, theta, psi):
    '''Return a grating of frequency lambda, orientation theta and phase psi
    on a canvas of size canvas_size.
    '''
    x = linspace(-1, 1, canvas_size)
    y = linspace(-1, 1, canvas_size)
    X, Y = meshgrid(x, y)


    cosTheta = cos(theta)
    sinTheta = sin(theta)
    xTheta = X * cosTheta  + Y * sinTheta
    yTheta = -X * sinTheta + Y * cosTheta
    
    cosed = cos((2 * pi * xTheta / lambd) + psi)
    return cosed


def load_img(imgpath, dims):
    """Load the image at image path and return a version scaled to dims
    represented in the form of an array where a pixel activation of 0 means
    gray and the entire array is normalized."""

    img = Image.open(imgpath).resize(dims).getdata()
    img.convert('L')
    img = subtract(array(img).flatten(), 127.5)
    return img/norm(img)


def load_data(filename):
    """Uncompress, unpickle and return the .pkl.gz file at filename."""

    return load(gz.open(filename))


def load_mini_mnist(option=None):
    """Returns the first 10\% of the images in the mnist dataset, without
    labels. Pass in 'train', 'valid' or 'test' if you want to load a specific
    subset of the dataset."""

    mmnist = load(gz.open('./data/mini_mnist.pkl.gz', 'rb'))
    if option == 'train':
        return mmnist[0]
    elif option == 'valid':
        return mmnist[1]
    elif option == 'test':
        return mmnist[2]
    else:
        return mmnist