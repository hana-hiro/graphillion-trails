#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gt_read_graph import read_graph

from collections import defaultdict
from itertools import combinations, chain
from graphillion import GraphSet
import sys
import time

def enumerate_trails(labeled_linegraph, node_table, start, goal, eulerian = False):
    # `labeled_linegraph' is an array of three-element arrays,
    # where each three-element array represents an edge in the line graph as follows:
    # [[node0, node1, label], [node0, node1, label], ...]
    # (See the reference for the definition of the `label'.)
    
    # --------- Add dummy vertices for the beginning and the ending of the paths ---------
    # Because the beginning or the ending of the simple paths in the line graph shoule be unique,
    # we add dummy vertices in the original graph so that the beginning or the ending of the trails
    # in the original graph is unique.
    # To achieve it with only the line graph, we have only to generate dummy beginning and ending
    # in the line graph (`bB' and `eE' in the figure below) and connect it to all vertices
    # including `B' or `E', respectively.
    # 
    # (B: Beginning, E: Ending, b: Dummy Beginning, e: Dummy Ending)
    # 
    # ORIGINAL  B----X       b----B----X
    # GRAPH     | __/|  -->       | __/|
    #           |/   |            |/   |
    #           Y----E            Y----E----e
    #
    #                           bB___         (Connect `bB' to all vertices including `B')
    # LINE      __BX__          |  __BX__
    # GRAPH    /  |   \         | /  |   \
    #        BY---XY---XE  -->  BY---XY---XE
    #          \__| __/           \__| __/ |
    #             YE                 YE____eE (Connect `eE' to all vertices including `E')
    
    # Classify edges in the line graph by their labels
    label2edge = defaultdict(list)
    for labeled_edge in labeled_linegraph:
        label2edge[labeled_edge[2]].append(tuple(labeled_edge[0:2]))
    
    if start not in node_table.keys() or goal not in node_table.keys():
        raise StandardError, "Start/Goal vertices are must be chosen from: " + str.join(", ", sorted(node_table.keys()))
    
    # Add dummy vertices and connect
    for vdummy, vtarget in (("{{START}}", start), ("{{GOAL}}", goal)):
        for vtarget_lg in node_table[vtarget]:
            label2edge[vtarget].append((vdummy, vtarget_lg))
    
    # --------- Generate the constraint for the simple paths in the line graph ---------
    # --------- so that they construct trails in the original graph            ---------
    constraint = []
    
    # line graph without labels
    linegraph = list(chain.from_iterable(label2edge.values()))
    
    # The constraint is that
    # "Two edges cannot be included in a simple path in the line graph
    #  if they have the same label and they share a vertex".
    # (See the reference for the detailed conditions and the proofs.)
    for edges in label2edge.values():
        for edge_pair in combinations(edges, 2):
            if len(set(edge_pair[0]).intersection(set(edge_pair[1]))) > 0:
                constraint.append(list(edge_pair))
    
    # --------- Enumerate ---------
    #print "ARGUMENT linegraph:  " + str(linegraph)
    #print "ARGUMENT constraint: " + str(constraint)
    #print "ARGUMENT start:      " + str(start)
    #print "ARGUMENT goal:       " + str(goal)
    
    GraphSet.set_universe(linegraph, 'bfs')
    #GraphSet.set_universe(new_ordering(linegraph), 'as-is') # To change the variable ordering in ZDD
    sgs = GraphSet({}).excluding(GraphSet(constraint))
    
    time_begin = time.clock()
    gs = GraphSet.paths("{{START}}", "{{GOAL}}", eulerian, graphset = sgs)
    total_count = gs.len()
    time_end = time.clock()

    return {
        "trails": total_count,
        "time": time_end - time_begin,
        "constraints": len(constraint),
        "index": gs,
    }

# Obtain the simple path from the set of edges.
# Ends with exception if the edges do not compose a simple path.
# 
# edges2path([[1, 2], [3, 4], [2, 4]]) # => [1, 2, 4, 3]
# edges2path([[1, 2], [3, 4], [2, 4], [3, 2]]) # => ERROR
def edges2path(edges):
    edge_table = defaultdict(list)
    
    # Classify edges by vertices
    for e in edges:
        edge_table[e[0]].append(e)
        edge_table[e[1]].append(e)
    
    # Classify vertices by degrees
    degree_1_vertices = []
    
    for v, e in edge_table.items():
        if len(e) == 1:
            degree_1_vertices.append(v)
        elif len(e) == 2:
            pass
        else:
            raise RuntimeError, "Given edges do not compose a path: the vertex \"" + v + "\" has degree " + str(len(e)) + " (expected 1 or 2)"
    
    if len(degree_1_vertices) != 2:
        raise RuntimeError, "Given edges do not compose a path: degree-1 vertices must be found just twice (" + str(len(degree_1_vertices)) + " found)"
    
    # Find the path, beginning with the degree-1 vertex
    degree_1_vertices.sort()
    degree_1_vertices.reverse()
    v = degree_1_vertices[0]
    result = [v]
    while True:
        current_edges = edge_table[v]
        if len(current_edges) == 0 and v == degree_1_vertices[1]:
            break
        
        if len(current_edges) != 1:
            raise RuntimeError, "Given edges do not compose a path because of vertex \"" + v + "\" (Remained edges: " + str(edge_table) + ")"
        
        current_edge = current_edges[0]
        edge_table[current_edge[0]].remove(current_edge)
        edge_table[current_edge[1]].remove(current_edge)
        
        current_edge = list(current_edge)
        current_edge.remove(v)
        v = current_edge[0]
        result.append(v)
    
    # In case some of the edges are not consumed as the path
    # (i.e. the set of edges are disconnected)
    if len(list(chain.from_iterable(edge_table.values()))) != 0:
        raise RuntimeError, "Given edges do not compose a path: path not connected"
    
    return result

if __name__ == '__main__':
    import json_nonunicode
    import sys
    
    if len(sys.argv) != 6:
        sys.stderr.write("Usage: " + sys.argv[0] + " File.lsgraph NodeTable.json StartNode GoalNode OnlyEulerian(0/1)\n")
        sys.exit(-1)
    
    labeled_linegraph = read_graph(sys.argv[1], True)
    
    f = open(sys.argv[2], 'rb')
    try:
        node_table = json_nonunicode.load(f)
    except ValueError:
        node_table = None
    
    f.close()
    
    if not isinstance(node_table, dict):
        sys.stderr.write("Invalid NodeTable file: the value must be a dictionary\n")
        sys.exit(-1)
    
    eulerian = None
    if sys.argv[5] == "0":
        eulerian = False
    elif sys.argv[5] == "1":
        eulerian = True
    else:
        sys.stderr.write("Specify 0 if enumerating all trails or 1 if only eulerian trails.\n")
        sys.exit(-1)
    
    res = enumerate_trails(labeled_linegraph, node_table, sys.argv[3], sys.argv[4], eulerian)
    
    if res is not None:
        print "Number of trails: " + str(res["trails"])
        print "Computation time (sec): " + str(res["time"])
        print "Number of pairs of edges as constraints: " + str(res["constraints"])
    else:
        sys.stderr.write("Computation failed\n")
        sys.exit(-1)
        
        for k in res:
            print k + ": " + str(res[k])
        print
    
    #print "<Trails>"
    #for i in res["index"]:
    #    print edges2path(list(i))

