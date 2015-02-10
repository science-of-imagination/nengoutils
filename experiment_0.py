from data import load_img
from utils.encoders import mk_bgbrs, mk_gbr_eval_pts
from numpy import array
from numpy.linalg import norm
from scipy.misc import lena

from models.run_integrator_batch import run_batch
from models.base_integrator import model



dim=78

#image stuff
img=load_img('./data/lena_512x512.png',(dim, dim))
#img=img/norm(img)

def stim_func(t):
    if t < 0.1:
        return img
    else:
        return [0 for _ in range(len(img))]


class Enc:
    def __init__(self, new_every=True):
        self.new_every = new_every
        self.encs = None

    def __call__(self, N, dim, f):
        if (not self.new_every and self.encs==None) or self.new_every:
            self.encs = array(mk_bgbrs(N/2, (dim,dim), f))
        return self.encs

print 'Initializing eval points.'
eval_points = mk_gbr_eval_pts(500, dim)

kwargs = {'N':[2000],
          'input_dim':[dim],
          'eval_points':[eval_points],
          'encs':Enc(),
          'f':4,
          'stim_func':[stim_func],
          'conn_synapse':[0.1],
          'probe_synapse':[0.01]}

if __name__=='__main__':
    run_batch('./', model, **kwargs)
