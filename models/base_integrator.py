"""Provides a nengo neural integrator model."""

import nengo


def model(n, input_dims, encs, eval_points, stim_func, conn_synapse=0.1,
          probe_synapse=0.01):
    """Initialize and build a neural integrator.

    Returns a tuple (sim, probe) where sim is the nengo.Simulator() object
    resulting from the arguments passed to the function and probe is the
    nengo.Probe() object which probes the decoded outputs of the integrator
    ensemble.

    Keyword arguments:

    n -- int, number of neurons in the ensemble.
    input_dims -- int, side length of the input image(s) (the image(s) are
        assumed
        to be square).
    encs -- array_like, encoders for the ensemble.
    eval_points -- array_like, evaluation points for the ensemble.
    stim_func -- function, a stimulus function. Should be a function that
        takes one argument, a float representing simulation time in seconds,
        and that returns the stimulus to the network at that time.
    conn_synapse -- float, PSTC (in seconds) for the recurrent connection of
        the model.
    probe_synapse: float, PSTC (in seconds) for the probe."""

    print 'Building model.'
    with nengo.Network() as net:
        
        neuron_type = nengo.LIF()        

        ipt = nengo.Node(stim_func)
        ens = nengo.Ensemble(n,
                             dimensions=input_dims,
                             encoders=encs,
                             eval_points=eval_points,
                             neuron_type=neuron_type)

        nengo.Connection(ipt, ens, synapse=None, transform=1)
        conn = nengo.Connection(ens, ens, synapse=conn_synapse)

        i_probe = nengo.Probe(ipt, attr='output',
                    synapse=None)
        o_probe = nengo.Probe(ens, attr='decoded_output',
                            synapse=probe_synapse)
    
    print 'Building simulation.'    
    return nengo.Simulator(net), i_probe, o_probe
