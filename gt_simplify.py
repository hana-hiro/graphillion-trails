#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Make the given graph a simple graph

from itertools import chain

def simplify(graph):
    # List of existing vertex names
    vertex_names = set(chain.from_iterable(graph))
    
    # Determine the separator
    used_characters = set(str.join("", vertex_names))
    sep = None
    
    for c in ["_", "-", "+", "=", "~", "*", "^", "`", ",", ".", '"', "'", "|", "/", "&", ";", ":", "#", "!", "?", "%", "@", "\\", "$"]:
        if c not in used_characters:
            sep = c
            break
    
    if sep is None:
        raise "No separator character available"
    
    # Table of numbers for naming inserted vertices
    numbers = {}
    
    # sort
    for edge in graph:
        edge.sort()
    
    graph.sort()
    
    # Insert additional vertices in multiple edges
    tmp_graph = []
    for i in range(0, len(graph)):
        if i == 0 or graph[i] != graph[i-1]:
            tmp_graph.append(graph[i])
        else:
            tmp_vertex_base = graph[i][0]+sep+graph[i][1]
            tmp_vertex = ""
            
            numbers[tmp_vertex_base] = numbers.get(tmp_vertex_base, 0)
            while True:
                numbers[tmp_vertex_base] += 1
                tmp_vertex = tmp_vertex_base+"("+str(numbers[tmp_vertex_base])+")"
                if tmp_vertex not in vertex_names:
                    break
            
            vertex_names.add(tmp_vertex)
            tmp_graph.append([graph[i][0], tmp_vertex])
            tmp_graph.append([tmp_vertex, graph[i][1]])
    
    graph = tmp_graph
    
    # Insert additional vertices in loop edges
    tmp_graph = []
    for i in range(0, len(graph)):
        if graph[i][0] != graph[i][1]:
            tmp_graph.append(graph[i])
        else:
            tmp_vertex_base = graph[i][0]+sep
            tmp_vertex1 = ""
            tmp_vertex2 = ""
            
            numbers[tmp_vertex_base] = numbers.get(tmp_vertex_base, -1)
            while True:
                numbers[tmp_vertex_base] += 2
                tmp_vertex1 = tmp_vertex_base+"("+str(numbers[tmp_vertex_base])+")"
                tmp_vertex2 = tmp_vertex_base+"("+str(numbers[tmp_vertex_base]+1)+")"
                if (tmp_vertex1 not in vertex_names) and (tmp_vertex2 not in vertex_names):
                    break
            
            vertex_names.add(tmp_vertex1)
            vertex_names.add(tmp_vertex2)
            tmp_graph.append([graph[i][0], tmp_vertex1])
            tmp_graph.append([tmp_vertex1, tmp_vertex2])
            tmp_graph.append([tmp_vertex2, graph[i][0]])
    
    graph = tmp_graph
    
    return graph

if __name__ == '__main__':
    import gt_read_graph
    import sys
    import fileinput
    
    result = []
    for l in fileinput.input():
        gt_read_graph.parse_line(l, result, False)
    
    for edges in simplify(result):
        print str.join(' ', edges)

