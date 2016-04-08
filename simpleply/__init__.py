#! /usr/bin/env python


"""
Dave Chen's simple PLY module

This module supports a simplified PLY mesh.  It does not support the completely
general PLY format.  In particular, vertices only have position, normal, color and texture
coordinates, and edges and faces only have vertex indices.  Other elements and properties
possible in more complex PLY files are ignored.

Also it only reads and writes ASCII PLY files.  Reading and writing of binary PLY
files might be supported in the future.

For a completely general PLY file, see the plyfile module:
    https://pypi.python.org/pypi/plyfile
"""

from __future__ import print_function
import sys, inspect
import plyheader


Debug = False

#
class PlyVertex:
    def __init__(self, pos=[0.0,0.0,0.0]):
        self.pos = pos
        self.norm = [0.0, 0.0, 0.0]
        self.tex = [0.0, 0.0]
        self.color = [1.0, 1.0, 1.0, 1.0]

    def setTexture(self, u, v):
        self.tex[0] = u
        self.tex[1] = v

    def setColor(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def setNormal(self, nx, ny, nz):
        self.norm[0] = nx
        self.norm[1] = ny
        self.norm[2] = nz

    def getTexture(self):
        return self.tex
    def getColor(self):
        return self.color
    def getNormal(self):
        return self.norm
    def getPosition(self):
        return self.pos

    def __str__(self):
        return str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.pos[2])

#
class PlyEdge:
    def __init__(self):
        self.ends = [0, 0]

    def __init__(self, e0, e1):
        self.ends = [e0, e1]

    def getEnds(self):
        return self.ends

    def __str__(self):
        return str(self.ends[0]) + " " + str(self.ends[1])

#
class PlyFace:
    def __init__(self, verts = []):
        self.vertices = verts
        #self.color = [1.0, 1.0, 1.0, 1.0]

    def getVertices(self):
        return self.vertices

    def __str__(self):
        x = ""
        for v in self.vertices:
          x = x + str(v) + " "
        return x

