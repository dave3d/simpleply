#! /usr/bin/env python

from __future__ import print_function

import sys

class ColorType:
    no_color, uchar_color, float_color = range(3)

def plyheader(nverts, nedges, nfaces, vcolorType=ColorType.no_color, vnormFlag=False, tcoordFlag=False, fout=sys.stdout):
    """A function write out an ASCII PLY file header"""

    print ("ply", file=fout)
    print ("format ascii 1.0", file=fout)

    if nverts>0:
        print ("element vertex", nverts, file=fout)
        print ("property float x", file=fout)
        print ("property float y", file=fout)
        print ("property float z", file=fout)

        if vcolorType == ColorType.uchar_color:
            print ("property uchar red", file=fout)
            print ("property uchar green", file=fout)
            print ("property uchar blue", file=fout)
        elif vcolorType == ColorType.float_color:
            print ("property float red", file=fout)
            print ("property float green", file=fout)
            print ("property float blue", file=fout)

        if vnormFlag:
            print ("property float nx", file=fout)
            print ("property float ny", file=fout)
            print ("property float nz", file=fout)

        if tcoordFlag:
            print ("property float u", file=fout)
            print ("property float v", file=fout)

    if nedges>0:
        print ("element face", nfaces, file=fout)
        print ("property uint e0", file=fout)
        print ("property uint e1", file=fout)

    if nfaces>0:
        print ("element face", nfaces, file=fout)
        print ("property list uchar int vertex_indices", file=fout)

    print ("end_header", file=fout)

