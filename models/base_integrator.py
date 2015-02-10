import nengo


def model(N, input_dims, encs, eval_points, stim_func, conn_synapse=0.1, probe_synapse=0.01):

    print 'Building model.'
    with nengo.Network() as net:
        
        neuron_type = nengo.LIF()        

        ipt = nengo.Node(stim_func)
        ens = nengo.Ensemble(N,
                             dimensions=input_dims,
                             encoders=encs,
                             eval_points=eval_points,
                             neuron_type=neuron_type)

        nengo.Connection(ipt, ens, synapse=None, transform=1)
        conn = nengo.Connection(ens, ens, synapse=conn_synapse)

        probe = nengo.Probe(ens, attr='decoded_output',
                            synapse=probe_synapse)
    
    print 'Building simulation.'    
    return nengo.Simulator(net), probe