#
class PlyMesh:
    def __init__(self):
        self.textureFlag = False
        self.vertexColorFlag = False
        self.vertexNormalFlag = False
        #self.faceColorFlag = False
        self.vertices = []
        self.edges = []
        self.faces = []

    def addVertex(self, v):
        self.vertices.append(v)
        return len(self.vertices)-1

    def addEdge(self, v):
        self.edges.append(v)
        return len(self.edges)-1

    def addFace(self, v):
        self.faces.append(v)
        return len(self.faces)-1

    def getVertex(self, index):
        return self.vertices[index]
    def getEdge(self, index):
        return self.edges[index]
    def getFace(self, index):
        return self.faces[index]

    def __str__(self):
        x = "PlyVertices\n"

        if len(self.vertices):
            count = 0
            for v in self.vertices:
                x = x + str(count) + ": " + str(v)  + '\n'
                count = count+1

        if len(self.edges):
            count = 0
            x = x + "PlyEdges\n"
            for e in self.edges:
                x = x + str(count) + ": " + str(e)
                count = count + 1

        if len(self.faces):
            x = x + "PlyFaces\n"
            for f in self.faces:
                x = x + str(f) + '\n'

        return x

    def write(self, name):
        """ Write an ASCII PLY file. """
        fp = open(name, "w")
        plyheader.plyheader(len(self.vertices), len(self.edges), len(self.faces), self.vertexColorFlag,
            self.vertexNormalFlag, self.textureFlag, fp)

        for v in self.vertices:
            print(v, end="", file=fp)
            if self.vertexColorFlag:
                print("", v.color[0], v.color[1], v.color[2], end="", file=fp)
            if self.vertexNormalFlag:
                print("", v.norm[0], v.norm[1], v.norm[2], end="", file=fp)
            if self.textureFlag:
                print("", v.tex[0], v.tex[1], end="", file=fp)
            print( "", file=fp )

        for e in self.edges:
            print(e, file=fp)

        for f in self.faces:
            print( len(f.vertices), end="", file=fp )
            for v in f.vertices:
                print( "", v, end="", file=fp )
            print( "", file=fp )

    def read(self, name):
        """ Read an ASCII PLY file.this is not a completely general PLY file reader.
            It only handles a position, color and texture coordinates.  Other properties
            are ignored.
        """
        # read file
        with open (name) as f:
            lines = f.read().splitlines()
        # setup variables
        end_head_found = False
        header = []
        lc = elempos = current_elem_type = 0
        vcpos = vtpos = vnpos = -1
        xpos = 0
        ypos = 1
        zpos = 2
        nums = []
        elements = []
        self.__init__()

        # parse the PLY header
        for l in lines:
            if l.find("end_header")>=0:
                end_header_found = True
                break
            header.append(l)
            lc = lc+1
            if l.find("binary") > 0:
                print("Error: cannot read binary PLY file", name)
                return
            # element statement
            if l.find("element")>=0:
                words = l.split()
                elempos = 0
                if l.find("vertex") > 0:
                    current_elem_type = 1
                    nums.append( int(words[2]) )
                    elements.append(1)
                if l.find("edge") > 0:
                    current_elem_type = 2
                    nums.append( int(words[2]) )
                    elements.append(2)
                if l.find("face") > 0:
                    current_elem_type = 3
                    nums.append( int(words[2]) )
                    elements.append(3)
            # property statement
            if l.find("property") >= 0:
                words = l.split()
                if current_elem_type == 1:
                    # red channel
                    if (words[2] == "r") or (words[2] == "red"):
                       vcpos = elempos
                       self.vertexColorFlag = True
                    # first texture coordinate
                    if words[2] == "u":
                       vtpos = elempos
                       self.textureFlag = True
                    if words[2] == "x":
                       xpos = elempos
                    if words[2] == "y":
                       ypos = elempos
                    if words[2] == "z":
                       zpos = elempos
                    if (words[2] == "nx"):
                       vnpos = elempos
                       self.vertexNormalFlag = True
                elempos = elempos+1


        starts = [lc+1]
        ends = [starts[0]+nums[0]-1]
        for i in range(1,len(elements)):
            starts.append( ends[i-1]+1 )
            ends.append( starts[i]+nums[i]-1 )

        if Debug:
            print ("elements:", elements)
            print ("numbers:", nums)
            print ("starts:", starts)
            print ("ends:", ends)

        # get vertices
        epos = -1
        try:
            epos = elements.index(1)
            self.vertices = [None] * nums[epos]

            count = 0
            for v in range(starts[epos], ends[epos]+1):
                words = lines[v].split()

                vert = PlyVertex( [float(words[xpos]), float(words[ypos]), float(words[zpos])] )
                if vcpos > 0:
                    vert.setColor( float(words[vcpos]), float(words[vcpos+1]), float(words[vcpos+2]) )
                if vnpos > 0:
                    vert.setNormal( float(words[vnpos]), float(words[vnpos+1]), float(words[vnpos+2]) )
                if vtpos > 0:
                    vert.setTexture( float(words[vtpos]), float(words[vtpos+1]) )
                self.vertices[count] = vert
                count = count+1
        except ValueError:
            print("PLY file has no vertices")


        # get faces
        epos = -1
        try:
            epos = elements.index(3)
            self.faces = [None] * nums[epos]
            count = 0
            for f in range(starts[epos], ends[epos]+1):
                words = lines[f].split()
                verts = []
                if Debug:
                    print (words)
                for w in words[1:]:
                    verts.append(int(w))
                if Debug:
                    print (verts)
                face = PlyFace( verts )
                self.faces[count] = face
                count = count+1
        except ValueError:
            print("PLY file has no faces")
            return

        if Debug:
            print(self)

def readPly(name):
    mesh = PlyMesh()
    mesh.read(name)
    return mesh

if __name__ == "__main__":
    print( "Simple Ply test" )


    if len(sys.argv) == 1:
        # if no file name is given on the command line,
        # create a 1 triangle ply mesh
        Debug = True
        v0 = PlyVertex([0.,0.,0.])
        v1 = PlyVertex([0.,1.,0.])
        v2 = PlyVertex([1.,0.,0.])

        mesh = PlyMesh()
        i0 = mesh.addVertex(v0)
        i1 = mesh.addVertex(v1)
        i2 = mesh.addVertex(v2)

        face = PlyFace([i0, i1, i2])
        mesh.addFace(face)

        print( mesh )
        #mesh.write("test.ply")

    else:
        # if there's a file name on the command line, read it that file
        mesh = PlyMesh()
        mesh.read(sys.argv[1])
        print ( mesh )

        if len(sys.argv) > 2:
            # if there's another file name, write out the ply file to that name
            mesh.write(sys.argv[2])

