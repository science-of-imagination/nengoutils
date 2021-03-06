'''Encoders for SOIL Nengo. Features only gabor filters for now.'''

from numpy import array, linspace, meshgrid, cos, sin, exp, pi, identity, log
from numpy.linalg import norm
from random import uniform, choice
import warnings


def pixel_encoders(canvas_size):
    """Return a set of encoders for a square image of side length canvas_size
    that are each sensitive to one pixel of the image. Individual encoders are
    flattened and normalized arrays."""
    return identity(canvas_size**2)


def gabor(canvas_size, lambd, theta, psi, sigma, gamma, x_offset, y_offset):
    '''Returns a single gabor filter.
    '''
    x = linspace(-1, 1, canvas_size)
    y = linspace(-1, 1, canvas_size)
    X, Y = meshgrid(x, y)
    X = X - x_offset
    Y = Y + y_offset

    cosTheta = cos(theta)
    sinTheta = sin(theta)
    xTheta = X * cosTheta  + Y * sinTheta
    yTheta = -X * sinTheta + Y * cosTheta
    e = exp( -(xTheta**2 + yTheta**2 * gamma**2) / (2 * sigma**2) )
    cosed = cos((2 * pi * xTheta / lambd) + psi)
    return e * cosed


def make_random_gabor(canvas_size):
    '''Returns a gabor filter with random size, frequency and orientation. The
    returned filter will be placed within the circle inscribed in a square
    canvas of side length canvas_size px. Gabors are more likely to be near the
    center of the canvas than near the edges.
    '''
    
    th = uniform(0, 2*pi)
    r = uniform(2.0/canvas_size,1.4)
    return gabor(canvas_size,
                 lambd=uniform(2.0/canvas_size, 1),
                 theta=uniform(0, 2*pi),
                 psi=uniform(0, 2*pi),
                 sigma=log(0.1*r+1),
                 gamma=0.24,#uniform(0.07, 1),
                 x_offset=r*cos(th),
                 y_offset=r*sin(th))


def normalized_random_gabor_encoders(canvas_size, array_size):
    '''Return an array of random gabor filters placed on a square canvas
    of side length canvas_size px.
    '''
    gabors = [make_random_gabor(canvas_size).flatten()
              for i in range(array_size)]
    #normalize gabors and return
    return array([(1/norm(i).flatten())*i for i in gabors])

from numpy import array, zeros, tile, sqrt, cos, sin, log, pi, exp, linspace, meshgrid
from numpy.linalg import norm
from random import uniform, choice



def mk_mesh(dims, x_offset, y_offset):
    '''Create a mesh to represent the space from which information is
    available to an encoder.'''

    x = linspace(-1, 1, dims[0])
    y = linspace(-1, 1, dims[1])
    X, Y = meshgrid(x, y)
    X = X - x_offset
    return X - x_offset, Y + y_offset


def rotate_mesh(theta, mesh):
    '''Rotate the mesh by theta, for asymmetric encoders--where orientation
    matters.'''
    return (mesh[0]*cos(theta)+mesh[1]*sin(theta),
            -mesh[0]*sin(theta)+mesh[1]*cos(theta))

def bio_gbr(dims, x_off, y_off, theta, f, phi, psi=0):
    '''Returns a quadrature pair of biologically inspired gabor placed on
    a pixel canvas of dimensions dims. (Short axis of envelope is aligned
    with the axis along which the waves travel;
    |long axis of envelope| = 2*|short axis of envelope|.)

    Note: Square canvas suggested.

    x_offset: position of the center of gabor along the x-axis of the image

    y_offset: position of the center of gabor along the y-axis of the image

    WARNING: x_offset, y_offset must be in [-1,1]

    theta: orientation of the gabor

    f: main frequency of gabor in Hz/canvas_length

    phi: Half-amplitude spatial frequency bandwidth of gabor.

    psi: phase of the gabor.'''

    #Compute kappa, sigma
    kappa = sqrt(2*log(2))*(2.0**phi+1)/(2.0**phi-1)
    sigma = kappa/(2*pi*f)
    #The linspace is (-1,1)x(-1,1), want f=1 to be 1 cycle per width
    f = f/float(2)
    
    #Change of basis, centered on center of gbr, rotated to align with the
    # direction of wave propagation
    X, Y = rotate_mesh(theta, mk_mesh(dims, x_off, y_off))

    #Compute parts of the gabor
    envelope = (sqrt(2*pi)/sigma)*exp(-(pi/(2*sigma))*(4*(X**2) + Y**2))
    re = cos(2*pi*f*X+psi)-exp(-kappa**2/2.0)
    im = sin(2*pi*f*X+psi)

    return envelope*re, envelope*im


#Lee (1996) says that neuro evidence points at 1.5 octaves for phi, and 2-3
# voices per octave. That the system looks at 3-5 octaves. That observations
# yield around 20 different directions represented.
# All this is implemented below.

def mk_bgbrs(n_pairs,
             dims,
             F_max,
             octaves=5,
             N=3,
             x_off=lambda:uniform(-0.5,0.5),
             y_off=lambda:uniform(-1,1),
             theta=lambda:choice([2*pi*i/20 for i in range(20)]),
             phi=1.5,
             psi=lambda:uniform(0,2*pi)):

    n_steps = octaves*N
    Fs = []
    for i in range(octaves*N):
        Fs.append((2**(-i/float(N)))*F_max)

    #determine sampling weights
    k= sqrt(2.0*log(2))*(2**phi+1)/(2**phi-1)
    alpha = k/(2*pi)
    p=[]
    for i in range(octaves*N):
        p.append(1/(alpha*2**(2*(i/float(N))+4)))
    proportions = array(p)/norm(array(p))


    #f_ch = lambda:choice(Fs) #original coice function
    f_ch = lambda:Fs[weighted_choice(proportions)]

    gbrs = []
    rng = range(n_pairs)
    for i in rng:
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            try:
                nxt = bio_gbr(dims, x_off(),  y_off(), theta(), f_ch(), phi, psi())
                #normalize and flatten
                g1, g2 = nxt[0].flatten(), nxt[1].flatten()
                g1, g2 = g1/norm(g1), g2/norm(g2)            
                gbrs.append(g1)
                gbrs.append(g2)
            except RuntimeWarning:
                rng.append(rng[-1]+1)
                print 'Warning Occured: (1)'
    return gbrs


def gbr_eval_pt(width):
    #Does not come in quadrature pairs.
    return gabor(width,
                 lambd=uniform(sqrt(8)/width, 1),
                 theta=uniform(0, 2*pi),
                 psi=uniform(0, 2*pi),
                 sigma=uniform(0,1),
                 gamma=uniform(0,1),
                 x_offset=uniform(-1,1),
                 y_offset=uniform(-1,1))


def mk_gbr_eval_pts(N, width):
    eval_pts = []
    rng =  range(N)
    for i in rng:
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            try:
                j = gbr_eval_pt(width).flatten()
                j = j/norm(j)
                eval_pts.append(j)
            except RuntimeWarning:
                rng.append(rng[-1]+1)
                print 'Warning Occured: (2)'
    return array(eval_pts)

import random

def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i