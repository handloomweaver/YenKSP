#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dijkstra.py
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
#  http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/ 
# 
from prioritydictionary import priorityDictionary


class Dijkstra:

	def __init__(self):
		return
	
	def calculate(self, graph, start, end=None):
		distances = {}		# dictionary of final distances
		previous = {}		# dictionary of predecessors
		Q = priorityDictionary()
		
		infinity = 10000
		undefined = None
		
		for v in graph:
			distances[v] = infinity
			previous[v] = undefined
			Q[v] = infinity
		
		distances[start] = 0
		Q[start] = 0
		
		for v in Q:
			if v == end: break
			
#			print "graph %s(%d) " % (v, distances[v]),  graph[v]
			for u in graph[v]:
				vuLength = distances[v] + graph[v][u]
				
#				print "\tlink %s(%d) vu=%d" % (u, distances[u], vuLength)
				if vuLength < distances[u]:
					distances[u] = vuLength
					Q[u] = vuLength
					previous[u] = v
	
		return (distances, previous)
	
	def path(self, previous, start, end):
		k = [end]
		
		p = end
		while p != start:
			if previous.has_key(p):
				p = previous[p]
				k.append(p)
			else:
				return None
		
		k.reverse()
		return k
		

def main():
	
	return 0


if __name__ == '__main__':
	main()
