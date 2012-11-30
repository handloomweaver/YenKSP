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


class PriorityQueue:
	m_queue = []
	m_dictionary = {}
	
	def __init__(self):
		
		return

	def __getitem__(self, index):
		if self.m_dictionary.has_key(index):
			return self.m_dictionary[index]
		else:
			return 10000

	def empty(self):
		if len(self.m_queue) == 0:
			return True
		else:
			return False

	def put(self, priority, item):
		if self.m_dictionary.has_key(item):
			self.m_queue.remove({self.m_dictionary[item]:item})
			self.m_queue.append({priority:item})
			self.m_queue.sort()			
			
			self.m_dictionary[item] = priority
		else:
			self.m_queue.append({priority:item})
			self.m_queue.sort()
		
			self.m_dictionary[item] = priority
		return 
		
	def get(self):
		items = self.m_queue[0]
		
		priority = items.keys()[0]
		item = items[priority]
		
		del self.m_queue[0]
		del self.m_dictionary[item]
		
		
		return priority, item


class Dijkstra:

	def __init__(self):
	
		return
	
	def calculate(self, graph, start, end=None):
		distances = {}		# dictionary of final distances
		previous = {}		# dictionary of predecessors
		Q = priorityDictionary()
		Q[start] = 0
	
		for v in Q:
			distances[v] = Q[v]
			if v == end: break
		
			for u in graph[v]:
				vuLength = distances[v] + graph[v][u]
				
				if  u in distances:
					if vuLength < distances[u]:
						continue
				elif u not in Q or vuLength < Q[u]:
					Q[u] = vuLength
					previous[u] = v
	
		return (distances, previous)
	
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
		
		Q[start] = 0
		
		for v in Q:
			distances[v] = Q[v]
			if v == end: break
			
			for u in graph[v]:
				vuLength = distances[v] + graph[v][u]
				
				if vuLength < distances[u]:
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
