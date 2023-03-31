import numpy as np


class NeuralNetwork:

    def create_array(self):
        """
        This function is used to create an array from the data file
        :param : none
        :return arr: numpy array of data
        """

        arr = np.empty((len(self.data), 5))
        for i, line in enumerate(self.data):
            items = line.split(';')[0:5]
            arr[i] = items
        return arr

    def __init__(self, data_file, train_sample, input_neuron, squash_factor, alpha, iteration,
                 first_hidden_layer_neurons, second_hidden_layer_neurons, output_neuron):
        """
         param
                data_file       : csv file
                train_sample    : number of training data
                input_neuron    : number of input neurons
                squash_factor   : squash factor for converting data to 0-1 range
                alpha           : learning rate
                iteration       : number of iteration for training
                first_hidden_layer_neurons  : number of neurons in first hidden layer
                second_hidden_layer_neurons : number of neurons in second hidden layer
                output_neuron               : number of output neurons
        """
        try:
            with open(data_file, 'r') as file:
                self.data = file.read()
                self.data = self.data.split('\n')
        except FileNotFoundError:
            print(f"File not found")
            exit(0)
        self.precision = 0
        self.data = np.array(self.data)
        self.data = self.create_array()
        self.train_sample = train_sample
        self.squash_factor = squash_factor
        self.iteration = iteration
        self.alpha = alpha
        self.number_of_first_hidden_layer_neurons = first_hidden_layer_neurons
        self.number_of_second_hidden_layer_neurons = second_hidden_layer_neurons
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.training_data = self.data[0:self.train_sample]
        self.training_data_input = self.training_data[:, 0:self.input_neuron]
        self.training_data_input = self.squash_data(self.training_data_input)
        self.training_data_output = self.training_data[:, self.input_neuron]
        self.training_data_output = self.squash_output(self.training_data_output)
        self.test_data = self.data[self.train_sample:]
        self.test_data_input = self.test_data[:, 0:self.input_neuron]
        self.test_data_input = self.squash_data(self.test_data_input)
        self.test_data_output = self.test_data[:, self.input_neuron]
        self.test_data_output = self.squash_output(self.test_data_output)
        self.W1, self.b1, self.W2, self.b2, self.W3, self.b3 = self.init_params()

    def squash_data(self, data):
        """
        squashing the input data to 0-1 range
        :param: array of data
        :return :
                data: arrays of squashed data in range of 0 to 1
        """
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                data[i][j] = int(data[i][j]) / self.squash_factor
        return data

    def reverse_squash_data(self, data):
        """
        :param: array of data
        :return :
                data: arrays of original data
        """
        for i in range(0, len(data)):
            for j in range(0, 1):
                data[i] = data[i] * self.squash_factor
        return data

    def squash_output(self, output):
        """
            :param: array of data
            :return :
                data: arrays of squashed output in range of 0 to 1
            """
        for i in range(0, len(output)):
            output[i] = int(output[i]) / self.squash_factor
        return output

    def sigmoid(self, x):
        """
            sigmoid activation function for converting the output to a value between 0 and 1
                :return:
                    data in range of 0 to 1
            """
        return 1 / (1 + np.exp(-x))

    def d_sigmoid(self, x):
        """
            derivative of sigmoid function
                :param:
                        x: input
                :return:
                        derivative of sigmoid function
            """
        return x * (1 - x)

    def init_params(self):
        """
            Initializing the weights and biases
            The weights and biases are in the range of -1 to 1
                :params : None
                :return :
                          w1:  weights for the first layer
                          w2:  weights for the second layer
                          w3:  weights for the third layer
                          b1:  biases for the first layer
                          b2:  biases for the second layer
                          b3:  biases for the third layer
            """
        w1 = 2 * np.random.random((self.number_of_first_hidden_layer_neurons, self.input_neuron)) - 1
        b1 = 2 * np.random.random((1, self.number_of_first_hidden_layer_neurons)) - 1
        w2 = 2 * np.random.random(
            (self.number_of_second_hidden_layer_neurons, self.number_of_first_hidden_layer_neurons)) - 1
        b2 = 2 * np.random.random((1, self.number_of_second_hidden_layer_neurons)) - 1
        w3 = 2 * np.random.random((self.output_neuron, self.number_of_second_hidden_layer_neurons)) - 1
        b3 = 2 * np.random.random((1, self.output_neuron)) - 1
        return w1, b1, w2, b2, w3, b3

    def forward_propagation(self, input_neuron, w1, w2, w3, b1, b2, b3):
        """
                calculating the output of the neural network for the given input given the weights and biases
                :params :
                        input   :  input data
                        W1      :     weights for the first layer
                        W2      :     weights for the second layer
                        W3      :     weights for the third layer
                        b1      :     biases for the first layer
                        b2      :     biases for the second layer
                        b3      :     biases for the third layer
                :return :
                        z1      :    output of the first layer
                        a1      :    applying sigmoid activation function to z1
                        z2      :    output of the second layer
                        a2      :    applying sigmoid activation function to z2
                        z3      :    output of the third layer
                        a3      :    final output of the neural network (predicted value)
            """
        z1 = np.dot(input_neuron, w1.T) + b1
        a1 = self.sigmoid(z1)
        z2 = np.dot(a1, w2.T) + b2
        a2 = self.sigmoid(z2)
        z3 = np.dot(a2, w3.T) + b3
        a3 = self.sigmoid(z3)
        return z1, a1, z2, a2, z3, a3

    def backward_propagation(self, output, a1, a2, w2, a3, w3):
        """
             backward propagation for calculating the gradients descent of the function
                :param:
                    output  :     actual value of the output
                    A1      :         output of the first layer
                    A2      :         output of the second layer
                    A3      :         output of the third layer
                    W2      :         weights for the second layer
                    W3      :         weights for the third layer
                :return:
                    a2_error:   error in the output of the second layer
                    a1_error:   error in the output of the first layer
                    dA      :   derivative of the weight with respect to the error
                    db      :   derivative of the biases
            """
        output = output.reshape(output.size, 1)
        a3_error = output - a3
        d_a3 = a3_error * self.d_sigmoid(a3)
        db3 = np.sum(d_a3, axis=0, keepdims=True)
        a2_error = d_a3.dot(w3)
        d_a2 = a2_error * self.d_sigmoid(a2)
        db2 = np.sum(d_a2, axis=0, keepdims=True)
        a1_error = d_a2.dot(w2)
        d_a1 = a1_error * self.d_sigmoid(a1)
        db1 = np.sum(d_a1, axis=0, keepdims=True)
        return a2_error, d_a2, a1_error, d_a1, db1, db2, a3_error, d_a3, db3

    def update_weights(self, input_neuron, a1, da2, da1, w1, w2, b1, b2, db1, db2, a2, da3, w3, b3, db3, alpha):
        """
                updating the weights and biases of the model after back propagation

                :param:
                        input   :   input data
                        A       :   output of the layer
                        dA      :   derivative of the weight with respect to the error
                        db      :   derivative of the biases
                        W       :   weights for the layer
                        b       :   biases for the layer
                        alpha   :   learning rate
                :return:
                        W       :   updated weights for the layer
                        b       :   updated biases for the layer
            """
        w3 += alpha * a2.T.dot(da3).T
        b3 += alpha * db3
        w2 += alpha * a1.T.dot(da2).T
        b2 += alpha * db2
        w1 += alpha * input_neuron.T.dot(da1).T
        b1 += alpha * db1
        return w1, w2, w3, b1, b2, b3

    def accuracy(self, output_test, output_prediction):
        """ params
                    output_test      : output of test data
                    output_prediction: predicted output of the given data
            :return
                    accuracy       : accuracy of the model
        """
        total_error = 0
        for i in range(0, len(output_test)):
            total_error_temp = (output_test[i] - output_prediction[0][i]) / output_test[i]
            if total_error_temp < 0:
                total_error_temp = total_error_temp * -1
            total_error += total_error_temp
        return 1 - total_error / len(output_test)

    def train(self):
        """
            Training the model with the given input and output data along with the number of epochs and learning rate
            params : none
            :return :
                    Weights and biases of the model
            """
        for i in range(self.iteration + 1):
            z1, a1, z2, a2, z3, a3 = self.forward_propagation(self.training_data_input, self.W1, self.W2, self.W3,
                                                              self.b1,
                                                              self.b2, self.b3)
            a2_error, d_a2, a1_error, d_a1, db1, db2, a3_error, d_a3, db3 = self.backward_propagation(
                self.training_data_output, a1, a2, self.W2,
                a3, self.W3)
            self.W1, self.W2, self.W3, self.b1, self.b2, self.b3 = self.update_weights(self.training_data_input, a1,
                                                                                       d_a2, d_a1, self.W1, self.W2,
                                                                                       self.b1, self.b2, db1,
                                                                                       db2, a2, d_a3, self.W3, self.b3,
                                                                                       db3,
                                                                                       self.alpha)

            if i % 20000 == 0:
                test = a3
                self.precision = self.accuracy(self.training_data_output, test.T) * 100
                print(f"Epoch: {i} Accuracy on train: {self.accuracy(self.training_data_output, test.T) * 100}%")
        return self.W1, self.W2, self.W3, self.b1, self.b2, self.b3

    def test(self):
        """
           Testing the remaining untrained data
           :params : none
           :return : none
           """
        z1, a1, z2, a2, z3, a3 = self.forward_propagation(self.test_data_input, self.W1, self.W2, self.W3, self.b1,
                                                          self.b2, self.b3)
        print(f"Accuracy on test: {self.accuracy(self.test_data_output, a3.T) * 100}%")

    def get_last_data(self):
        """
           Getting the last data of the dataset
           :params : none
           :return : none
           """
        return self.data[-1] * self.squash_factor