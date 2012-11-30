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
import os


class Yen:
	m_graph = {}
	m_dijkstra = None
	
	def __init__(self, graph=None):
		if graph:
			self.m_graph = graph
		
		self.m_dijkstra = dijkstra.Dijkstra()
		
		return
	
	def setGraph(self, graph):
		self.m_graph = graph
		
		return
	
	def calculate(self, start, end, K=2):
		# Show the initial graph.
		self.m_graph.m_gviz.clearLegendText()
		self.m_graph.m_gviz.setLegendColor("#000000")
		self.m_graph.m_gviz.addLegendText("YenKSP(%s, %s, %s)" % (start, end, K))
		self.export(2)
		
		distances, previous = self.m_dijkstra.calculate(self.m_graph, start)
		
#		for k,v in distances.iteritems():
#			print k, "=", v, "\t<-", previous[k]
		
		A = [self.m_dijkstra.path(previous, start, end)]
		B = []
		
		# Show the best path, A[0], node by node
		for i in range(0, len(A[0])):
			self.m_graph.m_gviz.setPath("".join(A[0][:i+1]), "#3465a4", "#204a87")
			self.m_graph.m_gviz.setLegendColor("#204a87")
			self.m_graph.m_gviz.clearLegendText()
			self.m_graph.m_gviz.addLegendText("Dijkstra: %s" % ",".join(A[0][:i+1]))
			self.export()
		
		# Show the best path, A[0]
		self.m_graph.m_gviz.setPath("".join(A[0]), "#3465a4", "#204a87")
		self.m_graph.m_gviz.setLegendColor("#204a87")
		self.m_graph.m_gviz.clearLegendText()
		self.m_graph.m_gviz.addLegendText("1st Shortest Path:")
		self.m_graph.m_gviz.addLegendText("A[1]= %s (%s)" % (",".join(A[0]), distances[end]))
		self.export(2)
		
#		print distances[end], A[0]
		
		for k in range(1, K):
#			print k + 1, "th Path:"
			for i in range(0, len(A[0]) - 1):
				self.m_graph.m_gviz.clearInfinity()
				self.m_graph.m_gviz.clearPath()
				self.m_graph.m_gviz.clearLegendText()
				self.m_graph.m_gviz.setLegendColor("white")
				numS = int(self.m_graph.m_name)
				flagS = True
				
				spurNode = A[k-1][i]
				rootPath = A[k-1][:i+1]
#				print "\tspurNode:", spurNode, "\n\trootPath:", rootPath
				
				# Show all the k-shortest paths so far.
				self.m_graph.m_gviz.clearLegendText()
				self.m_graph.m_gviz.addLegendText("A so far:")
				self.m_graph.m_gviz.setLegendColor("#204a87")
				for j in range(0, len(A)):
					apath = A[j]
					self.m_graph.m_gviz.setPath("".join(apath), "#3465a4", "#204a87")
					if j < 3:
						if j == 0:
							self.m_graph.m_gviz.addLegendText("A = %s" % ",".join(apath))
						else:
							self.m_graph.m_gviz.addLegendText("    %s" % ",".join(apath))
				self.export()
				
				# Show root path and spur node
				self.m_graph.m_gviz.setPath("".join(rootPath), "#73d216", "#4e9a06")
				self.m_graph.m_gviz.setPath(spurNode, "#75507b", "#5c3566")
				self.m_graph.m_gviz.clearLegendText()
				self.m_graph.m_gviz.setLegendColor("#000000")
				self.m_graph.m_gviz.addLegendText("Root Path: %s" % (",".join(rootPath)))
				self.m_graph.m_gviz.addLegendText("Spur Node: %s" % spurNode)
				self.export(2)
				
				edgesRemoved = []
				for kPath in A:
					if rootPath == kPath[:i+1]:
						val = self.m_graph.removeLink(kPath[i], kPath[i+1])
						if val == -1:
							continue
#						print "\t\tRemove: %s -> %s (%d)" % (kPath[i], kPath[i+1], val)
						edgesRemoved.append([kPath[i], kPath[i+1], val])
						self.m_graph.m_gviz.setInfinity(kPath[i], kPath[i+1])
				
				# Show the removed edges.
				if edgesRemoved:
					self.m_graph.m_gviz.clearLegendText()
					self.m_graph.m_gviz.setLegendColor("#ef2929")
					self.m_graph.m_gviz.addLegendText("Removing links.")
					self.export()
				
				dist, prev = self.m_dijkstra.calculate(self.m_graph, spurNode, end)
				spurPath = self.m_dijkstra.path(prev, spurNode, end)
				
				# Show the spur path.
				if spurPath:
