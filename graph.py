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
from graphviz2 import Graphviz2


class DiGraph:
    _directoryData  = "data/"
    _painter        = None
    
    INFINITY = 10000
    UNDEFINDED = None
    
    _name = "graph"
    _data = {}
    

    def __init__(self, name=None):
        if name:
            self._name = name
        
        self._painter = Graphviz2()
        return

    def __getitem__(self, index):
        return self._data[index]

    def __iter__(self):
        return self._data.__iter__();

    def keys(self):
        return self._data.keys();

    def add_node(self, node):
        if self._data.has_key(node):
            return False

        self._data[node] = {}
        return True

    def add_edge(self, node_from, node_to, cost=None):
        if not cost:
            cost = random.randrange(1, 11)
        
        self.add_node(node_from)
        self.add_node(node_to)
        
        self._data[node_from][node_to] = cost
        return

    def remove_edge(self, node_from, node_to, cost=None):
        if not self._data.has_key(node_from):
            return -1
        
        if self._data[node_from].has_key(node_to):
            if not cost:
                cost = self._data[node_from][node_to]
                
                if cost == self.INFINITY:
                    return -1
                else:
                    self._data[node_from][node_to] = self.INFINITY
                    return cost
            elif self._data[node_from][node_to] == cost:
                self._data[node_from][node_to] = self.INFINITY
                
                return cost
            else:
                return -1
        else:
            return -1
    
    def load(self, name=None):
        if not name:
            name = self._name
        
        path_json = "%s%s.json" % (self._directoryData, name)
        if not os.path.exists(path_json):
            return False
        
        fhandle = open(path_json, 'r')
        self._data = json.loads(fhandle.read())
        fhandle.close()
        
        return True
    
    def save(self):
        if not os.path.exists(self._directoryData):
            os.mkdir(self._directoryData)
        
        fhandle = open("%s%s.json" % (self._directoryData, self._name), 'w')
        fhandle.write(json.dumps(self._data))
        fhandle.close()
        
        return
    
    def export(self, frames=False):
        self._painter.setGraph(self._data)
        self._painter.generate(self._name, frames)
        
        return
    
    def random(self, num_nodes, num_edges, max_cost):
        self._data = {}
        
        for node in range(num_nodes):
            self.add_node("N%d" % node)
        
        for edge in range(num_edges):
            node_from = random.choice(self._data.keys())
            
            node_to = node_from
            while node_to == node_from:
                node_to = random.choice(self._data.keys())
            
            cost = random.randrange(0, max_cost) + 1
            self.add_edge(node_from, node_to, cost)
        
        return
    
    def set_name(self, name):
        if name:
            self._name = name
        
            return True
        else:
            return False


def main():
    G = Graph("0")
#   G.add_edge("A", "B")
#   G.add_edge("A", "C")
#   G.add_edge("A", "D")
#   
#   G.add_edge("B", "C")
#   
#   G.add_edge("C", "D")
#   G.add_edge("C", "F")
#   
#   G.add_edge("D", "F")
#   
#   G.add_edge("E", "A")
#   G.add_edge("E", "B")
#   
#   G.save()
    G.load()
    G.export()
    
    return 0


if __name__ == '__main__':
    main()
