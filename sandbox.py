#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sandbox.py
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
from graph import Graph
from graphviz2 import Graphviz2


def main():
	G = Graph("0")
	
	G.addLink("C", "B", 1)
	G.addLink("C", "D", 2)
	G.addLink("C", "E", 3)
	G.addLink("B", "D", 4)
	G.addLink("D", "E", 2)
	G.addLink("D", "F", 1)
	G.addLink("E", "F", 2)
	G.addLink("A", "C", 2)
	G.addLink("A", "B", 3)
	G.save()
	
#	G.load()
#	
#	G.m_gviz = Graphviz2()
#	G.m_gviz.setSourceSink("A", "F")
#	G.m_gviz.setRank(['A', 'B', 'D'])
#	G.m_gviz.setRank(['C', 'E', 'F'])
#	
#	G.m_gviz.setPath("ACDF", "#3465a4", "#204a87")
#	G.m_gviz.setInfinity("A", "C")
#	G.m_gviz.setLegendColor("#729fcf")
#	G.m_gviz.clearLegendText()
#	G.m_gviz.addLegendText("A[0]= A,C,D,F    (5)")
#	G.m_gviz.addLegendText("A[0]= A,C,D,F (5)")
#	G.m_gviz.addLegendText("A[0]= A,C,D,F (5)")
#	G.m_gviz.addLegendText("A[0]= A,C,D,F (5)")
	
	G.export2()
	
	return 0


if __name__ == '__main__':
	main()
