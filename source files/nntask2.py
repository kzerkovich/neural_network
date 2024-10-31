import argparse
import os
import xml.etree.ElementTree as ET


def log(error):
    log_file = open("Log.txt", "w", encoding="utf-8")
    log_file.write(error)


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)
    for nextElem in graph[start] - visited:
        dfs(graph, nextElem, visited)
    return visited


def check_cycle(graph):
    adj_list = {}
    for v1, v2, _ in graph:
        if v1 not in adj_list:
            adj_list[v1] = []
        if v2 not in adj_list:
            adj_list[v2] = []
        adj_list[v1].append(v2)

    for v in adj_list:
        visited = set()
        stack = [v]
        while stack:
            current = stack.pop()
            if current in visited:
                return True
            visited.add(current)
            for neighbor in adj_list[current]:
                if neighbor not in visited:
                    stack.append(neighbor)

    return False


def get_data(input_file):
    if not os.path.isfile(input_file):
        log(f"Файл {input_file} не существует")
        exit()

    tree = ET.parse(input_file)
    root = tree.getroot()

    edges = []

    try:
        for arc in root.findall('arc'):
            from_vertex = arc.find('from').text
            to_vertex = arc.find('to').text
            order = int(arc.find('order').text)

            edges.append((int(from_vertex), int(to_vertex), order))
    except Exception:
        log(f"Ошибка считывания данных из файла")
        exit()

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

    return edges


def find_sink(data):
    for key, value in data.items():
        if not value['out']:
            return key


def build_function(node, adj_list):
    result = []

    for _, elem in adj_list.get(node)['in'].items():
        if elem == node:
            continue
        else:
            result.append(
                f"{elem}({build_function(elem, adj_list)})" if adj_list.get(elem)['in'] else f"{elem}")
    return ",".join(result) if result else ""


def get_fun_by_graph(path):
    graph = get_data(path)

    if check_cycle(graph):
        log("Ошибка. В графе есть цикл.")
    else:
        adj_list = {}
        for a, b, n in graph:
            if a not in adj_list:
                adj_list[a] = {'out': [], 'in': {}}
            if b not in adj_list:
                adj_list[b] = {'out': [], 'in': {}}

            adj_list[a]['out'].append((b, n))
            adj_list[b]['in'][n] = a

        sink = find_sink(adj_list)

        return f"{sink}({build_function(sink, adj_list)})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nntask2.exe",
        description="Creating a directed graph")
    parser.add_argument("-input1", nargs=1, default=["input.xml"])
    parser.add_argument("-input2", nargs=1, default=["input2.xml"])
    parser.add_argument("-output1", nargs=1, default=["output.xml"])
    parser.add_argument("-output2", nargs=1, default=["output2.xml"])

    args = parser.parse_args()

    first_input = args.input1[0]
    second_input = args.input2[0]
    first_output = args.output1[0]
    second_output = args.output2[0]

    result_str = get_fun_by_graph(first_input)

    with open(first_output, "w") as file:
        file.write(result_str)
