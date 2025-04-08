import random

import numpy
import matplotlib.pyplot as plt
import networkx as nx


EDGES = [
    (4, 7), (5, 11), (3, 4), (11, 14), (8, 13), (7, 8),
    (3, 5), (8, 12), (2, 4), (6, 12), (3, 16), (6, 11),
    (5, 13), (6, 13), (5, 9), (12, 16), (2, 8), (8, 10),
    (5, 10), (14, 15), (5, 7), (8, 9), (5, 12), (6, 9),
    (13, 14), (4, 15), (9, 16), (4, 13), (11, 16), (10, 14),
    (8, 11), (4, 9), (3, 14), (7, 14), (7, 16),
]


def make_bipartite_simple(G: nx.Graph):
    color_map = {}
    edges_removed = []

    for start_node in G.nodes():
        if start_node not in color_map:
            color_map[start_node] = 0
            queue = [start_node]

            while queue:
                current = queue.pop(0)
                current_color = color_map[current]

                for neighbor in G.neighbors(current):
                    if neighbor not in color_map:
                        color_map[neighbor] = 1 - current_color
                        queue.append(neighbor)
                    else:
                        if color_map[neighbor] == current_color:
                            G.remove_edge(current, neighbor)
                            edges_removed.append((current, neighbor))

    return edges_removed, color_map



def ford_fulkerson_bipartite_matching(G: nx.Graph):
    """
    Ищет наибольшее паросочетание в двудольном графе G методом Форда-Фалкерсона (через nx.maximum_flow).
    Предполагается, что G - двудольный граф.
    """
    U, V = nx.bipartite.sets(G)

    flow_graph = nx.DiGraph()

    flow_graph.add_node("S")
    flow_graph.add_node("T")
    flow_graph.add_nodes_from(G.nodes())


    # Связываем 'S'
    for u in U:
        flow_graph.add_edge("S", u, capacity=1)

    # Связываем 'U' и 'V'
    for (a, b) in G.edges():
        if a in U and b in V:
            flow_graph.add_edge(a, b, capacity=1)
        elif b in U and a in V:
            flow_graph.add_edge(b, a, capacity=1)

    # Связываем 'T'
    for v in V:
        flow_graph.add_edge(v, "T", capacity=1)

    flow_value, flow_dict = nx.maximum_flow(flow_graph, "S", "T")

    # Восстанавливаем ребра паросочетания: ищем те, что идут из U в V и имеют поток 1
    matching_edges = []
    for u in U:
        if u in flow_dict:
            for v, flow in flow_dict[u].items():
                if v in V and flow == 1:  # Насыщено
                    matching_edges.append((u, v))

    return matching_edges, len(matching_edges)


def kuhn_maximum_matching(G):
    """
    Реализация алгоритма Куна (Kuhn's algorithm) для нахождения наибольшего паросочетания в двудольном графе G.
    """

    U, V = nx.bipartite.sets(G)

    adjacency = {u: [] for u in U}
    for (a, b) in G.edges():
        if a in U and b in V:
            adjacency[a].append(b)
        elif b in U and a in V:
            adjacency[b].append(a)

    # match_for_v[v] будет хранить, с какой вершиной u сейчас сопоставлена вершина v (или None, если свободна).
    match_for_v = {v: None for v in V}

    # Вспомогательная функция DFS — пытается найти/улучшить
    # «увеличивающую цепь» для вершины u
    def try_kuhn(u, visited):
        """Пытается найти свободную вершину v (или перенаправить занятую),
           проходя по списку смежности у 'u'."""
        for v in adjacency[u]:
            # проверяем, не заходили ли мы уже в v при данном запуске
            if v not in visited:
                visited.add(v)
                # если v свободна (match_for_v[v] == None)
                # или пытаемся "перенаправить" текущего владельца v
                if match_for_v[v] is None or try_kuhn(match_for_v[v], visited):
                    match_for_v[v] = u
                    return True
        return False

    for u in U:
        visited = set() # Множество посещённых за одну итерацию v
        try_kuhn(u, visited)

    # Формируем список рёбер (u, v), которые образуют паросочетание
    matching_edges = []
    for v, u in match_for_v.items():
        if u is not None:
            matching_edges.append((u, v))

    matching_size = len(matching_edges)
    return matching_edges, matching_size


def main() -> None:
    numpy.random.seed(47)
    G = nx.Graph()
    G.add_edges_from(EDGES)

    # Проверяем, двудольный ли уже
    print("Является ли граф двудольным до модификации?", nx.is_bipartite(G))

    # 3. Делаем попытку «наивной» 2-раскраски с удалением конфликтных рёбер
    removed_edges, color_map = make_bipartite_simple(G)
    print(removed_edges, color_map)

    ford_fulkerson_bipartite_matching(G)


    node_color = ["red" if color_map[node] else "green" for node in G]
    nx.draw_networkx(G, node_color=node_color)

    plt.show()


if __name__ == "__main__":
    main()
