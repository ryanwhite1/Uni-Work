from OpenGL.GL import *
import math
import numpy as np
import time
import imgui

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu
from ObjModel import ObjModel


g_cameraPosition = [-20,6,-3]
#g_cameraDirection = [0,0,-1]
g_yFovDeg = 45.0
g_cameraYawDeg = -81.0
g_cameraPitchDeg = 9.7

g_houseModel = None

def update(dt, keys, mouseDelta):
    global g_cameraPosition
    #global g_cameraDirection 
    global g_cameraYawDeg
    global g_cameraPitchDeg

    cameraSpeed = 0.0
    cameraTurnSpeed = 0.0
    cameraPitchSpeed = 0.0
    cameraStrafeSpeed = 0.0

    if keys["UP"] or keys["W"]:
        cameraSpeed += 10.0
    if keys["DOWN"] or keys["S"]:
        cameraSpeed -= 10.0
    if keys["LEFT"]:
        cameraTurnSpeed -= 90.0
    if keys["RIGHT"]:
        cameraTurnSpeed += 90.0
    if keys["A"]:
        cameraStrafeSpeed += 10.0
    if keys["D"]:
        cameraStrafeSpeed -= 10.0

    # Mouse look is enabled with right mouse button
    if keys["MOUSE_BUTTON_LEFT"]:
        cameraTurnSpeed = mouseDelta[0] * 90.0
        cameraPitchSpeed = mouseDelta[1] * 90.0

    g_cameraYawDeg += cameraTurnSpeed * dt
    g_cameraPitchDeg = min(89.0, max(-89.0, g_cameraPitchDeg + cameraPitchSpeed * dt))

    #g_cameraDirection = lu.Mat3(lu.make_rotation_y(cameraTurnSpeed * dt)) * lu.Mat3(lu.make_rotation_x(cameraPitchSpeed * dt)) * g_cameraDirection
    cameraRotation = lu.Mat3(lu.make_rotation_y(math.radians(g_cameraYawDeg))) * lu.Mat3(lu.make_rotation_x(math.radians(g_cameraPitchDeg))) 
    cameraDirection = cameraRotation * [0,0,1]
    g_cameraPosition += np.array(cameraDirection) * cameraSpeed * dt




# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(width, height):
    global g_cameraPosition
    global g_cameraYawDeg
    global g_cameraPitchDeg
    global g_yFovDeg
    global g_houseModel

    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(0, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.3, 0.3, 0.7, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    viewToClipTransform = magic.make_perspective(g_yFovDeg, width/height, 0.01, 50.0)

    cameraDirection = lu.Mat3(lu.make_rotation_y(math.radians(g_cameraYawDeg))) * lu.Mat3(lu.make_rotation_x(math.radians(g_cameraPitchDeg))) * [0,0,1]

    worldToViewTransform = magic.make_lookFrom(g_cameraPosition, cameraDirection, [0,1,0])
    viewToClipTransform = magic.make_perspective(g_yFovDeg, width/height, 0.01, 1000.0)

    magic.drawObjModel(viewToClipTransform, worldToViewTransform, lu.Mat4(), g_houseModel)

    magic.drawCoordinateSystem(viewToClipTransform, worldToViewTransform)


def drawUi(width, height):
    global g_yFovDeg
    global g_cameraYawDeg
    global g_cameraPitchDeg

    _,g_yFovDeg = imgui.slider_float("Y-Fov (Degrees)", g_yFovDeg, 1.00, 90.0)
    _,g_cameraYawDeg = imgui.slider_float("Camera Yaw (Degrees)", g_cameraYawDeg, -180.00, 180.0)
    _,g_cameraPitchDeg = imgui.slider_float("Camera Pitch (Degrees)", g_cameraPitchDeg, -89.00, 89.0)



def initResources():
    global g_houseModel
    g_houseModel = ObjModel("data/house.obj");

# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 2, part 2", 640, 480, renderFrame, initResources, drawUi, update)
