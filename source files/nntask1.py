import argparse
import os
import xml.etree.ElementTree as ET


def log(error):
    log_file = open("Log.txt", "w", encoding="utf-8")
    log_file.write(error)


def sort1(edges):
    return sorted(edges, key=lambda x: (x[0]))


def sort2(edges):
    return sorted(edges, key=lambda x: (x[1]))


def change_order(edges):
    result = []

    for i in range(len(edges)):
        elem = edges[i]
        if elem not in result:
            result.append(elem)
        for j in range(i + 1, len(edges)):
            sec = edges[j]
            if elem[1] == sec[1]:
                if elem[2] > sec[2]:
                    if sec not in result:
                        result.insert(result.index(elem), sec)
                if elem[2] < sec[2]:
                    if sec not in result:
                        result.insert(result.index(elem) + 1, sec)

    return result


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
            edges[i] = (a, b, int(n))
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

    # edges = change_order(edges)

    return edges


def graph_to_xml(edges, path):
    vertices = []

    for (x1, x2, _) in edges:
        if int(x1) not in vertices:
            vertices.append(int(x1))
        if int(x2) not in vertices:
            vertices.append(int(x2))

    root = ET.Element('graph')
    vertices.sort()
    for vertex in vertices:
        vertex_elem = ET.SubElement(root, 'vertex')
        vertex_elem.text = str(vertex)

    for vertex in edges:
        arc_elem = ET.SubElement(root, 'arc')
        ET.SubElement(arc_elem, 'from').text = vertex[0]
        ET.SubElement(arc_elem, 'to').text = vertex[1]
        ET.SubElement(arc_elem, 'order').text = str(vertex[2])

    root = ET.fromstring(ET.tostring(root, encoding='utf-8'))
    tree = ET.ElementTree(root)

    ET.indent(tree, '   ')

    tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nntask1.exe",
        description="Creating a directed graph")
    parser.add_argument("-input1", nargs=1, default=["input.txt"])
    parser.add_argument("-input2", nargs=1, default=["input2.txt"])
    parser.add_argument("-output1", nargs=1, default=["output.xml"])
    parser.add_argument("-output2", nargs=1, default=["output2.xml"])

    args = parser.parse_args()

    first_input = args.input1[0]
    second_input = args.input2[0]
    first_output = args.output1[0]
    second_output = args.output2[0]

    graph = check_graph(first_input)

    graph_to_xml(graph, first_output)
