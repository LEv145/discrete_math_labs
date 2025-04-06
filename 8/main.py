import numpy
import random
from random import randint
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def max_flow_algorithm(G, source, sink):
    # Шаг 1: Инициализация потоков (Этап 1)
    for u, v in G.edges:
        G[u][v]["flow"] = 0

    # Этап 1: Насыщение потока (Шаги 2-4)
    while True:
        # Шаг 2: Поиск ненасыщенного пути
        path = find_unsaturated_path_phase1(G, source, sink)
        if not path:
            break  # Шаг 4: Пути не найдены -> поток насыщен
        # Шаг 3: Увеличение потока
        min_residual = min(G[u][v]["capacity"] - G[u][v]["flow"] for u, v in path)
        for u, v in path:
            G[u][v]["flow"] += min_residual

    # Этап 2: Пометка вершин и перераспределение (Шаги 5-7)
    while True:
        # Шаг 5-6: Пометка вершин
        labels, sink_labeled = phase2_labeling(G, source, sink)
        if not sink_labeled:
            break  # Этап 3: S не помечен -> переход к Шагу 8
        # Шаг 7: Перераспределение потока
        augmenting_path, delta = find_augmenting_path(G, labels, source, sink)
        if not augmenting_path:
            break
        augment_flow(G, augmenting_path, delta)

    # Этап 3: Определение разреза (Шаг 8)
    A = set(labels.keys())    # Множество помеченных вершин
    B = set(G.nodes) - A      # Множество непомеченных

    # Вычисление максимального потока
    max_flow = sum(G[source][neighbor]["flow"] for neighbor in G.successors(source))
    return max_flow, A, B

# Шаг 2: Поиск ненасыщенного пути (BFS)
def find_unsaturated_path_phase1(graph, source, sink):
    visited = {node: False for node in graph.nodes}
    parent = {}
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in graph.successors(u):
            # Проверка на ненасыщенность (flow < capacity)
            if not visited[v] and graph[u][v]["flow"] < graph[u][v]["capacity"]:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                if v == sink:
                    # Восстановление пути
                    path = []
                    current = sink
                    while current != source:
                        path.append((parent[current], current))
                        current = parent[current]
                    path.reverse()
                    return path
    return None  # Путь не найден

# Шаги 5-6: Алгоритм пометки вершин
def phase2_labeling(graph, source, sink):
    labels = {}
    labels[source] = (None, "+")  # Шаг 5: Пометить исток "I" (здесь "+" как направление)
    queue = deque([source])
    reached_sink = False

    while queue and not reached_sink:
        m = queue.popleft()

        # Обработка прямых рёбер (m -> n)
        for n in graph.successors(m):
            if n not in labels and graph[m][n]["flow"] < graph[m][n]["capacity"]:
                labels[n] = (m, "+")  # Метка +m для ненасыщенных рёбер
                queue.append(n)
                if n == sink:
                    reached_sink = True
                    break

        # Обработка обратных рёбер (m <- n)
        if not reached_sink:
            for n in graph.predecessors(m):
                if n not in labels and graph[n][m]["flow"] > 0:
                    labels[n] = (m, "-")  # Метка -m для ненулевых обратных потоков
                    queue.append(n)
                    if n == sink:
                        reached_sink = True
                        break

    return labels, reached_sink


# Шаг 7: Поиск увеличивающего пути и вычисление δ
def find_augmenting_path(graph, labels, source, sink):
    # Проверка вроде не нужна, но оставлена на всякий случай, чтобы избежать ошибок
    if sink not in labels:
        return None, 0

    path = []
    current = sink
    delta = float("inf")

    # Восстановление пути из меток
    while current != source:
        pred, direction = labels[current]

        if direction == "+":
            u, v = pred, current
            residual = graph[u][v]["capacity"] - graph[u][v]["flow"]
            path.append((u, v, "+"))  # Прямое ребро
        elif direction == "-":
            u, v = current, pred
            residual = graph[v][u]["flow"]
            path.append((u, v, "-"))  # Обратное ребро

        delta = min(delta, residual)
        current = pred

    path.reverse()
    return path, delta