#					print "\tspurPath:", spurPath
					totalPath = rootPath[:-1] + spurPath
					totalDist = distances[spurNode] + dist[end]
					
					if not ({totalDist:totalPath} in B):
						self.m_graph.m_gviz.clearPath()
						self.m_graph.m_gviz.setPath("".join(rootPath), "#73d216", "#4e9a06")
						self.m_graph.m_gviz.setLegendColor("#75507b")
						for j in range(0, len(spurPath)):
							self.m_graph.m_gviz.setPath("".join(spurPath[:j+1]), "#75507b", "#5c3566")
							self.m_graph.m_gviz.clearLegendText()
							self.m_graph.m_gviz.addLegendText("Spur Path = %s" % ",".join(spurPath[:j+1]))
							self.export()
						
						self.m_graph.m_gviz.clearPath()
						self.m_graph.m_gviz.setPath("".join(rootPath), "#73d216", "#4e9a06")
						self.m_graph.m_gviz.setPath("".join(spurPath), "#75507b", "#5c3566")
						self.m_graph.m_gviz.clearLegendText()
						self.m_graph.m_gviz.setLegendColor("#75507b")
						
						if len(B) > 3:
							for j in range(0, 2):
								self.m_graph.m_gviz.addLegendText("B  = %s (%s)" % (",".join(B[j].values()[0]), (B[j].keys()[0])))
						else:
							for j in range(0, len(B)):
								self.m_graph.m_gviz.addLegendText("B  = %s (%s)" % (",".join(B[j].values()[0]), (B[j].keys()[0])))
						
						self.m_graph.m_gviz.addLegendText("B += %s (%s)" % (",".join(rootPath[:-1] + spurPath), distances[spurNode] + dist[end]))
						self.export(2)
						
						B.append({totalDist:totalPath})
					else:
						flagS = False
				else:
					flagS = False
				
				if not flagS:
					numE = int(self.m_graph.m_name)
					
					for num in range(numS+1, numE+1):
						os.remove("data/gif/%s.dot" % num)
						os.remove("data/gif/%s.png" % num)
					
					self.m_graph.setName(str(numS))
					
					self.m_graph.m_gviz.clearLegendText()
					self.m_graph.m_gviz.setLegendColor("black")
					self.m_graph.m_gviz.addLegendText("No unique Spur Path")
					self.m_graph.m_gviz.addLegendText("can be found.")
					self.export(2)
				
				for edge in edgesRemoved:
					self.m_graph.addLink(edge[0], edge[1], edge[2])
				
				
				
			B.sort()
			if len(B):
#				print B[0]
				
				# Show the kth shortest path.
				self.m_graph.m_gviz.clearPath()
				self.m_graph.m_gviz.clearInfinity()
				self.m_graph.m_gviz.setPath("".join(B[0].values()[0]), "#3465a4", "#204a87")
				self.m_graph.m_gviz.setLegendColor("#204a87")
				self.m_graph.m_gviz.clearLegendText()
				self.m_graph.m_gviz.addLegendText("A[%s]= %s (%s)" % (k+1, ",".join(B[0].values()[0]), B[0].keys()[0]))
				self.export(2)
				
				A.append(B[0].values()[0])
				B.pop(0)
				
			else:
				break
		
		self.export()
		
		print "\nK-Shortest Paths:"
		for i in A:
			print i
		
		# Show all the k-shortest paths so far.
		self.m_graph.m_gviz.clearLegendText()
		self.m_graph.m_gviz.clearPath()
		self.m_graph.m_gviz.addLegendText("Finished:")
		self.m_graph.m_gviz.setLegendColor("#204a87")
		for j in range(0, len(A)):
			apath = A[j]
			if j < 3:
				if j == 0:
					self.m_graph.m_gviz.addLegendText("A = %s" % ",".join(apath))
				else:
					self.m_graph.m_gviz.addLegendText("    %s" % ",".join(apath))
		self.export(3)
		
		return
	
	def export(self, amount=1):
		amount=1
		for x in range(0, amount):
			self.m_graph.setName()
			self.m_graph.export2()
		
		return

def main():
	G = graph.Graph("0");
	G.load()
	
	G.m_gviz.setSourceSink("C", "H")
	G.m_gviz.setRank(['C', 'D', 'F'])
	G.m_gviz.setRank(['E', 'G', 'H'])
	
	Y = Yen(G)
	Y.calculate("C", "H", 3)
	
#	G = graph.Graph("graph");
#	G.load()
#	
#	Y = Yen(G)
#	Y.calculate("N0", "N5", 40)
	
	return 0


if __name__ == '__main__':
	main()
