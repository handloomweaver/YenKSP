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
from graphviz import Graphviz


## @brief Represents a directed graph of nodes and edges.
# 
# The directed graph is indentified with a supplied name and stored in the 
# "data/json/" folder if saved. Initially the graph contains zero nodes, but
# can be populated automatically by loading the data of the supplied name. The
# graph can also be randomly generated, or manually configured.
class DiGraph:
    ## The location that the graph data is stored as json objects.
    _directory_data = "data/json/"
    
    ## The Graphviz object that will be used to display the graph.
    _painter = None
    
    ## An edge with this cost signifies that it has been removed from the graph.
    # This value implies that any edge in the graph must be very small in 
    # comparison.
    INFINITY = 10000
    
    ## Represents a NULL predecessor.
    UNDEFINDED = None
    
    ## Specifies the identifier for the graph.
    _name = "graph"
    
    ## The dictionary of the graph. Each key represents a node and the value of
    # the associated node is a dictionary of all the edges. The key of the edges
    # dictionary is the node the edge terminates at and the value is the cost of
    # the edge.
    _data = {}
    
    ## Initializes the graph with an indentifier and Graphviz object.
    #    
    # @post The graph will contain the data specified by the identifier, if that
    # data exist. If not, then the graph will be empty.
    #
    # @param self The object pointer.
    # @param name The identifier for the graph by which the data is stored as or
    # will be stored as.
    # 
    def __init__(self, name=None):
        if name:
            self._name = name
        
        self.load()
        
        self._painter = Graphviz()
        return

    ## Gets the edges of a specified node.
    #
    # @param self The object pointer.
    # @param node The node whose edges are being queried.
    # @retval {} A dictionary of the edges and thier cost if the node exist 
    # within the graph or None if the node is not in the graph.
    #
    def __getitem__(self, node):
        if self._data.has_key(node):
            return self._data[node]
        else:
            return None

    ## Iterator for the digraph object.
    #
    # @param self The object pointer.
    # @retval iter An iterator that can be used to process each node of the 
    # graph.
    #
    def __iter__(self):
        return self._data.__iter__()

    ## Adds a node to the graph.
    #
    # @param self The object pointer.
    # @param node The name of the node that is to be added to the graph.
    # @retval bool True if the node was added or False if the node already 
    # existed in the graph.
    #
    def add_node(self, node):
        if self._data.has_key(node):
            return False

        self._data[node] = {}
        return True

    ## Adds a edge to the graph.
    #
    # @post The two nodes specified exist within the graph and their exist an
    # edge between them of the specified value.
    #
    # @param self The object pointer.
    # @param node_from The node that the edge starts at.
    # @param node_to The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified a random
    # cost is generated from 1 to 10.
    #
    def add_edge(self, node_from, node_to, cost=None):
        if not cost:
            cost = random.randrange(1, 11)
        
        self.add_node(node_from)
        self.add_node(node_to)
        
        self._data[node_from][node_to] = cost
        return

    ## Removes an edge from the graph.
    #
    # @param self The object pointer.
    # @param node_from The node that the edge starts at.
    # @param node_to The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified all edges
    # between the nodes are removed.
    # @retval int The cost of the edge that was removed. If the nodes of the 
    # edge does not exist, or the cost of the edge was found to be infinity, or 
    # if the specified edge does not exist, then -1 is returned.
    #
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
    
    ## Populates the graph with the data of the graph indentifier.
    #
    # @pre The _name variable has been set and there exist a ".json" file at
    # the directory specified by _directory_data with the graph data.
    # @post The _data dictionary will contain all the nodes and edges of the 
    # graph.
    #
    # @param self The object pointer.
    # @retval bool True if the graph was populated from the specified file, 
    # False otherwise.
    # 
    def load(self):
        path_json = "%s%s.json" % (self._directory_data, self._name)
        if not os.path.exists(path_json):
            return False
        
        fhandle = open(path_json, 'r')
        self._data = json.loads(fhandle.read())
        fhandle.close()
        
        return True
    
    ## Stores the nodes and edges of the graph.
    #
    # @pre The _name variable has been set and the _data dictionary contains all
    # the nodes and edges of the graph.
    # @post There exist a ".json" file at the directory specified by 
    # _directory_data with the graph data.
    # 
    # @param self The object pointer.
    # 
    def save(self):
        if not os.path.exists(self._directory_data):
            os.mkdir(self._directory_data)
        
        fhandle = open("%s%s.json" % (self._directory_data, self._name), 'w')
        fhandle.write(json.dumps(self._data))
        fhandle.close()
        
        return
    
    ## Generates an image of the graph.
    #
    # @pre The _name variable has been set and the _data dictionary contains all
    # the nodes and edges of the graph.
    # @post There exist a ".png" file at the directory specified by Graphviz 
    # with the graph image.
    #
    # @param frames Denotes whether the generated image will be a frame in a set
    # of multiple images. 
    # @param painter A new Graphviz object to paint the graph with.
    # 
    def export(self, frames=False, painter=None):
        if not painter:
            painter = self._painter
        
        painter.set_graph(self._data)
        painter.generate(self._name, frames)
        
        return
    
    ## Populates the graph with random data.
    #
    # @post The _data dictionary will contain all the nodes and edges of the 
    # graph.
    #
    # @param self The object pointer.
    # @param num_nodes The amount of nodes the graph should contain.
    # @param num_edges The amount of edges the graph should contain.
    # @param max_cost The maximum cost of any edge in the graph.
    # 
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
    
    ## Sets the graph indentifier.
    #    
    # @post The _name variable will contain the specified name.
    #
    # @param self The object pointer.
    # @param name The identifier for the graph by which the data is stored as or
    # will be stored as.
    # @retval bool True is the name was set, False otherwise.
    # 
    def set_name(self, name):
        if name:
            self._name = name
        
            return True
        else:
            return False
    
    ## The reference to the Graphviz object.
    #    
    # @pre The _painter variable has been initialized with the Graphviz object.
    #
    # @param self The object pointer.
    # @retval Graphviz The Graphviz object used by the graph.
    #
    def painter(self):
        return self._painter