# Шаг 7: Увеличение/уменьшение потока
def augment_flow(graph, path, delta):
    for u, v, direction in path:
        if direction == "+":
            graph[u][v]["flow"] += delta  # Увеличение на прямых рёбрах
        else:
            graph[v][u]["flow"] -= delta  # Уменьшение на обратных рёбрах

# Визуализация разреза (Этап 3)
def draw_graph_with_cut(graph, A, B, source, sink):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 6))

    # Цвета вершин по множествам A и B
    node_colors = ["lightblue" if node in A else "lightgreen" for node in graph.nodes]

    # Красные рёбра разреза (A->B)
    edge_colors = [
        "red" if (u in A and v in B) else "black"
        for u, v in graph.edges
    ]

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, arrows=True)
    nx.draw_networkx_labels(graph, pos)

    # Подписи рёбер: поток/пропускная способность
    edge_labels = {
        (u, v): f"({graph[u][v]["capacity"]})"
        for u, v in graph.edges
    }
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="blue")

    plt.title(f"Max Flow: {sum(graph[source][n]["flow"] for n in graph.successors(source))}")
    plt.show()

def main() -> None:
    random.seed(42)

    edges_list = [
        [
            ("A", "p", 7), ("A", "d", 5), ("A", "a", 3),
            ("a", "d", 2), ("a", "k", 1), ("a", "b", 6),
            ("b", "C", 5),
            ("c", "b", 1), ("c", "C", 4),
            ("d", "k", 2), ("d", "c", 6),
            ("p", "k", 2), ("p", "b", 3),
            ("k", "C", 6),
        ],
        [
            ("A", "B", 5), ("A", "C", 9), ("A", "I", 4),
            ("B", "I", 6), ("B", "C", 6), ("B", "G", 6),
            ("D", "C", 6),
            ("E", "D", 7),
            ("F", "E", 7), ("F", "D", 7), ("F", "C", 6),
            ("G", "C", 7), ("G", "D", 3), ("G", "E", 3), ("G", "F", 3),
            ("H", "C", 7), ("H", "G", 7), ("H", "F", 7),
            ("I", "C", 4), ("I", "G", 6), ("I", "H", 7),
        ],
        [
            ("A", "B", randint(100, 1000)), ("A", "C", randint(100, 1000)), ("A", "I", randint(100, 1000)),
            ("B", "I", randint(100, 1000)), ("B", "C", randint(100, 1000)), ("B", "G", randint(100, 1000)),
            ("D", "C", randint(100, 1000)),
            ("E", "D", randint(100, 1000)),
            ("F", "E", randint(100, 1000)), ("F", "D", randint(100, 1000)), ("F", "C", randint(100, 1000)),
            ("G", "C", randint(100, 1000)), ("G", "D", randint(100, 1000)), ("G", "E", randint(100, 1000)), ("G", "F", randint(100, 1000)),
            ("H", "C", randint(100, 1000)), ("H", "G", randint(100, 1000)), ("H", "F", randint(100, 1000)),
            ("I", "C", randint(100, 1000)), ("I", "G", randint(100, 1000)), ("I", "H", randint(100, 1000)),
        ],
    ]
    for edges in edges_list:
        numpy.random.seed(5)
        G = nx.DiGraph()

        for a, b, capacity in edges:
            G.add_edge(a, b, capacity=capacity)

        max_flow, A, B = max_flow_algorithm(G, "A", "C")
        print(f"Максимальный поток: {max_flow}")
        print(f"Множество A: {A}")
        print(f"Множество B: {B}")

        # Шаг 8: Визуализация минимального разреза
        draw_graph_with_cut(G, A, B, "A", "C")

if __name__ == "__main__":
    main()
