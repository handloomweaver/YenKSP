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
import codecs


class Graphviz2:
	m_dirWorking	= "data/gif/"
	m_template		= "template.dot"
	
	m_formatBody	= None
	m_formatNode	= "\"%s\" [color=\"%s\"]"
	m_formatEdge	= "\"%s\" -> \"%s\" [label=\"%s\"%s]"
	
	m_formatRankSame	= "{ rank=same; %s }"
	m_formatRankSource	= "\"%s\" [rank=\"source\"]"
	m_formatRankSink	= "\"%s\" [rank=\"sink\"]"
	
	m_formatInfinity	= "#ef2929"
	m_formatLegend		= "%-20s"
	
	m_infinity = 10000
	
	m_graph				= None
	m_containerPaths	= [] # [{ path: "", colorNode: "", colorEdge:""}, {}]
	m_containerRanks	= [] # [['A','B','C'],[]]
	m_containerInfinity	= [] # ["", ""]
	m_nodeSource		= None
	m_nodeSink			= None
	m_legendText		= [] # ["", ""]
	m_legendColor		= "white"
	
	def __init__(self):
		self.setup()
		return
	
	def setup(self):
		path = self.m_dirWorking + self.m_template
		
		if not os.path.exists(path):
			return False
		
		fhandle = open(path, 'r')
		self.m_formatBody = fhandle.read()
		fhandle.close()
		
		return True
	
	def reset(self):
		self.m_graph				= None
		self.m_containerPaths		= []
		self.m_containerRanks		= []
		self.m_containerInfinity	= []
		self.m_nodeSource			= None
		self.m_nodeSink				= None
		self.m_legendText			= []
		
		return
	
	def setGraph(self, graph):
		self.m_graph = graph
		
		return
	
	def setRank(self, arrNodes):
		self.m_containerRanks.append(arrNodes)
		
		return
	
	def setPath(self, strNodes, colorNode, colorEdge):
		self.m_containerPaths.append({'path':strNodes, 'colorNode': colorNode, 'colorEdge': colorEdge})
		
		return
	
	def clearPath(self):
		self.m_containerPaths = []
		
		return
	
	def setInfinity(self, node, toNode):
		self.m_containerInfinity.append(node + toNode)
		
		return
	
	def clearInfinity(self):
		self.m_containerInfinity = []
		
		return
	
	def setSourceSink(self, source, sink):
		self.m_nodeSource = source
		self.m_nodeSink = sink
		
		return
	
	def setLegendColor(self, color):
		self.m_legendColor = color
		
		return
	
	def addLegendText(self, text):
		self.m_legendText.append(text)
		
		return
	
	def clearLegendText(self):
		self.m_legendText = []
		
		return
	
	def generate(self, name):
		self.createDot(name)
		self.createImage(name)
		
		return
	
	def createDot(self, name):
		if not os.path.exists(self.m_dirWorking):
			os.mkdir(self.m_dirWorking)
		
		fhandle = codecs.open("%s%s.dot" % (self.m_dirWorking, name), encoding='utf-8', mode='w')
		
		fields = self.parseGraph()
		fields.append(self.parseRank())
		fields.append(self.parseSourceSink())
		fields.append(self.m_legendColor)
		fields.extend(self.parseLegend())
		
		body = self.m_formatBody % tuple(fields)
		fhandle.write(body)
		
		fhandle.close()
		
		return 
	
	def createImage(self, name, itype=None):
		if not itype:
			itype = "dot"
		
		pathDot = "%s%s.dot" % (self.m_dirWorking, name)
		pathPng = "%s%s.png" % (self.m_dirWorking, name)
		
		if not os.path.exists(pathDot):
			return False
		
		cmd = "%s %s -Tpng -o %s" % (itype, pathDot, pathPng)
		if os.system(cmd) == 0:
			return True
		else:
			return False
	
	def parseGraph(self):
		nodes = ""
		edges = ""
		
		for node,nitems in self.m_graph.iteritems():
			nodes = nodes + self.m_formatNode % (node, self.findNodeColor(node)) + "\n\t"
			
			for toNode,cost in nitems.iteritems():
				if (node + toNode) in self.m_containerInfinity:
					temp = self.m_formatEdge % (node, toNode, u"∞", "style=dashed, color=\"%s\"" % self.m_formatInfinity)
				else:
					temp = self.m_formatEdge % (node, toNode, cost, self.findEdgeColor(node, toNode))
				
				if temp in edges:
					continue
				
				edges += temp + "\n\t"
		
		return [nodes, edges]
	
	def parseRank(self):
		rank = ""
		for nodes in self.m_containerRanks:
			rank += self.m_formatRankSame % ("\"%s\"" % "\" \"".join(nodes)) + "\n\t"
		
		return rank
	
	def parseSourceSink(self):
		ss = ""
		if self.m_nodeSource:
			ss += self.m_formatRankSource % self.m_nodeSource + "\n\t"
		
		if self.m_nodeSink:
			ss += self.m_formatRankSink % self.m_nodeSink + "\n"
		
		return ss
	
	def parseLegend(self):
		legend = []
		for i in range(0, 4):
			if i < len(self.m_legendText):
				legend.append(self.m_formatLegend % self.m_legendText[i])
			else:
				legend.append(self.m_formatLegend % "")
		
		return legend
	
	def findNodeColor(self, node):
		color = ""
		for pathInfo in self.m_containerPaths:
			if node in pathInfo['path']:
				color = pathInfo['colorNode']
		
		return color
	
	def findEdgeColor(self, node, toNode):
		color = ""
		edge = "%s%s" % (node, toNode)
		for pathInfo in self.m_containerPaths:
			if edge in pathInfo['path']:
				color = ", penwidth=2, color=\"%s\"" % pathInfo['colorEdge']
		
		return color


def main():
	print "Usage: Use with the Graph class."
	return 0


if __name__ == '__main__':
	main()
