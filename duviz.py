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

THRESH=.02
CM_CONST=3


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
    tmparr = line.split(None, 1)
    if len(tmparr) != 2:
        error("%r is not valid, somehow, picked up on %d splits" % (line, len(tmparr)))
        tmparr = (None, None)
    size, path = tmparr
    path = path.strip()
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
    # am I at the root?
    if len(data) == 1 and size == data[data.keys()[0]].size:
        root_node = data[data.keys()[0]]
        drawroot(root_node.name, size)
        draw_level(root_node.children, size, 1, 0)
    else:
        print "??"
        print data
        sys.exit(1)
    print open("base_end_text").read()


def drawroot(label, size):
    print "\draw (0,0) circle (%dcm);" % CM_CONST
    print "\\node at (0,.25) {%s};" % (human_readable(label))
    print "\\node at (0,-.25) {%s};" % (human_readable(size))



def draw_level(data, size, level, alpha):
    for label,node in data.items():
        endalpha = int((float(node.size)/size)*360)
        curdist = level * CM_CONST
        newdist = (level+1) * CM_CONST
        print "\\begin{scope}[rotate=%d]" % alpha
        print "\\draw (0:%dcm) -- (0:%dcm)" % (curdist, newdist)
        print "  arc (0:%d:%dcm) -- (%d:%dcm)" % \
            (endalpha, newdist, endalpha, curdist)
        print "  arc (%d:0:%dcm) -- cycle;" % (endalpha, curdist)
        print "\\end{scope}"
        # label
        rotate = alpha + endalpha/2 - 90
        print "\\begin{scope}[rotate=%d]" % rotate
        print "\\node[rotate=%d] at (0, %f) {\\footnotesize %s};" % \
            (rotate, curdist + float(CM_CONST)/2 + .25, escape(node.name))
        print "\\node[rotate=%d] at (0, %f) {\\footnotesize %s};" % \
            (rotate, curdist + float(CM_CONST)/2, human_readable(node.size))
        print "\\end{scope}"
        draw_level(node.children, size, level+1, alpha)
        alpha = endalpha + alpha
        

def human_readable(size):
    for i in ("B", "KB", "GB", "TB", "PB"):
        if size < 1024 or i == "PB":
            return "%3.2f %s" % (size, i)
        size = size/1024.
   

def escape(s):
    for character in "\\#$%^&_{}~":
        s = s.replace(character, '\\'+character)
    return s


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


if __name__ == "__main__":
    main(sys.argv[-1]) # simple hack for now


