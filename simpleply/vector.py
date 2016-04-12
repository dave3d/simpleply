#! /usr/bin/env python


"""Some vector math functions.  All except cross work on N vectors."""

import math

def add(a,b):
    """Returns the sum of two vectors"""
    c = []
    for ax, by in zip(a,b):
        c.append(ax+by)
    return c

def subtract(a,b):
    """Returns the difference of two vectors"""
    c = []
    for ax, by in zip(a,b):
        c.append(ax-by)
    return c

def dot(a,b):
    """Returns the dot product of two vectors"""
    c = []
    for ax, by in zip(a,b):
        c.append(ax*by)
    return c

def cross(a,b):
    """Returns the cross product of two vectors"""
    c = [0,0,0]
    c[0] = a[1]*b[2] - b[1]*a[2]
    c[1] = -(a[0]*b[2] - b[0]*a[2])
    c[2] = a[0]*b[1] - b[0]*a[1]
    return c

def length(a):
    """Returns the length of a vector"""
    s = 0.0
    for x in a:
        s = s + x*x
    return math.sqrt(s)

def normalize(a):
    """Returns a normalized version of a vector"""
    l = length(a)
    c = []
    if l == 0.0:
        return c
    for x in a:
        c.append(x/l)
    return c

def distance(a,b):
    """Returns the distance between two vectors"""
    c = subtract(a,b)
    return length(c)

if __name__ == "__main__":

    v1 = [1,2,3]
    v2 = [4,5,6]
    print "v1:", v1
    print "v2:", v2

    print "v1+v2:", add(v1,v2)
    print "v1-v2:", subtract(v1,v2)

    print "v1.v2:", dot(v1,v2)
    print "v1Xv2:", cross(v1,v2)

    print "length(v1):", length(v1)
    print "normalize(v1):", normalize(v1)

    print "distance(v1,v2):", distance(v1,v2)
