from numpy import array, sqrt
from nengoutils.collect import Data, save_data
from nengoutils import gen_stim_func
import itertools
import os


def run_base_batch(data_path, model, N, input_dim, eval_points, encs, f,
                   stim_func_pairs, conn_synapse, probe_synapse, t=0.5):
    #Make all parameters lists except t and model

    print 'Initializing parameters.'
    input_dim = [x**2 for x in input_dim]
    paramses = itertools.product(N, input_dim, eval_points, stim_func_pairs,
                                 conn_synapse, probe_synapse)
    for param in paramses:
        param = list(param)
        stim_pairs = param[3]
        param[3] = gen_stim_func(param[3], param[1])
        param.insert(2, encs(param[0], sqrt(param[1]), f))
        sim, probe = model(*param)
        print 'Running simulation.'
        sim.run(t)

        print 'Saving data.'
        param[4] = stim_pairs
        save_data(data_path,
                  Data(label=os.path.basename(__file__).strip('.py').strip('.pyc'),
                       params=param,
                       data=array([opt for opt in sim.data[probe]])))
        print 'Simulation finished.'

