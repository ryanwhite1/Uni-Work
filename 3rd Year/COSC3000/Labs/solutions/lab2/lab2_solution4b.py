from OpenGL.GL import *
import math
import numpy as np
import time
import imgui

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu

g_cameraDistance = 1.0
g_cameraYawDeg = 0.0
g_cameraPitchDeg = 0.0
g_yFovDeg = 45.0

g_triangleVerts = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]

# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(width, height):
    global g_triangleVerts
    global g_cameraDistance
    global g_cameraYawDeg
    global g_cameraPitchDeg
    global g_yFovDeg

    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(0, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.2, 0.3, 0.1, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)



    viewToClipTransform = magic.make_perspective(g_yFovDeg, width/height, 0.01, 50.0)
    worldToViewTransform = magic.make_lookAt([0.5,0.5,g_cameraDistance], [0.5,0.5,0], [0,1,0])


    worldToClipTransform = viewToClipTransform * worldToViewTransform

    magic.drawVertexDataAsTriangles(g_triangleVerts, worldToClipTransform);

    # Draw UI display for the render data here to save having to copy transforms and data a
    # ImGui can be used everywhere in the draw function, it is just usually neater to keep UI separate.
    # But, not always!
    if imgui.tree_node("World Space", imgui.TREE_NODE_DEFAULT_OPEN):
        for i,(x,y,z) in enumerate(g_triangleVerts):
            imgui.input_float3("v%d"%i, x,y,z, 2)
        imgui.tree_pop()
    if imgui.tree_node("View Space", imgui.TREE_NODE_DEFAULT_OPEN):
        for i,(x,y,z) in enumerate(g_triangleVerts):
            hx,hy,hz,hw = worldToViewTransform * [x,y,z,1]
            imgui.input_float3("v%d"%i, hx, hy, hz, 2)
        imgui.tree_pop()
    if imgui.tree_node("Clip Space", imgui.TREE_NODE_DEFAULT_OPEN):
        for i,(x,y,z) in enumerate(g_triangleVerts):
            hx,hy,hz,hw = worldToClipTransform * [x,y,z,1]
            imgui.input_float4("v%d"%i, hx, hy, hz, hw, 2)
        imgui.tree_pop()
    if imgui.tree_node("NDC", imgui.TREE_NODE_DEFAULT_OPEN):
        for i,(x,y,z) in enumerate(g_triangleVerts):
            hx,hy,hz,hw = worldToClipTransform * [x,y,z,1]
            imgui.input_float3("v%d"%i, hx/hw, hy/hw, hz/hw, 2)
        imgui.tree_pop()

    magic.drawCoordinateSystem(viewToClipTransform, worldToViewTransform)


def drawUi(width, height):
    global g_triangleVerts
    global g_cameraDistance
    global g_cameraYawDeg
    global g_cameraPitchDeg
    global g_yFovDeg

    imgui.push_item_width(125)
    _,g_cameraDistance = imgui.slider_float("CameraDistance", g_cameraDistance, 1.00, 20.0)
    _,g_yFovDeg = imgui.slider_float("Y-Fov (Deg)", g_yFovDeg, 1.00, 90.0)
    _,g_cameraYawDeg = imgui.slider_float("Camera Yaw (Deg)", g_cameraYawDeg, -180.00, 180.0)
    _,g_cameraPitchDeg = imgui.slider_float("Camera Pitch (Deg)", g_cameraPitchDeg, -89.00, 89.0)
    imgui.pop_item_width()

# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 2", 640, 480, renderFrame, None, drawUi)

#        vec2 uv = abs(2.0 * mod(v2f_modelSpaceXy.xy * 10.0, 1.0) - 1.0);
#	    fragmentColor = vec4(1.0 - vec3(pow(max(uv.x, uv.y), 21.0)), 1.0);
