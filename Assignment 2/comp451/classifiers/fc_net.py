from builtins import range
from builtins import object
import numpy as np

from comp451.layers import *
from comp451.layer_utils import *


class ThreeLayerNet(object):
    """
    A three-layer fully-connected neural network with Leaky ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of tuple of (H1, H2) yielding the dimension for the
    first and second hidden layer respectively, and perform classification over C classes.

    The architecture should be affine - leakyrelu - affine - leakyrelu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(self, input_dim=3*32*32, hidden_dim=(64, 32), num_classes=10,
                 weight_scale=1e-3, reg=0.0, alpha=1e-3):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: A tuple giving the size of the first and second hidden layer respectively
        - num_classes: An integer giving the number of classes to classify
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        - alpha: negative slope of Leaky ReLU layers
        """
        self.params = {}
        self.reg = reg
        self.alpha = alpha

        ############################################################################
        # TODO: Initialize the weights and biases of the three-layer net. Weights  #
        # should be initialized from a Gaussian centered at 0.0 with               #
        # standard deviation equal to weight_scale, and biases should be           #
        # initialized to zero. All weights and biases should be stored in the      #
        # dictionary self.params, with first layer weights                         #
        # and biases using the keys 'W1' and 'b1', second layer                    #
        # weights and biases using the keys 'W2' and 'b2',                         #
        # and third layer weights and biases using the keys 'W3' and 'b3.          #
        #                                                                          #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        mu, sigma = 0.0, weight_scale
        W1 = np.random.normal(mu, sigma, (input_dim, hidden_dim[0]))
        b1 = np.zeros((hidden_dim[0],))
        W2 = np.random.normal(mu, sigma, (hidden_dim[0], hidden_dim[1]))
        b2 = np.zeros((hidden_dim[1],))
        W3 = np.random.normal(mu, sigma, (hidden_dim[1], num_classes))
        b3 = np.zeros((num_classes,))

        self.params['W1'] = W1
        self.params['b1'] = b1
        self.params['W2'] = W2
        self.params['b2'] = b2
        self.params['W3'] = W3
        self.params['b3'] = b3

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################


    def loss(self, X, y=None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer net, computing the  #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        h1_out, h1_cashe = affine_lrelu_forward(X, self.params['W1'], self.params['b1'], {'alpha':self.alpha})
        h2_out, h2_cashe = affine_lrelu_forward(h1_out, self.params['W2'], self.params['b2'], {'alpha':self.alpha})
        scores, h3_cashe = affine_forward(h2_out, self.params['W3'], self.params['b3'])

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer net. Store the loss#
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        loss, dout = softmax_loss(scores, y)
        dx_3, dw_3, db_3 = affine_backward(dout, h3_cashe)
        dx_2, dw_2, db_2 = affine_lrelu_backward(dx_3, h2_cashe)
        dx_1, dw_1, db_1 = affine_lrelu_backward(dx_2, h1_cashe)

        grads['W1'] = dw_1 + self.reg * self.params['W1']
        grads['b1'] = db_1 
        grads['W2'] = dw_2 + self.reg * self.params['W2']
        grads['b2'] = db_2 
        grads['W3'] = dw_3 + self.reg * self.params['W3']
        grads['b3'] = db_3 

        loss += (self.reg * 0.5 * (np.sum(self.params['W1']*self.params['W1']) + np.sum(self.params['W2']*self.params['W2']) + np.sum(self.params['W3']*self.params['W3'])))

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    LeakyReLU nonlinearities, and a softmax loss function. This will also implement
    dropout optionally. For a network with L layers, the architecture will be

    {affine - leakyrelu - [dropout]} x (L - 1) - affine - softmax

    where dropout is optional, and the {...} block is repeated L - 1 times.

    Similar to the ThreeLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
                 dropout=1, reg=0.0, alpha=1e-2,
                 weight_scale=1e-2, dtype=np.float32, seed=None):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=1 then
          the network should not use dropout at all.
        - reg: Scalar giving L2 regularization strength.
        - alpha: negative slope of Leaky ReLU layers
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deterministic so we can gradient check the
          model.
        """
        self.use_dropout = dropout != 1
        self.reg = reg
        self.alpha = alpha
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution centered at 0 with standard       #
        # deviation equal to weight_scale. Biases should be initialized to zero.   #
        #                                                                          #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        mu, sigma = 0.0, weight_scale
        W1 = np.random.normal(mu, sigma, (input_dim, hidden_dims[0]))
        b1 = np.zeros((hidden_dims[0],))
        self.params['W1'] = W1
        self.params['b1'] = b1

        W_h = None
        b_h = None
        for i in range(self.num_layers-2):
          W_h = np.random.normal(mu, sigma, (hidden_dims[i], hidden_dims[i+1]))
          b_h = np.zeros((hidden_dims[i+1],))
          self.params['W' + str(i+2)] = W_h
          self.params['b' + str(i+2)] = b_h

        W_f = np.random.normal(mu, sigma, (hidden_dims[self.num_layers-2], num_classes))
        b_f = np.zeros((num_classes,))
        self.params['W' + str(self.num_layers)] = W_f
        self.params['b' + str(self.num_layers)] = b_f


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {'mode': 'train', 'p': dropout}
            if seed is not None:
                self.dropout_param['seed'] = seed

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as ThreeLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = 'test' if y is None else 'train'

        # Set train/test mode for dropout param since it
        # behaves differently during training and testing.
        if self.use_dropout:
            self.dropout_param['mode'] = mode
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        cashes = {}
        drop_cashes = {}
        h_out = X
        cash = None
        for i in range(self.num_layers-1):
          h_out, cash = affine_lrelu_forward(h_out, self.params['W'+str(i+1)], self.params['b' + str(i+1)], {"alpha":self.alpha})
          cashes['cash_' + str(i+1)] = cash
          if self.use_dropout:
            h_out, drop_cash = dropout_forward(h_out, self.dropout_param)
            drop_cashes['drop_' + str(i+1)] = drop_cash

        scores, cash = affine_forward(h_out, self.params['W' + str(self.num_layers)], self.params['b' + str(self.num_layers)])
        cashes['cash_' + str(self.num_layers)] = cash

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == 'test':
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        loss, dout = softmax_loss(scores, y)

        dout, dw_h, db_h = affine_backward(dout, cashes["cash_" + str(self.num_layers)])
        grads['W' + str(self.num_layers)] = dw_h + self.reg * self.params['W' + str(self.num_layers)]
        grads['b' + str(self.num_layers)] = db_h 

        for i in range(self.num_layers-1, 0, -1):
          if self.use_dropout:
            dout = dropout_backward(dout, drop_cashes["drop_" + str(i)])
          dout, dw_h, db_h = affine_lrelu_backward(dout, cashes["cash_" + str(i)])
          grads['W' + str(i)] = dw_h + self.reg * self.params['W' + str(i)]
          grads['b' + str(i)] = db_h


        reg_term = 0
        for i in range(self.num_layers):
          reg_term += np.sum(self.params['W'+str(i+1)]*self.params['W'+str(i+1)])
        loss += (self.reg * 0.5 * reg_term)
        
        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
