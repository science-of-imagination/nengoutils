from utils.collect import Data, save_data
import itertools

def run_batch(data_path, model, t=0.2, N, input_dims, eval_points, neuron_type, stim_func, conn_synapse, probe_synapse):
    #Make all parameters lists except t and model

    w = [x**2 for x in w]
    paramses = itertools.product(N, input_dims, eval_points, neuron_type, stim_func, conn_synapse, probe_synapse)
    
    for param in paramses:
        sim=model(encs[param[0]], *param)
        print 'Running simulation.'
        sim.run(t)
        print 'Connection RMSE: '+str(norm(sim.data[conn].solver_info['rmses']))
        print 'Error on the 100th frame: ' + str(rmses[98])

        print 'Simulation finished.'
        save_data(data_path, Data(label=os.path.basename(__file__).strip('.py').strip('.pyc'),
                                  params=params,          
                                  data=array([opt for opt in sim.data[probe]])))
