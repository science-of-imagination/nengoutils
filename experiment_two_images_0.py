from data import load_img, load_data, mk_gratings, grating
from utils.encoders import mk_bgbrs, mk_gbr_eval_pts
from numpy import array,pi,split
import numpy as np
from random import uniform
from numpy.linalg import norm

import matplotlib.pyplot as plt

from utils.batch import run_base_batch
from models.base_integrator import model
from utils.collect import save_data


dim=78

def mk_half_gratings(dim,lambd,theta,psi):
    #do it...
    #g = grating(dim,lambd,theta,psi)



    gs = split(grating(dim,lambd,theta,psi),2,1)
    return [np.append(gs[0],np.zeros((dim,dim/2)),1),np.append(np.zeros((dim,dim/2)),gs[1],1)]




#image stuff
#img=load_img('./data/lena_512x512.png',(dim, dim))
#img=img/norm(img)

grating = mk_half_gratings(dim,2**-1,2*pi/3,uniform(0,2*pi))
img1 = grating[0]
img1 = array(img1)
img1 = img1.flatten()
img1 = img1/norm(img1)
img2 = grating[1]
img2 = array(img2)
img2 = img2.flatten()
img2 = img2/norm(img2)

def stim_func(t):
    if t < 0.1:
        return img1
    elif t > 0.1 and t < 0.2:
        return img2
    else:
        return [0 for _ in range(len(img1))]


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

kwargs = {'N':[5000],
          'input_dim':[dim],
          'eval_points':[eval_points],
          'encs':Enc(),
          'f':4,
          'stim_func':[stim_func],
          'conn_synapse':[0.1],
          'probe_synapse':[0.01]}

if __name__ == '__main__':
    datalist = run_base_batch('./', model, **kwargs)
    for data in datalist:
        del data.params
        data.dims = (dim, dim)
        save_data('./', data)

