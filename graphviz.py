#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  graphviz.py
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
import os


class Graphviz:
	m_dirWorking = "data/"
	
	m_header = "digraph network { rankdir=LR; \n\t%s \n\t%s \n}"
	m_nodes = "\"%s\" [penwidth=1, shape=circle]"
	m_edges = "\"%s\" -> \"%s\" [label=\"%d\", constraint=false]"
	
	m_rankSource = "\"%s\" [penwidth=1, shape=circle, rank=\"source\"]"
	m_rankSink = "\"%s\" [penwidth=1, shape=circle rank=\"sink\"]"
	
	m_infinity = 10000
	m_infinityEdge = "\"%s\" -> \"%s\" [label=\"~\", color=\"red\"]"
	
	def __init__(self):
		return
	
	def generate(self, name, graph, source=None, sink=None):
		self.createDot(name, graph, source, sink)
		self.createImage(name)
		
		return
	
	def createDot(self, name, graph, source=None, sink=None):
		if not os.path.exists(self.m_dirWorking):
			os.mkdir(self.m_dirWorking)
		
		fhandle = open("%s%s.dot" % (self.m_dirWorking, name), 'w')
		
		items = self.parseGraph(graph, source, sink)
		body = self.m_header % (items[0], items[1])
		fhandle.write(body)
		
		fhandle.close()
		
		return 
	
	def createImage(self, name, itype=None):
		if not itype:
			itype = "circo"
		
		pathDot = "%s%s.dot" % (self.m_dirWorking, name)
		pathPng = "%s%s.png" % (self.m_dirWorking, name)
		
		if not os.path.exists(pathDot):
			return False
		
		cmd = "%s %s -Tpng -o %s" % (itype, pathDot, pathPng)
		if os.system(cmd) == 0:
			return True
		else:
			return False
	
	def parseGraph(self, graph, source=None, sink=None):
		nodes = ""
		edges = ""
		
		for node,nitems in graph.iteritems():
			if node == source:
				nodes = nodes + self.m_rankSource % node + "\n\t"
			elif node == sink:
				nodes = nodes + self.m_rankSink % node + "\n\t"
			else:
				nodes = nodes + self.m_nodes % node + "\n\t"
			
			for edge,cost in nitems.iteritems():
				temp = self.m_edges % (node, edge, cost)
				
				if temp in edges:
					continue
				
				edges = edges + temp + "\n\t"
		
		return [nodes, edges]


def main():
	print "Usage: Use with the Graph class."
	return 0


if __name__ == '__main__':
	main()
