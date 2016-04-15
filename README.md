# simpleply
A python module for simplified ASCII PLY files

Written by David T. Chen from the National Library of Medicine, dchen@mail.nih.gov It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

Simple PLY module
=================
A module that contains a data structure for a simplified PLY mesh.  The PLY
format is a general file format for storing 3d surface meshes created by
Greg Turk.

The original PLY file format
----------------------------
The general PLY format consists of a text header and then either
ASCII or binary data.  The header describes the basic elements in the mesh,
typically vertices, edges and faces.  Each element can have a variety of
properties such as "x", "y", "z", "red", "green", or "blue" for the vertices.
It also allows for list properties.

This simplified PLY format
--------------------------
This module reads and writes only the ASCII version of the PLY file format.
Also it is limited in what elements and properties it recognizes.  In the general
file format, the elements can be arbitrary, not just vertices, edges and faces.
And each element could have an arbitrary number and types of properties.

Our simplified version of PLY supported here only allows vertex, edge and face
elements.  The vertex element only allows for "x", "y", "z", "nx", "ny", "nz",
"r", "g", "b", "red", "green", "blue", "u", and "v" properties.  Edges can only
have two vertex index properties.  Faces can only have a list of vertex index
property.

While these restrictions may seem limiting, in our experience they allow for
the vast majority of PLY files in typical usage.

A more general PLY module
-------------------------
There is a general PLY file module at the following link
  https://pypi.python.org/pypi/plyfile

That plyfile module is a straight python port of Turk's original C code.
However the poor performance reading ASCII Ply files and relatively awkward data
structures motivated this module.

