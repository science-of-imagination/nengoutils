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