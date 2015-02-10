from tkFileDialog import askopenfilenames
from pylab import plot, show
from data import load_data
from numpy import dot, mean, sqrt, subtract
from numpy.linalg import norm

def cos_simi(tgt, opt):
    return dot(tgt, opt)/(norm(tgt)*norm(opt))

def rmse(tgt, opt):
    return sqrt(mean(dot(subtract(tgt, opt), subtract(tgt, opt))))

queue = askopenfilenames()
if isinstance(queue, unicode):
    queue = queue.encode('ascii', 'replace').split()
data = []
for path in queue:
    data.append(load_data(path).rmses[49])
plot(data)
show()
 
