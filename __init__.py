#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#  
#  Copyright 2012 Kevin R <KRPent@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from graph import DiGraph
import algorithms

## \mainpage Yen's K-Shortest Path Algorithm
#
# \section intro_sec Introduction
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971 and implores any shortest path algorithm to find the best path, then proceeds to find K − 1 deviations of the best path. See also, <a href="http://en.wikipedia.org/wiki/Yen%27s_algorithm">Yen's Algorithm</a>.
#
# \section install_sec Description
#
# The algorithm can be broken down into two parts, determining the first k-shortest path, \f$A^1\f$, and then determining all other k-shortest paths. It is assumed that the container \f$A\f$ will hold the k-shortest path, whereas the container \f$B\f$, will hold the potential k-shortest paths. To determine \f$A^1\f$, the shortest path from the source to the sink, any efficient shortest path algorithm can be used.
#
# To find the \f$A^k\f$, where \f$k\f$ ranges from \f$2\f$ to \f$K\f$, the algorithm assumes that all paths from \f$A^1\f$ to \f$A^{k-1}\f$ have previously been found. The \f$k\f$ iteration can be divided into two processes, finding all the deviations \f${A^k}_i\f$ and choosing a minimum length path to become \f$A^k\f$. Note that in this iteration, \f$i\f$ ranges from \f$1\f$ to \f${Q^k}_k\f$.
#
# The first process can be further subdivided into three operations, choosing the \f${R^k}_i\f$, finding \f${S^k}_i\f$, and then adding \f${A^k}_i\f$ to the container \f$B\f$. The root path, \f${R^k}_i\f$, is chosen by finding the subpath in \f$A^{k-1}\f$ that follows the first i nodes of \f$A^{j}\f$, where \f$j\f$ ranges from \f$1\f$ to \f$k-1\f$. Then, if a path is found, the cost of edge \f$d_{i(i+1)}\f$ of \f$A^{j}\f$ is set to infinity. Next, the spur path, \f${S^k}_i\f$, is found by computing the shortest path from the spur node, node \f$i\f$, to the sink. The removal of previous used edges from \f$(i)\f$ to \f$(i + 1)\f$ ensures that the spur path is different. \f${A^k}_i = {R^k}_i + {S^k}_i\f$, the addition of the root path and the spur path, is added to \f$B\f$. Next, the edges that were removed, i.e. had their cost set to infinity, are restored to their initial values.
#
# The second process determines a suitable path for \f$A^k\f$ by finding the path in container \f$B\f$ with the lowest cost. This path is removed from container be and inserted into container \f$A\f$ and the algorithm continues to the next iteration. Note that if the amount of paths in container \f$B\f$ equal or exceed the amount of k-shortest paths that still need to be found, then the necessary paths of container \f$B\f$ is added to container \f$A\f$ and the algorithm is finished.
#
# \section example_sec Example
#
# \image html YenKSP-K3-CH.gif
#
# The example uses Yen's K-Shortest Path Algorithm to compute three paths from \f$(C)\f$ to \f$(H)\f$. Dijkstra's algorithm is used to calculate the best path from \f$(C)\f$ to \f$(H)\f$, which is \f$(C)-(E)-(F)-(H)\f$ with cost 5. This path is appended to container \f$A\f$ and becomes the first k-shortest path, \f$A^1\f$. 
# 
# Node \f$(C)\f$ of \f$A^1\f$ becomes the spur node with a root path of itself, \f${R^2}_1 = (C)\f$. The edge, \f$(C)-(E)\f$, is removed because it coincides with the root path and a path in container \f$A\f$. Dijkstra's algorithm is used to compute the spur path \f${S^2}_1\f$, which is \f$(C)-(D)-(F)-(H)\f$, with a cost of 8. \f${A^2}_1 = {R^2}_1 + {S^2}_1 = (C)-(D)-(F)-(H)\f$ is added to container \f$B\f$ as a potential k-shortest path.
#
# Node \f$(E)\f$ of \f$A^1\f$ becomes the spur node with \f${R^2}_2 = (C)-(E)\f$. The edge, \f$(E)-(F)\f$, is removed because it coincides with the root path and a path in container \f$A\f$. Dijkstra's algorithm is used to compute the spur path \f${S^2}_2\f$, which is \f$(E)-(G)-(H)\f$, with a cost of 7. \f${A^2}_2 = {R^2}_2 + {S^2}_2 = (C)-(E)-(G)-(H)\f$ is added to container \f$B\f$ as a potential k-shortest path.
# 
# Node \f$(F)\f$ of \f$A^1\f$ becomes the spur node with a root path, \f${R^2}_3 = (C)-(E)-(F)\f$. The edge, \f$(F)-(H)\f$, is removed because it coincides with the root path and a path in container \f$A\f$. Dijkstra's algorithm is used to compute the spur path \f${S^2}_3\f$, which is \f$(F)-(G)-(H)\f$, with a cost of 8. \f${A^2}_3 = {R^2}_3 + {S^2}_3 = (C)-(E)-(F)-(G)-(H)\f$ is added to container \f$B\f$ as a potential k-shortest path.
# 
# Of the three paths in container B, \f${A^2}_2\f$ is chosen to become \f$A^2\f$ because it has the lowest cost of 7. This process is continued to the 3rd k-shortest path. However, within this 3rd iteration, note that some spur paths do not exist, and the path that is chosen to become \f$A^3\f$ was found within the 2nd iteration, namely \f${A^2}_2  = (C)-(E)-(G)-(H)\f$.
# 
# \section features_sec Features
# \subsection sub_space Space complexity
# To store the edges of the graph, the shortest path list \f$A\f$, and the potential shortest path list \f$B\f$, \f$N^2 + KN\f$ memory addresses are required.<ref name=yenksp2 /> At worse case, the every node in the graph has an edge to every other node in the graph, thus \f$N^2\f$ addresses are needed. Only \f$KN\f$ addresses are need for both list \f$A\f$ and \f$B\f$ because at most only \f$K\f$ paths will be stored, where it is possible for each path to have \f$N\f$ nodes.
# 
# \subsection sub_time Time complexity
# The time complexity of Yen's algorithm is dependent on the shortest path algorithm used in the computation of the spur paths, so the Dijkstra algorithm is assumed. Dijkstra's algorithm has a worse case time complexity of \f$O(N^2)\f$, but using a Fibonacci heap it becomes \f$O(M + N\log N)\f$, where \f$M\f$ is the amount of edges in the graph. Since Yen's algorithm makes \f$K\f$ calls to the Dijkstra in computing the spur paths, the time complexity becomes \f$O(KN(M + N\log N))\f$.
#
def main():
    # Load the graph
    G = DiGraph("net5")
    
    # Get the painting object and set its properties.
    paint = G.painter()
    paint.set_source_sink("C", "H")
    paint.set_rank_same(['C', 'D', 'F'])
    paint.set_rank_same(['E', 'G', 'H'])
    
    # Generate the graph using the painter we configured.
    G.export(False, paint)
    
    # Get 30 shortest paths from the graph.
    items = algorithms.ksp_yen(G, "C", "H", 30)
    for path in items:
        print "Cost:%s\t%s" % (path['cost'], "->".join(path['path']))
          
    return 0


if __name__ == "__main__":
    main()
