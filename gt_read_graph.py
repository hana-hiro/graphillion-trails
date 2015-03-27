#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_line(line, result_array, is_labeled):
    column_num = 3 if is_labeled else 2
    
    vertices = line.split()
    if len(vertices) == 0:
        pass
    elif len(vertices) == column_num:
        result_array.append(vertices)
    else:
        raise StandardError, "Invalid edge description ('" + str(len(vertices)) + "' vertices specified; '" + str(column_num) + "' expected)"

def parse_graph(lines, is_labeled):
    result = []
    for l in lines:
        parse_line(l, result, is_labeled)
    
    return result

def read_graph(filename, is_labeled):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return parse_graph(lines, is_labeled)

