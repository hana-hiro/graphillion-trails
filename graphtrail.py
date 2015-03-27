#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================
# 
# graphillion-trails: Enumerating trails in a graph
# (C) 2014-2015 Hiroyuki HANADA <hana-hiro@live.jp>
# 
# For details, see README.txt.
# Available under the MIT License. See LICENSE.txt.
# 
# ============================================================

from gt_read_graph import *
from gt_simplify import *
from gt_linegraph import *
from gt_enumerate import *
from optparse import OptionParser
import json_nonunicode
import json
import os
import os.path

def run_simple(infile, outfile):
    # Check whether the generation is needed
    time_in = os.path.getmtime(infile)
    
    try:
        time_out = os.path.getmtime(outfile)
    except os.error:
        time_out = 0    
    
    if time_in < time_out:
        sys.stderr.write("File \"" + outfile + "\" is up-to-date.\n")
        return
    
    sys.stderr.write("Generating \"" + outfile + "\"\n")
    
    # Generate the simple graph
    graph = read_graph(infile, False)
    sgraph = simplify(graph)
    
    ofile = open(outfile, "w")
    for edges in sgraph:
        ofile.write(str.join(' ', edges) + "\n")
    ofile.close()

def run_linegraph(infile, outfile):
    outfile_json = outfile + ".json"
    
    # Check whether the generation is needed
    time_in = os.path.getmtime(infile)
    
    try:
        time_out = min([os.path.getmtime(outfile), os.path.getmtime(outfile_json)])
    except os.error:
        time_out = 0
    
    if time_in < time_out:
        sys.stderr.write("Files \"" + outfile + "\" and \"" + outfile_json + "\" are up-to-date.\n")
        return
    
    sys.stderr.write("Generating \"" + outfile + "\" and \"" + outfile_json + "\"\n")
    
    # Generate the line graph
    sgraph = read_graph(infile, False)
    lg = line_graph(sgraph)
    
    ofile = open(outfile, "w")
    for edges in lg["edges"]:
        ofile.write(str.join(' ', edges) + "\n")
    ofile.close()

    for k in lg["name2vertices"]:
        if isinstance(lg["name2vertices"][k], set):
            lg["name2vertices"][k] = list(lg["name2vertices"][k])
    
    ofile = open(outfile_json, "w")
    ofile.write(json.dumps(lg["name2vertices"]))
    ofile.close()

def run_enumerate(infile, start, goal, eulerian, display_trails):
    lsgraph = read_graph(infile, True)

    ifile = open(infile + ".json", 'r')
    node_table = json_nonunicode.load(ifile)
    ifile.close()
    
    res = enumerate_trails(lsgraph, node_table, start, goal, eulerian)
    if res is not None:
        print "Number of trails: " + str(res["trails"])
        print "Computation time (sec): " + str(res["time"])
        print "Number of pairs of edges as constraints: " + str(res["constraints"])
        
        if display_trails > 0:
            print "Trails:"
            for i in res["index"]:
                path_on_line_graph = (edges2path(list(i)))[1:-1]
                trail_on_original_graph = [x.split(node_table[""]) for x in path_on_line_graph]
                trail_combined = []
                
                if len(trail_on_original_graph) == 1:
                    trail_combined = trail_on_original_graph[0]
                else:
                    for j in range(0, len(trail_on_original_graph)):
                        if j == 0:
                            if trail_on_original_graph[0][0] in trail_on_original_graph[1]:
                                trail_combined = [trail_on_original_graph[0][1], trail_on_original_graph[0][0]]
                            else:
                                trail_combined = [trail_on_original_graph[0][0], trail_on_original_graph[0][1]]
                        else:
                            if trail_on_original_graph[j][0] in trail_on_original_graph[j-1]:
                                trail_combined.append(trail_on_original_graph[j][1])
                            else:
                                trail_combined.append(trail_on_original_graph[j][0])

                print str.join(', ', trail_combined)
                display_trails -= 1
                if display_trails <= 0:
                    break
    else:
        sys.stderr.write("Computation failed\n")
        sys.exit(-1)

def opt_enumerate(option, opt_str, value, parser):
    if opt_str in {"-E", "--enumerate-auto", "-U", "--enumerate-eulerian-auto"}:
        parser.values.mode = ["auto", "simple", "linegraph", "enumerate"]
    else:
        parser.values.mode = ["enumerate"]
    
    if opt_str in {"-u", "--enumerate-eulerian", "-U", "--enumerate-eulerian-auto"}:
        parser.values.eulerian = True
    
    parser.values.start_goal = value.split(",")
    if len(parser.values.start_goal) != 2:
        raise StandardError, "Start/Goal vertices must be specified by two names of vertices"

