from OpenGL.GL import *
import math
import numpy as np
import time

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu

g_triangleVerts = [
    [-1, -1, 0],
    [0, 1, 0],
    [1, -1, 0],
]

# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(width, height):
    global g_triangleVerts
    
    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(0, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.2, 0.3, 0.1, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    # This is implemented to upload the vertex data to the graphics card and issue a drawcall to produce one triangle 
    # for every three vertices.
    magic.drawVertexDataAsTriangles(g_triangleVerts)


# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 1, part 1", 640, 480, renderFrame)
