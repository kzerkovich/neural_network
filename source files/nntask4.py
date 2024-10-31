import argparse
import math
import os
import xml.etree.ElementTree as ET


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
                    lines.append([int(x) for x in element.strip("[]").split()])
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
        with open(vector_file, 'r') as f:
            for line in f:
                return [int(x) for x in line.split()]
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculate(matrix, vector):
    new_matrix = []

    for layer in matrix:
        tmp = []
        for neuron in layer:
            if len(neuron) == len(vector):
                weighted_sum = sum(w * x for w, x in zip(neuron, vector))
                output = sigmoid(weighted_sum)
                tmp.append(output)
            else:
                log("Ошибка! Несоответствие размерностей.")
                exit()
        new_matrix.append(tmp)
        vector = tmp

    return new_matrix[-1]



def matrix_to_xml(matrix, path):
    root = ET.Element('NeuralNetwork')

    for layer in matrix:
        layer_elem = ET.SubElement(root, 'layer')
        for neuron in layer:
            ET.SubElement(layer_elem, 'neuron').text = str(neuron)

    root = ET.fromstring(ET.tostring(root, encoding='utf-8'))
    tree = ET.ElementTree(root)

    ET.indent(tree, '   ')

    tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nntask4.exe",
        description="Creating a directed graph")
    parser.add_argument("-input1", nargs=1, default=["input1.txt"])
    parser.add_argument("-input2", nargs=1, default=["input2.txt"])
    parser.add_argument("-output1", nargs=1, default=["output1.xml"])
    parser.add_argument("-output2", nargs=1, default=["output2.txt"])

    args = parser.parse_args()

    first_input = args.input1[0]
    second_input = args.input2[0]
    first_output = args.output1[0]
    second_output = args.output2[0]

    matrix = load_matrix(first_input)

    vector = load_vector(second_input)

    result = calculate(matrix, vector)

    matrix_to_xml(matrix, first_output)

    with open(second_output, "w") as file:
        file.write(" ".join(str(x) for x in result))