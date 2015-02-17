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
        """

        Keyword arguments:
        seed -- array_like, the matrix whose SVD will provide the basis vectors
            for compression.
        n -- int (default=600), number of """

        # The basis is U.
        self.basis, S, V = svds(seed.T, k=n)

    def _compress(self, original):
        return dot(original, self.basis)

    def compress(self, originals):
        """Compress the contents of targets.

        Keyword arguments:
        originals -- iterable, a collection of vectors or matrices to be
            compressed using the encoding computed at initialization."""

        return map(self._compress, originals)

    def _decompress(self, compressed):
        return dot(self.basis, compressed.T).T

    def decompress(self, compresseds):
        """Decompress the contents of compresseds.

        Keyword arguments:
        compresseds -- iterable, a collection of vectors or matrices to be
            decompressed using the encoding computed at initialization."""

        return map(self._decompress, compresseds)