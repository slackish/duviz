#!/usr/bin/python
"""
Visualizing du on large directories suck

I could not find a method of visualizing du in one hour, so I wrote this
instead.

There are tools that exist that do this, but have problems.  Big problems.
Like with you are dealing with "big data".  Like >100TB sets.  I think it's
simple, so I'm writing this 

Resources:
http://www.tug.org/pracjourn/2007-1/mertz/mertz.pdf
"""

import os
import sys

THRESH=.03

class Node:
    def __init__(self, name, size=None):
        self.name = name
        self.size = size
        self.children = {}

    def has_children(self):
        return len(self.children) > 1

    def __str__(self):
#        return str(self.children)
        return str(self.children)

    def __repr__(self):
#        return str(self.children)
        return str(self.children)
    

def grabsize(inputfh):
    inputfh.seek(-1024,2)
    line = inputfh.readlines()[-1]
    size, _ = parseline(line)
    inputfh.seek(0,0)
    return size


def parseline(line):
    tmparr = line.split()
    if len(tmparr) != 2:
        error("%r is not valid, somehow" % line)
        tmparr = (None, None)
    size, path = tmparr
    try:
        size = int(size)
    except:
        #TODO: handle human readable
        pass
    return size, path
    

def parse(inputf):
    inputfh = open(inputf, "rb")
    totalsize = grabsize(inputfh)
    threshold = int(THRESH * totalsize)
    final_dict = {}
    cleanup_count = 0
    cutoff = 0
    for line in inputfh:
        size, path = parseline(line)
        if size == None or path == None:
            continue
        if size >= threshold:
            final_dict[path] = size
    return final_dict, totalsize


def error(msg):
    print >>sys.stderr, msg


def draw(data, size):
    print open("base_open_text").read()
    print len(data)


def draw_level(data, size):
    




def process(data, size):
    """ Now to identify inputs """
    head_dict_tree = Node(".")
    for path,size in data.items():
        process_path(head_dict_tree.children, path, size)
    return head_dict_tree.children
        

def process_path(dict_tree, path, size):
    
    if os.sep not in path:
        if path not in dict_tree:
            dict_tree[path] = Node(path, size)
        else:
            dict_tree[path].size = size
    else:
        current, remaining = path.split(os.sep,1)
        if current not in dict_tree.keys():
            dict_tree[current] = Node(current)
        process_path(dict_tree[current].children, remaining, size)




    


def main(inputf):
    data, size = parse(inputf)
    data = process(data, size)
    draw(data, size)
    print "hi"
    print data



if __name__ == "__main__":
    main(sys.argv[-1]) # simple hack for now


