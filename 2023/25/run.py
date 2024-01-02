#! /usr/bin/python3

import networkx as nx
import itertools


def parse_line(line):
    # return edge list e.g. [('A', 'B'), ('A', 'C'), ('B', 'D')]
    v1, v2_list = [i for i in line.strip().split(":")]
    return [(v1, v2) for v2 in [v for v in v2_list.split(" ") if v != ""]]


def rank_edges_by_betweenness_centrality(G):
    # Calculate edge betweenness centrality for the graph
    edge_betweenness = nx.edge_betweenness_centrality(G)

    # Sort the edges based on their betweenness centrality in descending order
    sorted_edges = sorted(edge_betweenness.items(), key=lambda x: x[1], reverse=True)

    return sorted_edges


def gen_trial_edge_set(ranked_edges):
    # Generate all possible 3-edge combinations
    # in sorted order of centrality
    subset_size = 3
    already_tried = set()
    while subset_size < 5:  # len(ranked_edges):
        subset = ranked_edges[:subset_size]
        combinations = itertools.combinations(subset, 3)
        for comb in combinations:
            if comb not in already_tried:
                already_tried.add(comb)
                yield comb
        subset_size += 1


with open("input.txt", "r") as f:
    edges = [parse_line(line) for line in f.readlines()]

    # parse edge lists into 1 complete adjacency list
    # e.g. {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}
    adj_list = {}
    for edge in edges:
        for v1, v2 in edge:
            if v1 not in adj_list:
                adj_list[v1] = []
            adj_list[v1].append(v2)

    G = nx.from_dict_of_lists(adj_list)

    temp_graph = G.copy()

    ranked_edges = rank_edges_by_betweenness_centrality(temp_graph)

    # Print the ranked edges
    # for edge, centrality in ranked_edges:
    #     print(f"Edge: {edge}, Betweenness Centrality: {centrality}")

    for edges_to_remove in gen_trial_edge_set(ranked_edges):
        edges_to_remove = [edge[0] for edge in edges_to_remove]
        temp_graph.remove_edges_from(edges_to_remove)

        if not nx.is_connected(temp_graph):
            print(f"removing edges {edges_to_remove} disconnects the graph")

            # Find disconnected components, calculate the answer
            components = list(nx.connected_components(temp_graph))
            result = 1
            for i, component in enumerate(components):
                subgraph = G.subgraph(component)
                print(f"Component {i + 1}:")
                print("   Nodes:", subgraph.nodes())
                print("   Edges:", subgraph.edges())
                print("   Number of nodes:", subgraph.number_of_nodes())
                print("   Number of edges:", subgraph.number_of_edges())

                result *= subgraph.number_of_nodes()

            print(f"Result: {result}")

            break

        # Reset the graph
        temp_graph = G.copy()
