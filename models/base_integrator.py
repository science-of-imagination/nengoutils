import nengo


def model(N, input_dims, encs, eval_points, stim_func, conn_synapse=0.1,
          probe_synapse=0.01):
    """Initialize and build a neural integrator. Returns a tuple (sim, probe)
    where sim is the nengo.Simulator() object resulting from the arguments
    passed to the function and probe is the nengo.Probe() object which probes
    the decoded outputs of the integrator ensemble.

    Parameters:

    N: Number of neurons in the ensemble.

    input_dims: Side length of the input image(s) (the image is assumed to be
        square).

    encs: Encoders for the ensemble.

    eval_points: Evaluation points for the ensemble.

    stim_func: A stimulus function. Should be a function that takes one
        argument, a float representing simulation time in seconds, and that
        returns the stimulus to the network at that time.

    conn_synapse: PSTC (in seconds) for the recurrent connection of the
        ensemble.

    probe_synapse: PSTC (in seconds) for the probe."""

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
