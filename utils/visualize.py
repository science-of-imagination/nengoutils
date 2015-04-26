"""This module provides utilities for displaying data.

Provides:
mk_imgs -- Creates and saves an image for each data point in a
    utils.collect.Data object."""


import os
import matplotlib.pyplot as plt
from analyze import cosines
from numpy import linspace, reshape, array
from matplotlib.pyplot import imsave

LINESTYLES=['o', '^', 's', '*', '+', 'x', 'd', 'p', 'h', 'v']

def mk_imgs(path, data):
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
    for i in range(len(data.data)):
        name = path+'%03d.png' % (i+1)
        img = reshape(data.data[i], data.dims, 'F')
        imsave(name, img.T, cmap='gray')
        print 'Saved img %d of %d' % (i+1, len(data.data))
    print 'Done.'

def mk_cosgraphs(path, fname, xvals, xvalsname, xinterval, xticks, yticks, 
                 imgvec, *Data):
    if not os.path.exists(path):
        os.makedirs(path)
    xvals=[n for n in xvals if n%xinterval==0]
    lblcos=[(d.params[0], cosines([n for i, n in enumerate(d.data) 
                                   if i%xinterval==0], imgvec)) 
            for d in Data]
    intensities=linspace(0.0, 0.9, len(lblcos))
    fig=plt.figure(1)
    ax=fig.add_subplot(111)
    for i, vals in enumerate(lblcos):
        label, cos=vals
        ax.plot(xvals, cos, color=str(intensities[i]), 
                label=str(label), ls='-', marker=LINESTYLES[i])
    if xticks!=None:
        ax.xaxis.set_ticks(xticks)
    if yticks!=None:
        ax.yaxis.set_ticks(yticks)
    handles, labels=ax.get_legend_handles_labels()
    lgd=ax.legend(handles, labels, loc=6, bbox_to_anchor=(1.01, 0.5))
    plt.xlabel(xvalsname, fontsize=20)
    plt.ylabel('Cosine Similarity', fontsize=20)
    plt.savefig(os.path.join(path, fname), bbox_extra_artists=(lgd,),
                bbox_inches='tight')

def test():
    from data import load_data, load_img
    d=load_data('2015042615490000_batch.pkl.gz')
    d2=load_data('2015042615490000_batch.pkl.gz')
    d2.data=array(d2.data)+20.
    img=load_img('./data/lena_512x512.png', (78,78)).reshape(78**2)
    mk_cosgraphs('.', 'graph.jpg', range(500), 'Time (ms)', 50, 
                 range(0, 501, 50), None, img, d, d2)
    
    