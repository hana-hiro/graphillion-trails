#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create the line graph

from collections import defaultdict
from itertools import chain
from itertools import combinations

def edge2vertex(vertex_pair, sep):
    return str.join(sep, sorted(vertex_pair))

def line_graph(graph):
    # List of existing vertex names
    vertex_names = set(chain.from_iterable(graph))
    
    # Determine the separator
    used_characters = set(str.join("", vertex_names))
    sep = None
    
    for c in ["|", "/", "&", ";", ":", "#", "!", "?", "%", "@", "\\", "$", "_", "-", "+", "=", "~", "*", "^", "`", ",", ".", '"', "'"]:
        if c not in used_characters:
            sep = c
            break
    
    if sep is None:
        raise "No separator character available"
    
    # Generating the line graph
    vertex_destination = defaultdict(list)
    
    for edge in graph:
        vertex_destination[edge[0]].append(edge[1])
        vertex_destination[edge[1]].append(edge[0])
    
    edges = []
    name2vertices = defaultdict(set)
    
    for vertex in sorted(vertex_destination.keys()):
        for pair in combinations(vertex_destination[vertex], 2):
            v1 = edge2vertex([vertex, pair[0]], sep)
            v2 = edge2vertex([vertex, pair[1]], sep)
            edges.append([v1, v2, vertex])
            name2vertices[vertex].add(v1)
            name2vertices[pair[0]].add(v1)
            name2vertices[vertex].add(v2)
            name2vertices[pair[1]].add(v2)
    
    name2vertices[""] = sep
    
    return {"edges": edges, "name2vertices": name2vertices}

if __name__ == '__main__':
    import gt_read_graph
    import sys
    import fileinput
    import json
    
    result = []
    for l in fileinput.input():
        gt_read_graph.parse_line(l, result, False)
    
    lg = line_graph(result)
    
    for k in lg["name2vertices"]:
        if isinstance(lg["name2vertices"][k], set):
            lg["name2vertices"][k] = list(lg["name2vertices"][k])
    
    sys.stderr.write(json.dumps(lg["name2vertices"])+"\n")
    for edge in lg["edges"]:
        print str.join(' ', edge)

