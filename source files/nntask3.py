import argparse
import math
import os


def log(error):
    log_file = open("Log.txt", "w", encoding="utf-8")
    log_file.write(error)


adj = {}


def check_graph(input_file):
    if not os.path.isfile(input_file):
        log(f"Файл {input_file} не существует")
        exit()

    edges = []
    line = ""
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for st in file:
                line += st.replace("\n", " ")
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()

    edges += (line.replace(" ", "").strip("\n").split("),"))

    edge_number = 1

    for i in range(len(edges)):
        try:
            a, b, n = edges[i].strip(",()").split(",")
            edges[i] = (int(a), int(b), int(n))
        except Exception:
            log(f"Ошибка ввода данных дуги {edge_number}: Некорректный формат записи.")
            exit()

        edge_number += 1

    unique = set()
    for x1, x2, _ in edges:
        if (x1, x2) in unique:
            log(f"Ошибка ввода данных. Дуга из вершины {x1} в {x2} уже есть")
            exit()
        unique.add((x1, x2))

    for i in range(len(edges)):
        current = edges[i]
        for j in range(i + 1, len(edges)):
            elem = edges[j]
            if current[1] == elem[1] and current[2] == elem[2]:
                log(f"Ошибка ввода данных : Одинаковые порядки у элементов {current} и {elem}.")
                exit()

    adj_list = {}
    for a, b, n in edges:
        if a not in adj_list:
            adj_list[a] = {'out': [], 'in': {}}
        if b not in adj_list:
            adj_list[b] = {'out': [], 'in': {}}

        adj_list[a]['out'].append((b, n))
        adj_list[b]['in'][n] = a

    global adj
    adj = adj_list

    return adj_list


def check_operations(input_file):
    if not os.path.isfile(input_file):
        log(f"Файл {input_file} не существует")
        exit()

    oper = {}
    try:
        with open(input_file, 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                oper[int(key.strip('a_'))] = value.strip()
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()

    return oper


def find_sink(data):
    for key, value in data.items():
        if not value['out']:
            return key


def calculate(node, operation, output):
    global result
    try:
        if adj.get(node)['in']:
            if operation[node] == '+':
                result = 0
                for _, elem in adj.get(node)['in'].items():
                    result += calculate(elem, operation, output)
            elif operation[node] == '*':
                result = 1
                for _, elem in adj.get(node)['in'].items():
                    result *= calculate(elem, operation, output)
            elif operation[node] == 'exp':
                for _, elem in adj.get(node)['in'].items():
                    result = math.exp(calculate(elem, operation, output))
            return result
        else:
            return int(operation[node])
    except OverflowError:
        with open(output, "w") as file:
            file.write("Infinity")
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nntask3.exe",
        description="Creating a directed graph")
    parser.add_argument("-input1", nargs=1, default=["input1.txt"])
    parser.add_argument("-input2", nargs=1, default=["input2.txt"])
    parser.add_argument("-output1", nargs=1, default=["output1.txt"])
    parser.add_argument("-output2", nargs=1, default=["output2.txt"])

    args = parser.parse_args()

    first_input = args.input1[0]
    second_input = args.input2[0]
    first_output = args.output1[0]
    second_output = args.output2[0]

    graph = check_graph(first_input)

    operations = check_operations(second_input)

    sink = find_sink(graph)

    res = calculate(sink, operations, first_output)

    with open(first_output, "w") as file:
        file.write(str(res))
