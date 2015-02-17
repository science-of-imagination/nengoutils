"""This module provides tools for analyzing data.

Provides:
cosine -- Computes the cosine of the angle between two vectors.
rmsd -- Computes the root mean square of the difference of two vectors.
"""
from tkFileDialog import askopenfilenames
from pylab import plot, show
from data import load_data
from numpy import dot, mean, sqrt, subtract
from numpy.linalg import norm

def cosine(u, v):
    """Compute and return the cosine of the angle between the vectors u, v.

    Note: Computes the ratio of the dot product of the two vectors to the
    product of the norms of the two vectors (<tgt, opt>/(|tgt||opt|)).

    Keyword arguments:
    u -- array_like, the first vector.
    v -- array_like, the second vector."""

    return dot(u, v)/(norm(u)*norm(v))

def rmsd(u, v):
    """Return the root mean square of the difference between vectors u, v.

    Keyword arguments:
    u -- array_like, the first vector.
    v -- array_like, the second vector."""

    d = subtract(u, v)
    return sqrt(mean(dot(d, d)))

#queue = askopenfilenames()
#if isinstance(queue, unicode):
#    queue = queue.encode('ascii', 'replace').split()
#data = []
#for path in queue:
#    data.append(load_data(path).rmses[49])
#plot(data)
#show()
 
