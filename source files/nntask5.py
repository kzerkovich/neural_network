import argparse
import math
import os
import numpy as np


def log(error):
    log_file = open("Log.txt", "w", encoding="utf-8")
    log_file.write(error)


def load_matrix(matrix_file):
    if not os.path.isfile(matrix_file):
        log(f"Файл {matrix_file} не существует")
        exit()

    matrix = []
    try:
        with open(matrix_file, 'r') as f:
            for line in f:
                lines = []
                elements = line.strip().split('] [')
                for element in elements:
                    lines.append([float(x) for x in element.strip("[]").split()])
                matrix.append(lines)
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()
    return matrix


def load_vector(vector_file):
    if not os.path.isfile(vector_file):
        log(f"Файл {vector_file} не существует")
        exit()

    try:
        xArray = []
        yArray = []
        with open(vector_file, 'r') as f:
            for line in f:
                res = line.strip("[]\n").split("] [")
                xArray.append([float(x) for x in res[0].split()])
                yArray.append([float(y) for y in res[1].split()])
            return xArray, yArray
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def mean_squared_error(act, pred):
    pred = np.asarray(pred)
    act = np.asarray(act)
    diff = pred - act
    differences_squared = diff ** 2
    mean_diff = sum(0.5 * differences_squared)

    return mean_diff

class Neuron:
    def __init__(self, weights):
        self.weights = weights
        self.activation_function = sigmoid
        self.activation_derivative = sigmoid_derivative
        self.output = None

    def activate(self, inputs):
        z = 0
        for i in range(len(inputs)):
            z += self.weights[i] * inputs[i]
        self.output = self.activation_function(z)
        return self.output


class Layer:
    def __init__(self, neurons):
        self.neurons = neurons
        self.output = None
        self.error = None
        self.delta = None

    def forward(self, inputs):
        self.output = [neuron.activate(inputs) for neuron in self.neurons]
        return self.output


class Network:
    def __init__(self, layers):
        self.layers = layers

    def forward(self, X):
        for layer in self.layers:
            X = layer.forward(X)
        return X

    def backward(self, X, y, learning_rate):
        output = self.forward(X)

        error = [y[0] - output[0]]
        self.layers[-1].error = error
        self.layers[-1].delta = [error[0] * self.layers[-1].neurons[0].activation_derivative(output[0])]

        for i in reversed(range(len(self.layers) - 1)):
            layer = self.layers[i]
            next_layer = self.layers[i + 1]
            layer.error = [0] * len(layer.neurons)
            for j, neuron in enumerate(next_layer.neurons):
                for k, weight in enumerate(neuron.weights):
                    layer.error[k] += next_layer.delta[j] * weight

            layer.delta = [
                layer.error[j] * neuron.activation_derivative(neuron.output)
                for j, neuron in enumerate(layer.neurons)
            ]

        for i in range(len(self.layers)):
            layer = self.layers[i]
            inputs = X if i == 0 else self.layers[i - 1].output
            for j, neuron in enumerate(layer.neurons):
                for k in range(len(neuron.weights)):
                    neuron.weights[k] += learning_rate * layer.delta[j] * inputs[k]

        return error

    def learning(self, X, y, learning_rate, epochs):
        errors = []
        for epoch in range(epochs):
            cur_error = []
            for xi, yi in zip(X, y):
                cur_error.append(self.backward(xi, yi, learning_rate))
            errors.append(mean_squared_error(cur_error, y))

        return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nntask5.exe",
        description="Creating a directed graph")
    parser.add_argument("-input1", nargs=1, default=["input1.txt"])
    parser.add_argument("-input2", nargs=1, default=["input2.txt"])
    parser.add_argument("-output1", nargs=1, default=["output1.xml"])
    parser.add_argument("-c", nargs=1, default=-1)

    args = parser.parse_args()

    first_input = args.input1[0]
    second_input = args.input2[0]
    first_output = args.output1[0]
    epochs = int(args.c[0])

    matrix = load_matrix(first_input)

    network_layers = []

    for layers in matrix:
        layer = []
        for neuron in layers:
            layer.append(Neuron(neuron))
        network_layers.append(Layer(layer))

    network = Network(network_layers)

    xArray, yArray = load_vector(second_input)
    '''
    print("До обучения:")
    for xi in xArray:
        output = network.forward(xi)
        print("Вход:", xi, "Выход:", output)

    print()
    '''
    result = network.learning(xArray, yArray, 0.1, epochs)
    '''
    print("После обучения:")
    for xi in xArray:
        output = network.forward(xi)
        print("Вход:", xi, "Выход:", output)
    '''
    with open(first_output, "w") as file:
        for i, elem in enumerate(result):
            file.write(f"{i}: {elem})\n")
