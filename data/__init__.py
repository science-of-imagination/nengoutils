"""This module provides functions for loading modeling data.

Provides:
mk_gratings -- Generate a set of experimental stimulus gratings.
grating -- Create a single stimulus grating.
load_img -- Load a stimulus image.
load_data -- Load compressed data.
load_mini_mnist -- Load a portion of the mnist dataset."""

import gzip as gz
from cPickle import load, dump
from PIL import Image
from numpy import array, subtract, meshgrid, linspace, cos, sin, pi
from numpy.random import uniform
from numpy.linalg import norm


def mk_gratings(canvas_size,filename):
    """Create and save a set of stimulus gratings.

    Creates stimulus gratings for a square canvas.

    Creates one grating at each of the following frequencies (in cycles per
    width):
    2**3, 2**2, 2, 1, 2**-1, 2**-2, 2**-3.

    And in each of the following orientations:
    0, 2*pi/3, 4*pi/3.

    Output is a .pkl.gz (see load_data). The pickle contains a list of
    sub-lists. Each sub-list is a pair [params, grating] where params are the
    parameters used to create the grating and grating is an array representing
    the grating in raster format.

    Keyword arguments:
    canvas_size -- int, size (in px) of a side of the canvas.
    filename -- str, path to which output should be saved."""

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
    """Create and return a stimulus grating.

    Keyword arguments:
    canvas_size -- int, size (in px) of a side of the canvas.
    lambd -- float, grating frequency in cycles per canvas width.
    theta -- float, orientation of the gradient (in rad).
    psi -- float, phase of the gradient (in rad)."""

    x = linspace(-1, 1, canvas_size)
    y = linspace(-1, 1, canvas_size)
    X, Y = meshgrid(x, y)


    cosTheta = cos(theta)
    sinTheta = sin(theta)
    xTheta = X * cosTheta  + Y * sinTheta
    yTheta = -X * sinTheta + Y * cosTheta
    
    cosed = cos((2 * pi * xTheta / lambd) + psi)
    return cosed


def load_img(path, dims):
    """Load the image at path and return an array representing the raster.

    Flattens image. Shifts pixel activations such that 0 represents gray,
    normalizes the output array.

    Keyword arguments:
    path -- str, path of the image to be loaded.
    dims -- (w, h), where w,h are ints indicating dimensions of the image (in
        px)."""

    img = Image.open(path).resize(dims).getdata()
    img.convert('L')
    img = subtract(array(img).flatten(), 127.5)
    return img/norm(img)


def load_data(filename):
    """Uncompress, unpickle and return a .pkl.gz file.

    Keyword arguments:
    filename -- str, a valid file path"""

    return load(gz.open(filename))


def load_mini_mnist(option=None):
    """Load and return the first \%10 of the images in the mnist dataset.

    Does not return labels. Pass in 'train', 'valid' or 'test' if you want to
    load a specific subset of the dataset.

    Keyword arguments:
    option -- str (default=None)."""

    mini_mnist = load(gz.open('./data/mini_mnist.pkl.gz', 'rb'))
    if option == 'train':
        return mini_mnist[0]
    elif option == 'valid':
        return mini_mnist[1]
    elif option == 'test':
        return mini_mnist[2]
    else:
        return mini_mnist