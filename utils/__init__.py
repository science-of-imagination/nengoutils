"""Module that provides general modeling utilities.

Provides:

Sub-modules:
analyze -- tools for analyzing data.
collect -- tools for collecting data.
visualize -- tools for visualizing data.

Functions and classes:
SVDCompressor -- class, Compresses a set of vectors based on a seed."""

from scipy.sparse.linalg import svds
from numpy import dot

def gen_stim_func(pairlst, ln_img):
    """Creates a stimulus function from a list of time-vector pairs
    
    pairlst -- array_like, a list of the time limits and corresponding vectors
               in (limit, vector) pairs
    limit -- numeric, time at which the input should switch
    vector -- array_like, input vector
    ln_img -- numeric, length of input image
    
    If the time exceeds the last limit, the function will output a zero vector
    
    """
    def stim_func(t):
        """The stimulus function

        t -- float, simulation time
        
        """
        loc_pairlst=pairlst
        loc_ln_img=ln_img
        index=0
        ln_pairlst=len(pairlst)
        while index<ln_pairlst:
            if t<loc_pairlst[index][0]:
                t=yield loc_pairlst[index][1]
            else:
                index+=1
        while True:
            t=yield [0 for _ in range(loc_ln_img)]
    stim_func=stim_func(0)
    stim_func.next()
    return stim_func.send

class SVDCompressor:
    """Compresses and decompresses vectors using SVD."""

    def __init__(self, seed, n=600):
        """Initialize an SVDCompressor object.

        Computes an SVD compression basis based on seed and n.

        Keyword arguments:
        seed -- array_like, the matrix whose SVD will provide the basis vectors
            for compression.
        n -- int (default=600), number of """

        self.basis, S, V = svds(seed.T, k=n)

    def compress(self, original):
        """Compress original.

        Keyword arguments:
        original -- array_like, a vector or matrix to be compressed using the
            encoding computed at initialization."""

        return dot(original, self.basis)

    def compress_many(self, originals):
        """Compress the contents of originals.

        Keyword arguments:
        originals -- iterable, a collection of vectors or matrices to be
            compressed using the encoding computed at initialization."""

        return map(self.compress, originals)

    def decompress(self, compressed):
        """Decompress compressed.

        Keyword arguments:
        compressed -- array_like, a vector or matrix to be decompressed using
            the encoding computed at initialization."""

        return dot(self.basis, compressed.T).T

    def decompress_many(self, compresseds):
        """Decompress the contents of compresseds.

        Keyword arguments:
        compresseds -- iterable, a collection of vectors or matrices to be
            decompressed using the encoding computed at initialization."""

        return map(self.decompress, compresseds)