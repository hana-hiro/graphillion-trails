# graphillion-trails

(C)2014-2015 Hiroyuki HANADA <hana-hiro@live.jp>

The author conducted the work under the research project
"ERATO Minato Discrete Structure Manipulation System Project"
by Japan Science and Technology Agency.
https://www-erato.ist.hokudai.ac.jp/
http://www.jst.go.jp/erato/research_area/ongoing/mrk_PJ.html

# 1. Overview

This program enumerates all trails (edge-disjoint walks) or all Eulerian trails
(walks that visit every edge just once) in a graph,
using "Graphillion": a path enumeration library in graphs.

For example of the graph below, there are 9 trails from B to C.
(BC, BAC, BDC, BACBDC, BACDBC, BDCABC, BCABDC, BDCBAC, BCDBAC)
Among them, the last 6 trails are Eulerian.

    A----B
    | __/|
    |/   |
    C----D

# 2. Technical feature

There are many researches on enumerating simple paths (vertex-disjoint walks)
rather than trails. Especially, the methods based on "zero-suppressed binary
decision diagram" (ZDD) is considered efficient for many practical cases.
(It needs, however, exponential time in general.)

The author developed a trail enumeration algorithm based on the simple path
enumeration algorithm in both mathematical consideration and implementation.
The key structure is "line graph", whose vertices correspond one-to-one
to the edges in the original graph.
[References]
http://link.springer.com/chapter/10.1007/978-3-319-15612-5_15
(Proceedings in an international conference)
http://www-alg.ist.hokudai.ac.jp/~thomas/TCSTR/tcstr_14_79/tcstr_14_79.pdf
(Technical report version of the proceeding above)
*Note: These manuscripts explain only eulerian trail case, but the program
       includes both "all trails" and "all eulerian trails" case.

In this program, simple path enumeration is done with "Graphillion", ZDD-based
graph and path library.
https://github.com/takemaru/graphillion (distributed here)
http://www-alg.ist.hokudai.ac.jp/~thomas/TCSTR/tcstr_13_65/tcstr_13_65.pdf

# 3. Preparation

Install Python and then Graphillion (see above).

# 4. Running the program

First let us prepare graph files. (Some samples are included.)
In the file, each line represents an edge, and each element in the line
(separated by space) represents the vertex. The program assumes every line has
just one space.

It is recommended that graph files have the extension ".graph".

For example, the following graph

    A----B
    | __/|
    |/   |
    C----D

is expressed as the file of the following content:

    A B
    A C
    B C
    B D
    C D

When we have the file at the path "sample/box.graph", let us input

    python graphtrail.py -E B,C sample/box.graph

Then we have the result

    Number of trails: 9
    Computation time (sec): 0.003668
    Number of pairs of edges as constraints: 24
    Trails:
    B, C, A, B, D, C
    B, C, D, B, A, C
    B, D, C, A, B, C
    B, D, C, B, A, C
    B, A, C, B, D, C
    B, A, C, D, B, C
    B, A, C
    B, C
    B, D, C

As shown in the top, 9 different trails are shown.
Note that "-E B,C" represents that "trails beginning with B and ending with C".

Using "-U" instead of "-E", only eulerian trails are enumerated. With the command

    python graphtrail.py -U B,C sample/box.graph

we get

    Number of trails: 6
    Computation time (sec): 0.003417
    Number of pairs of edges as constraints: 24
    Trails:
    B, C, A, B, D, C
    B, C, D, B, A, C
    B, D, C, A, B, C
    B, D, C, B, A, C
    B, A, C, B, D, C
    B, A, C, D, B, C

In the commands above, the following files are automatically generated.

FILENAME.graph   - Original graph
FILENAME.sgraph  - The simple graph of the original graph
FILENAME.lsgraph - The line graph of the simple graph
FILENAME.lsgraph.json
- The mapping from the vertices in the original graph to the vertices in the
  line graph (i.e. edges in the original graph)

# 5. Command line option

python graphtrail.py -h

# 6. License

Available under MIT License. The full license text is in LICENSE.txt.

# 7. Contact

Hiroyuki HANADA <hana-hiro@live.jp> (contact in English or Japanese)
