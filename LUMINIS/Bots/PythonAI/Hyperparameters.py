import numpy as np
import pickle

layer_dims = [75, 30, 10, 5]
def initialize_parameters_deep(layer_dims):
    """
    Arguments:
    layer_dims -- python array (list) containing the dimensions of each layer in our network
    
    Returns:
    parameters -- python dictionary containing your parameters "W1", "b1", ..., "WL", "bL":
                    Wl -- weight matrix of shape (layer_dims[l], layer_dims[l-1])
                    bl -- bias vector of shape (layer_dims[l], 1)
    """
    parameters = {}
    L = len(layer_dims)            # number of layers in the networ
    for l in range(1, L):
    	parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * 0.01
    	parameters['b' + str(l)] = np.zeros((layer_dims[l], 1))
    	assert(parameters['W' + str(l)].shape == (layer_dims[l], layer_dims[l-1]))
    	assert(parameters['b' + str(l)].shape == (layer_dims[l], 1))
    return parameters

parameters = initialize_parameters_deep(layer_dims)

with open("parameters.pkl", "wb") as output_file:
	pickle.dump(parameters, output_file)

with open("layer_dims.pkl", "wb") as output_file:
	pickle.dump(layer_dims, output_file)