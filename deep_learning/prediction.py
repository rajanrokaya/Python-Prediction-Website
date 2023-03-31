from deep_learning import neural_network as nn
import numpy as np


class Prediction:
    def __init__(self, year):
        """
        :param year: class is initialized with required year for calculation
        """
        self.year = year

    def prediction_calculator(self):
        """
        --Trains the neural network for both import and export dataset.
        --The number of hidden layers, learning rate(alpha) and the iteration can be
        adjusted as per the requirement of the dataset
        --The input neuron is the dependent variable of the result
        --After training the neural network, the prediction is made for the required year
        for a given year

        :return: the prediction for the given year along with the accuracy of the model
        """
        global prediction_import, prediction_export
        difference = int(self.year) - 2021

        toatl_number_of_samples = 50
        input_neurons = 4
        squash_factor = 2000000
        alpha = 0.1
        iteration = 600000
        number_of_first_hidden_layer_neurons = 10
        number_of_second_hidden_layer_neurons = 20
        number_of_output_neurons = 1
        import_nueral_network = nn.NeuralNetwork('scraping/imports.csv', toatl_number_of_samples,
                                                 input_neurons, squash_factor,
                                                 alpha, iteration,
                                                 number_of_first_hidden_layer_neurons,
                                                 number_of_second_hidden_layer_neurons,
                                                 number_of_output_neurons)
        export_nueral_network = nn.NeuralNetwork('scraping/exports.csv', toatl_number_of_samples, input_neurons,
                                                 squash_factor,
                                                 alpha, iteration,
                                                 number_of_first_hidden_layer_neurons,
                                                 number_of_second_hidden_layer_neurons,
                                                 number_of_output_neurons)
        last_data_import = import_nueral_network.get_last_data()[1:]
        last_data_export = export_nueral_network.get_last_data()[1:]
        print(f"Training the neural network for imports data")
        print(f"--------------------------------------------")
        import_weight_and_bias = import_nueral_network.train()
        for i in range(difference):
            prediction_import = import_nueral_network.forward_propagation(last_data_import,
                                                                          import_weight_and_bias[0],
                                                                          import_weight_and_bias[1],
                                                                          import_weight_and_bias[2],
                                                                          import_weight_and_bias[3],
                                                                          import_weight_and_bias[4],
                                                                          import_weight_and_bias[5])[
                                    5] * import_nueral_network.squash_factor
            last_data_import = np.append(last_data_import[1:], prediction_import)
        print(f"Training the neural network for exports data")
        print(f"--------------------------------------------")
        export_weight_and_bias = export_nueral_network.train()
        for i in range(difference):
            prediction_export = export_nueral_network.forward_propagation(last_data_export, export_weight_and_bias[0],
                                                                          export_weight_and_bias[1],
                                                                          export_weight_and_bias[2],
                                                                          export_weight_and_bias[3],
                                                                          export_weight_and_bias[4],
                                                                          export_weight_and_bias[5])[
                                    5] * import_nueral_network.squash_factor
            last_data_export = np.append(last_data_export[1:], prediction_export)

        return int(prediction_import[0][0]), int(prediction_export[0][0]), import_nueral_network.precision, export_nueral_network.precision

