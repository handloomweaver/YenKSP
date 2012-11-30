#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  graph.py
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
import json
import random
import graphviz
import graphviz2


class Graph:
	m_name = ""
	m_graph = {}
	
	m_dirWorking = "data/"
	
	m_gviz = None

	def __init__(self, name):
		self.m_name = name
		
		self.m_gviz = graphviz2.Graphviz2()
		return

	def __getitem__(self, index):
		return self.m_graph[index]

	def __iter__(self):
		return self.m_graph.__iter__();

	def keys(self):
		return self.m_graph.keys();

	def addNode(self, node):
		if self.m_graph.has_key(node):
			return False

		self.m_graph[node] = {}
		return True

	def addLink(self, nodeFrom, nodeTo, cost=None):
		if not cost:
			cost = random.randrange(0, 5) + 1
		
		self.addNode(nodeFrom)
		self.addNode(nodeTo)
		
		self.m_graph[nodeFrom][nodeTo] = cost
		return

	def removeLink(self, nodeFrom, nodeTo, cost=None):
		if not self.m_graph.has_key(nodeFrom) or not self.m_graph.has_key(nodeTo):
			return -1
		
		if self.m_graph[nodeFrom].has_key(nodeTo):
			if not cost:
				cost = self.m_graph[nodeFrom][nodeTo]
#				del self.m_graph[nodeFrom][nodeTo]
				
				if cost == 10000:
					return -1
				else:
					self.m_graph[nodeFrom][nodeTo] = 10000
					return cost
			elif self.m_graph[nodeFrom][nodeTo] == cost:
#				del self.m_graph[nodeFrom][nodeTo]
				self.m_graph[nodeFrom][nodeTo] = 10000
				
				return cost
			else:
				return -1
		else:
			return -1
	
	def load(self, name=None):
		if not name:
			name = self.m_name
		
		pathJson = "%s%s.json" % (self.m_dirWorking, name)
		if not os.path.exists(pathJson):
			return False
		
		fhandle = open(pathJson, 'r')
		self.m_graph = json.loads(fhandle.read())
		fhandle.close()
		
		return
	
	def save(self):
		if not os.path.exists(self.m_dirWorking):
			os.mkdir(self.m_dirWorking)
		
		fhandle = open("%s%s.json" % (self.m_dirWorking, self.m_name), 'w')
		fhandle.write(json.dumps(self.m_graph))
		fhandle.close()
		
		return
	
	def export(self, source=None, sink=None):
		grapher = graphviz.Graphviz()
		grapher.generate(self.m_name, self.m_graph, source, sink)
		
		return
	
	def export2(self):
		self.m_gviz.setGraph(self.m_graph)
		self.m_gviz.generate(self.m_name)
		
		return
	
	def random(self, numNodes, numEdges, maxCost):
		self.m_graph = {}
		
		for node in range(numNodes):
			nameNode = "N%d" % node
			self.addNode(nameNode)
		
		for edge in range(numEdges):
			fromNode = random.choice(self.m_graph.keys())
			
			toNode = fromNode
			while toNode == fromNode: # or self.m_graph[fromNode].has_key(toNode):
				toNode = random.choice(self.m_graph.keys())
			
			cost = random.randrange(0, maxCost) + 1
			self.addLink(fromNode, toNode, cost)
		
		return
	
	def setName(self, name=None):
		if not name:
			name = int(self.m_name) + 1
		
		self.m_name = name
		
		return


def main():
	G = Graph("0")
#	G.addLink("A", "B")
#	G.addLink("A", "C")
#	G.addLink("A", "D")
#	
#	G.addLink("B", "C")
#	
#	G.addLink("C", "D")
#	G.addLink("C", "F")
#	
#	G.addLink("D", "F")
#	
#	G.addLink("E", "A")
#	G.addLink("E", "B")
#	
#	G.save()
	G.load()
	G.export()
	
	return 0


if __name__ == '__main__':
	main()
