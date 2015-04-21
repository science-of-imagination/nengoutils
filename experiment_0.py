from data import load_img
from utils.encoders import mk_bgbrs, mk_gbr_eval_pts
from numpy import array

from utils.batch import run_base_batch
from models.base_integrator import model


# dimensions of the sides of the simulation canvas.
dim = 78


# initialize image.
img = load_img('./data/lena_512x512.png', (dim, dim))


# a stimulus function.
def stim_func(t):

    if t < 0.1:
        return img
    else:
        return [0 for _ in range(len(img))]


class Enc:
    """A class that generates encoders for every simulation run, or one for
    each level, depending on the experiment."""

    def __init__(self, new_every=True):
        """Initialize an Enc object.

        Keyword arguments:
        new_every -- bool (default=True), determines if new encoders will
            be generated at every call to self. """

        self.new_every = new_every
        self.encs = None

    def __call__(self, n, dim, f):
        """Return an array of encoders.

        If self.new_every is True returns a new set every time self is called.
        Otherwise, returns the same set every time.

        Keyword arguments:
        n -- int, number of encoders in the set to be returned.
        dim -- int, length of the sides of the image canvas the encoders
            will be probing.
        f -- float, frequency of the encoders to be constructed."""

        if (not self.new_every and self.encs is None) or self.new_every:
            self.encs = array(mk_bgbrs(n/2, (dim, dim), f))
        return self.encs


print 'Initializing eval points.'
eval_points = mk_gbr_eval_pts(100, dim)


kwargs = {'N': [1000],
          'input_dim': [dim],
          'eval_points': [eval_points],
          'encs': Enc(),
          'f': 4,
          'stim_func': [stim_func],
          'conn_synapse': [0.1],
          'probe_synapse': [0.01]}


if __name__ == '__main__':
    run_base_batch('./', model, **kwargs)
