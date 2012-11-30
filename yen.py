#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  yen.py
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
import graph
import dijkstra


## @package YenKSP
# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971 and implores any shortest path algorithm to find the best path, then proceeds to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval Array of paths, where [0] is the shortest, [1] is the next shortest, and so on.
def yenKSP(graph, start, end, K=2):
	distances, previous = self.m_dijkstra.calculate(self.m_graph, start)
	
	A = [self.m_dijkstra.path(previous, start, end)]
	B = []
	
	for k in range(1, K):
		for i in range(0, len(A[0]) - 1):
			spurNode = A[k-1][i]
			rootPath = A[k-1][:i+1]
			
			edgesRemoved = []
			for kPath in A:
				if rootPath == kPath[:i+1]:
					val = self.m_graph.removeLink(kPath[i], kPath[i+1])
					if val == -1:
						continue
					edgesRemoved.append([kPath[i], kPath[i+1], val])
			
			dist, prev = self.m_dijkstra.calculate(self.m_graph, spurNode, end)
			spurPath = self.m_dijkstra.path(prev, spurNode, end)
			
			if spurPath:
				totalPath = rootPath[:-1] + spurPath
				totalDist = distances[spurNode] + dist[end]
			
				if not ({totalDist:totalPath} in B):
					B.append({totalDist:totalPath})
			
			for edge in edgesRemoved:
				self.m_graph.addLink(edge[0], edge[1], edge[2])
		
		B.sort()
		if len(B):
			A.append(B[0].values()[0])
			B.pop(0)
		else:
			break
	
	return A

def main():
	G = graph.Graph("0");
	G.load()
	
	print yenKSP(G, "C", "H", 2)
	
	return 0


if __name__ == '__main__':
	main()