def main():
    # ---------- Parse options ----------
    parser = OptionParser(usage = "Usage: graphtrail (-s|-S|-l|-L|-e NODE1,NODE2|-E NODE1,NODE2|-u NODE1,NODE2|-U NODE1,NODE2) (-o OUTFILE|-d) (INFILE|-i INFILE)")
    
    parser.set_defaults(mode = None)
    parser.set_defaults(outfile = None)
    parser.set_defaults(infile = None)
    parser.set_defaults(start_goal = None)
    parser.set_defaults(eulerian = False)
    parser.set_defaults(result = 0)
    
    parser.add_option("-s", "--simple", dest = "mode", action = "store_const", const = ["simple"],
                      help = "Given a graph given as INFILE, generate the simple graph.")
    parser.add_option("-l", "--linegraph", dest = "mode", action = "store_const", const = ["linegraph"],
                      help = "Given a simple graph given as INFILE, generate the line graph.")
    parser.add_option("-e", "--enumerate", dest = "mode", metavar = "NODE1,NODE2", action = "callback", type = "string", callback = opt_enumerate,
                      help = "Given a line graph as INFILE, enumerate the number of trails (edge-disjoint walks) in the original graph. In addition to INFILE, INFILE.json is also needed (generated by \"-l\" mode).")
    parser.add_option("-u", "--enumerate-eulerian", dest = "mode", metavar = "NODE1,NODE2", action = "callback", type = "string", callback = opt_enumerate,
                      help = "Similar to \"-e\", but enumerates only Eulerian trails (visiting each edge in the graph just once).")
    parser.add_option("-S", "--simple-auto", dest = "mode", action = "store_const", const = ["auto", "simple"],
                      help = "Conduct \"-s\", determining output file name automatically by the extensions.")
    parser.add_option("-L", "--linegraph-auto", dest = "mode", action = "store_const", const = ["auto", "simple", "linegraph"],
                      help = "Conduct \"-s\" and \"-l\", determining output file name automatically by the extensions.")
    parser.add_option("-E", "--enumerate-auto", dest = "mode", metavar = "NODE1,NODE2", action = "callback", type = "string", callback = opt_enumerate,
                      help = "Conduct \"-s\", \"-l\" and \"-e\", determining output file name automatically by the extensions.")
    parser.add_option("-U", "--enumerate-eulerian-auto", dest = "mode", metavar = "NODE1,NODE2", action = "callback", type = "string", callback = opt_enumerate,
                      help = "Similar to \"-E\", but enumerates only Eulerian trails (visiting each edge in the graph just once).")
    parser.add_option("-r", "--result", dest = "result", metavar = "NUMBER_OF_TRAILS", action = "store",
                      help = "Number of enumerated trails to be displayed (0 by default). Applicable to only \"-e\", \"-u\", \"-E\" and \"-U\".")
    
    parser.add_option("-o", "--outfile", dest = "outfile", metavar = "OUTFILE", action = "store",
                      help = "Output the result to OUTFILE. Applicable to only \"-s\" and \"-l\".")
    parser.add_option("-d", "--default-outfile", dest = "outfile", action = "store_const", const = False,
                      help = "(Chosen by default) Output the result to automatically named file.")
    parser.add_option("-i", "--infile", dest = "infile", metavar = "INFILE", action = "store",
                      help = "Read the graph from INFILE. \"-i\" can be omitted.")
    
    (options, args) = parser.parse_args()
    if options.mode is None:
        parser.print_help()
        return
    
    if options.infile is not None:
        args.insert(0, options.infile)
    
    if len(args) != 1:
        raise StandardError, "Just one input file can be specified"
    
    infile = args[0]
    outfile = options.outfile
    result_num = int(options.result)
    
    # ---------- Run operations ----------
    for mode in options.mode:
        if mode == "auto":
            outfile = False
        elif mode == "simple":
            if outfile is False:
                if infile[-6:].lower() == ".graph":
                    outfile_tmp = infile[:-6] + ".sgraph"
                else:
                    outfile_tmp = infile + ".sgraph"
            else:
                outfile_tmp = outfile
            run_simple(infile, outfile_tmp)
            infile = outfile_tmp
        elif mode == "linegraph":
            if outfile is False:
                if infile[-7:].lower() == ".sgraph":
                    outfile_tmp = infile[:-7] + ".lsgraph"
                else:
                    outfile_tmp = infile + ".lsgraph"
            else:
                outfile_tmp = outfile
            
            run_linegraph(infile, outfile_tmp)
            infile = outfile_tmp
        elif mode == "enumerate":
            run_enumerate(infile, options.start_goal[0], options.start_goal[1], options.eulerian, result_num)
        else:
            raise StandardError, "Unexpected error: Unknown mode specified"
    
main()

