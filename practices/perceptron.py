import numpy as np

class Perceptron:

    def __init__(self, learning_rate=0.01, n_iterations=10000):
        self.lr = learning_rate
        self.ni = n_iterations
        self.activation_function = _unit_step_function
        self.weigths = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # hyperparameters
        self.weights = np.zeros(n_features)
        self.bias = 0

        y_ = [1 if i > 0 else 0 for i in y]

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self.activation_function(linear_output)
        return y_predicted

    def _unit_step_function(self, x):
        # return 1 if x >= 0 else 0
        return np.where(x >= 0, 1, 0)
    