from OpenGL.GL import *
import math
import numpy as np
import time

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu

g_triangleVerts = [
    [320, 480, 0],
    [640, 0, 0],
    [0, 0, 0],
]

def make_translation(x, y, z):
    return lu.Mat4([[1,0,0,x],
                 [0,1,0,y],
                 [0,0,1,z],
                 [0,0,0,1]])


def make_scale(x, y, z):
    return lu.Mat4([[x,0,0,0],
                 [0,y,0,0],
                 [0,0,z,0],
                 [0,0,0,1]])


def make_rotation_z(angle):
    return lu.Mat4([[math.cos(angle),-math.sin(angle),0,0],
                 [math.sin(angle),math.cos(angle),0,0],
                 [0,0,1,0],
                 [0,0,0,1]])


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

    screenSpaceToNdc = make_translation(-1.0, -1.0, 0.0) * make_scale(2.0/width, 2.0/height, 1.0)
    mouseTfm = make_translation(magic.g_mousePos[0], height-magic.g_mousePos[1], 0.0)
    rotTfm = make_rotation_z(time.time())
    triCentre = np.average(g_triangleVerts, 0)
    scale = 0.75 + math.sin(time.time()) * 0.5
    scaleTfm = make_scale(scale,scale,scale)
    triTfm = mouseTfm * rotTfm * scaleTfm * make_translation(-triCentre[0], -triCentre[1], 0)
    tfm = screenSpaceToNdc * triTfm

    magic.drawVertexDataAsTrianglesWithVertexShader(g_triangleVerts, tfm, """
    #version 330
    in vec3 positionIn;
    uniform mat4 transformationMatrix;
    void main() 
    {
	    gl_Position = transformationMatrix * vec4(positionIn, 1.0);
    }
    """);


# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 1, part 1", 640, 480, renderFrame)
