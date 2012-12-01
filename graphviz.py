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


## @brief Generates images based on the Graph class.
# 
# Generates ".dot" markup files based on the directed graph and saves these 
# files to in the "data/dot/" folder, then generates an image based on the file 
# and stores the image in the "images/" folder.
#
class Graphviz:
    ## The location that the graph data is stored as dot markups.
    _directory_data = "data/dot/"    
    ## The location that the graph data is stored as images.
    _directory_images = "images/"    
    ## The location of the templates for the dot markup.
    _directory_templates = "data/templates/"
    ## The name of the template for the dot markup.
    _template_dot = "template.dot"
    
    ## The template for the entire dot markup.
    _format_body = None
    ## The template for each node in the dot markup.
    _format_node = "\"%s\" [color=\"%s\"]"
    ## The template for each edge in the dot markup.
    _format_edge = "\"%s\" -> \"%s\" [label=\"%s\"%s]"
    
    ## The template for nodes of the same rank in the dot markup.
    _format_rank_same = "{ rank=same; %s }"
    ## The template for the source node in the dot markup.
    _format_rank_source = "\"%s\" [rank=\"source\"]"
    ## The template for the sink node in the dot markup.
    _format_rank_sink = "\"%s\" [rank=\"sink\"]"
    
    ## Color to display edges with infinity cost in the dot markup.
    _format_infinity_color = "#ef2929"
    ## Color to paint the legend text.
    _format_legend_color = "white"
    ## The template for legend text in the dot markup.
    _format_legend_text = "%-20s"
    
    ## The data of the graph that is being processed.
    _graph = None
    
    ## Container for all the paths that are to be displayed.
    # The container is a list of dictionaries. Each dictionary has three key-
    # value pairs, path, colorNode, and colorEdge. Path is a string of the 
    # nodes in the path, where colorNode is the color to paint each node in the
    # path, and colorEdge is the color to paint each edge.
    # [{ path: "", colorNode: "", colorEdge:""}, {}]
    _container_paths = [] 
    
    ## Container for all the ranks that are to be displayed.
    # The container is a list of lists. Each sub list consist of the nodes that
    # share the same rank.
    # [['A','B','C'],[]]
    _container_ranks = []
    
    ## Container for all the edges that have infinity cost.
    # The container is a list of strings. Each string is the nodes that make up
    # the edge of infinite cost.
    # ["",""]
    _container_infinite = []
    
    ## The source node of the layout.    
    _node_source = None
    ## The sink node of the layout.
    _node_sink = None
    
    ## Container for the lines of legend text that are to be displayed.
    # The container is a list of strings, where each string is a line to be 
    # painted.
    # ["",""]
    _container_legend_text = []
    
    ## Frame number of the current image.
    _frame_num = 0
    
    ## Initializes the Graphviz painter with the dot template.
    #
    # @pre The template dot file exist in the template directory.
    # @post The format for the body of the dot graph will be set.
    #
    # @param self The object pointer.
    # 
    def __init__(self):
        path = "%s%s" % (self._directory_templates, self._template_dot)
        
        if os.path.exists(path):        
            fhandle = open(path, 'r')
            self._format_body = fhandle.read()
            fhandle.close()
        
        return
    
    ## Resets the painter to its default state.
    #    
    # @post The graph, paths, ranks, infinity edges, legend text, source, and 
    # sink will be reset.
    #
    # @param self The object pointer.
    # 
    def reset(self):
        self._graph = None
        self._container_paths = []
        self._container_ranks = []
        self._container_infinite = []
        self._node_source = None
        self._node_sink = None
        self._container_legend_text = []
        
        return
    
    ## Sets the graph data that will be painted.
    #
    # @post The _graph variable will contain the supplied graph data.
    #
    # @param self The object pointer.
    # @param graph Dictionary of nodes in the graph will each value being a
    # dictionary of edges, where each value is the cost of an edge.
    #
    def set_graph(self, graph):
        self._graph = graph
        
        return
    
    ## Set a list of nodes to have the same rank.
    #
    # @pre The nodes exist in the graph data.
    # @post The specified list will be added to _container_ranks.
    #
    # @param self The object pointer.
    # @param nodes List of nodes which should have the same rank.
    #
    def set_rank_same(self, nodes):
        self._container_ranks.append(nodes)
        
        return
    
    ## Add a path to be painted with the specified colors.
    # Note that _container_paths is FIFO, so the first paths to be place in will
    # be painted first. Therefore, items at the end of the container will be 
    # painted on top of item in the front of the container.
    #
    # @pre The nodes and edges between them exist in the graph data.
    # @post The specified path and colors will be added to _container_paths.
    #
    # @param self The object pointer.
    # @param nodes String of nodes in the path, i.e. "ABC" for the path A to B 
    # to C.
    # @param color_node The color that the nodes of the path will be painted. 
    # @param color_edge The color that the edges of the path will be painted.
    #
    def add_path(self, nodes, color_node, color_edge):
        self._container_paths.append({'path':nodes, 'colorNode': color_node, 
                                      'colorEdge': color_edge})        
        return
    
    ## Clears all paths to be painted.
    #
    # @post The _container_paths list will be empty.
    #
    # @param self The object pointer.
    #
    def clear_paths(self):
        self._container_paths = []
        
        return
    
    ## Add an edge to be painted as an infinite cost edge.
    #
    # @pre The specified nodes and edge exist in the graph data.
    # @post The specified edge will be in _container_infinity.
    #
    # @param self The object pointer.
    # @param node_from The node that the edge originates from.
    # @param node_to The node that the edge terminates at.
    #
    def add_infinite_edge(self, node_from, node_to):
        self._container_infinite.append("%s%s" % (node_from, node_to))
        
        return
    
    ## Clears all infinite cost edges to be painted.
    #
    # @post The _container_infinity list will be empty.
    #
    # @param self The object pointer.
    #
    def clear_infinite_edges(self):
        self._container_infinite = []
        
        return
    
    ## Sets the source and sink node for the layout.
    #
    # @pre The source and sink specified exist in the graph data.
    # @post The _node_source and _node_sink will be set.
    #
    # @param self The object pointer.
    # @param source The source node for the layout.
    # @param sink The sink node for the layout.
    #
    def set_source_sink(self, source, sink):
        self._node_source = source
        self._node_sink = sink
        
        return
    
    ## Sets the color the legend text will be painted.
    #
    # @post The _format_legend_color variable will be set.
    #
    # @param self The object pointer.
    # @param color Color as a word or hex, "red" or "#333333".
    #
    def set_legend_color(self, color):
        self._format_legend_color = color
        
        return
    
    ## Adds a line of text to the legend.
    # Currently only 4 lines of legend text are supported based on the dot
    # template file. If there are more lines of text, only the first 4 will be
    # displayed.
    #
    # @post The line will be added to _container_legend_text.
    #
    # @param self The object pointer.
    # @param text Line of text.
    #
    def add_legend_text(self, text):
        self._container_legend_text.append(text)
        
        return
    
    ## Clears all lines of legend text to be painted.
    #
    # @post The _container_legend_text list will be empty.
    #
    # @param self The object pointer.
    #
    def clear_legend_text(self):
        self._container_legend_text = []
        
        return
    
    ## Generates an image for the graph data with the supplied name.
    # Creates the dot markup file for the graph in _directoryData and the image
    # in _directory_images. Note that if the frames flag is set, the generated
    # image is to be part of a set, so the name will be "name-(frame #)".
    #
    # @pre The graph data exist.
    # @post An image of the graph will be located in _directory_images.
    #
    # @param self The object pointer.
    # @param name The name of the image file.
    # @param frame Denotes whether the image is to be part of a set.
    #
    def generate(self, name, frames=False):
        if frames:
            name = "%s-%s" % (name, self._frame_num)
            self._frame_num += 1
        
        self.create_dot(name)
        self.create_image(name)
        
        return
    
    ## Generates the dot markup file for the graph data.
    #
    # @pre The graph data and _format_body has been set.
    # @post The dot file for the graph will exist at _directory_data.
    #
    # @param self The object pointer.
    # @param name The name of the dot file to be generated.
    #
    def create_dot(self, name):
        if not os.path.exists(self._directory_data):
            os.mkdir(self._directory_data)
        
        fhandle = codecs.open("%s%s.dot" % (self._directory_data, name), 
                              encoding='utf-8', mode='w')
        
        fields = self.parse_graph()
        fields.append(self.parse_rank())
        fields.append(self.parse_source_sink())
        fields.append(self._format_legend_color)
        fields.extend(self.parse_legend())
        
        body = self._format_body % tuple(fields)
        fhandle.write(body)
        
        fhandle.close()
        
        return 
    
    ## Generates the image file for the graph data.
    #
    # @pre The dot file has been generated properly.
    # @post The image for the graph will exist at _directory_images.
    #
    # @param self The object pointer.
    # @param name The name of the image file to be generated.
    # @retval bool True if the image was created successfully, False otherwise.
    #
    def create_image(self, name):
        path_dot = "%s%s.dot" % (self._directory_data, name)
        path_png = "%s%s.png" % (self._directory_images, name)
        
        if not os.path.exists(path_dot):
            return False
        
        cmd = "dot %s -Tpng -o %s" % (path_dot, path_png)
        if os.system(cmd) == 0:
            return True
        else:
            return False
    
    ## Formats the nodes and edges of the graph data.
    #
    # @pre The graph data, _format_node, and _format_edge has been set.
    #
    # @param self The object pointer.
    # @retval [] A list of two strings, the nodes formatted string and the edges
    # formatted string.
    #
    def parse_graph(self):
        nodes = ""
        edges = ""
        
        for node, nitems in self._graph.iteritems():
            nodes += self._format_node % (node, self.find_node_color(node)) \
                     + "\n\t"
            
            for node_to, cost in nitems.iteritems():
                if (node + node_to) in self._container_infinite:
                    temp = self._format_edge % (node, node_to, u"∞", 
                                                "style=dashed, color=\"%s\"" 
                                                % self._format_infinity_color)
                else:
                    temp = self._format_edge % (node, node_to, cost, 
                                                self.find_edge_color(node, 
                                                                     node_to))
                
                if temp in edges:
                    continue
                else:
                    edges += temp + "\n\t"
        
        return [nodes, edges]
    
    ## Formats the rank of the nodes of the graph data.
    #
    # @pre The graph data and _format_rank_same has been set.
    #
    # @param self The object pointer.
    # @retval "" The node rank formatted string.
    #
    def parse_rank(self):
        rank = ""
        for nodes in self._container_ranks:
            rank += self._format_rank_same % ("\"%s\"" % "\" \"".join(nodes)) \
                    + "\n\t"
        
        return rank
    
    ## Formats the source and sink nodes of the graph data.
    #
    # @pre The graph data, _format_rank_source, and _format_rank_sink has been 
    # set.
    #
    # @param self The object pointer.
    # @retval "" The source and sink rank formatted string.
    #
    def parse_source_sink(self):
        layout = ""
        if self._node_source:
            layout += self._format_rank_source % self._node_source + "\n\t"
        
        if self._node_sink:
            layout += self._format_rank_sink % self._node_sink + "\n"
        
        return layout
    
    ## Formats the legend text.
    #
    # @pre The _format_legend_text has been set.
    #
    # @param self The object pointer.
    # @retval " The lines of the legend formatted string.
    #
    def parse_legend(self):
        legend = []
        for i in range(0, 4):
            if i < len(self._container_legend_text):
                legend.append(self._format_legend_text % 
                              self._container_legend_text[i])
            else:
                legend.append(self._format_legend_text % "")
        
        return legend
    
    ## Finds the color of a node based on the paths set.
    #
    # @param self The object pointer.
    # @param node The node whose color is being queried.
    # @retval "" The color as a word or hex, "red" or "#333333".
    #
    def find_node_color(self, node):
        color = ""
        for path_info in self._container_paths:
            if node in path_info['path']:
                color = path_info['colorNode']
        
        return color
    
    ## Finds the color of a edge based on the paths set.
    #
    # @param self The object pointer.
    # @param node The node where the edge originates from.
    # @param node _to The node where the edge terminates.
    # @retval "" The color as a word or hex, "red" or "#333333".
    #
    def find_edge_color(self, node, node_to):
        color = ""
        edge = "%s%s" % (node, node_to)
        for path_info in self._container_paths:
            if edge in path_info['path']:
                color = ", penwidth=2, color=\"%s\"" % path_info['colorEdge']
        
        return color

