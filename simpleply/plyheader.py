#! /usr/bin/env python

from __future__ import print_function

import sys


def plyheader(nverts, nfaces, vcolorFlag=False, tcoordFlag=False, fout=sys.stdout):

  print ("ply", file=fout)
  print ("format ascii 1.0", file=fout)
  print ("element vertex", nverts, file=fout)
  print ("property float x", file=fout)
  print ("property float y", file=fout)
  print ("property float z", file=fout)

  if vcolorFlag:
    print ("property uchar red", file=fout)
    print ("property uchar green", file=fout)
    print ("property uchar blue", file=fout)

  if tcoordFlag:
    print ("property float u", file=fout)
    print ("property float v", file=fout)

  print ("element face", nfaces, file=fout)
  print ("property list uchar int vertex_indices", file=fout)

  print ("end_header", file=fout)

