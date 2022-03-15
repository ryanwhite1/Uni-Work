from OpenGL.GL import *

import math
import numpy as np
import time
from ObjModel import ObjModel
import imgui

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu

g_completeCraneModel = None
g_groundModel = None
g_baseModel = None
g_postModel = None
g_beamModel = None
g_weightModel = None
g_ballModel = None
g_cableModel = None

g_worldSpaceLightDirection = [-1, -1, -1]
g_cameraDistance = 40.0
g_cameraYaw = 45.0
g_cameraPitch = 40.0
g_lookTargetHeight = 6.0

g_baseRotationDeg = 0.0
g_beamOffset = 0.0


# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(width, height):
    global g_completeCraneModel
    global g_groundModel
    global g_baseModel
    global g_postModel
    global g_beamModel
    global g_weightModel
    global g_ballModel
    global g_cableModel

    global g_worldSpaceLightDirection
    global g_cameraDistance
    global g_cameraYaw
    global g_cameraPitch
    global g_lookTargetHeight
    global g_baseRotationDeg
    global g_beamOffset

    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(0, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.2, 0.3, 0.1, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    # Use the camera parameters to calucalte the position of the 'eye' or camera, the viewer location
    eyePos = lu.Mat3(lu.make_rotation_y(math.radians(g_cameraYaw)) * lu.make_rotation_x(-math.radians(g_cameraPitch))) * [0.0, 0.0, g_cameraDistance]

    worldToViewTfm = magic.make_lookAt(eyePos, [0,g_lookTargetHeight,0], [0, 1, 0])
    viewToClipTfm = magic.make_perspective(45.0, width / height, 0.1, 1000.0)

    # code drawing the floor. The model to world transform is identity, which means that the model/object space
    # is the same as the world space.
    drawObjModel(viewToClipTfm, worldToViewTfm, lu.Mat4(), g_groundModel)


    # rendering each of the parts of the crane in turn, note however that the order of drawing is irrelevant, what matteris is how the transforms are combined.
    baseModelToWorldTransform = lu.make_rotation_y(math.radians(g_baseRotationDeg)) * lu.make_translation(0.0, 1.0, 0.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, baseModelToWorldTransform, g_baseModel)

    postModelToWorldTransform = baseModelToWorldTransform * lu.make_translation(0, 7.0, 0.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, postModelToWorldTransform, g_postModel)

    beamModelToWorldTransform = baseModelToWorldTransform * lu.make_translation(0, 15.0, 3.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, beamModelToWorldTransform, g_beamModel)

    weightModelToWorldTransform = baseModelToWorldTransform * lu.make_translation(0, 15.0, -6.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, weightModelToWorldTransform, g_weightModel)

    ballModelToWorldTransform = baseModelToWorldTransform * lu.make_translation(0, 2.0, 10.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, ballModelToWorldTransform, g_ballModel)

    cableModelToWorldTransform = baseModelToWorldTransform * lu.make_translation(0, 9.0, 10.0)
    drawObjModel(viewToClipTfm, worldToViewTfm, cableModelToWorldTransform, g_cableModel)

    # draw the semi-transparent full crane for reference.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    drawObjModel(viewToClipTfm, worldToViewTfm, lu.Mat4(), g_completeCraneModel)
    glDisable(GL_BLEND)

# This code loads models for drawing, so we don't have to use code to define everything. I used Maya to model and texture the crane, and later exported it part by part as .obj
# It may safely be ignored for now.
def initResources():
    global g_completeCraneModel
    global g_groundModel
    global g_baseModel
    global g_postModel
    global g_beamModel
    global g_weightModel
    global g_ballModel
    global g_cableModel

    g_completeCraneModel = ObjModel("data/crane/crane_complete.obj")
    g_groundModel = ObjModel("data/crane/ground.obj")
    g_baseModel = ObjModel("data/crane/base.obj")
    g_postModel = ObjModel("data/crane/post.obj")
    g_beamModel = ObjModel("data/crane/beam.obj")
    g_weightModel = ObjModel("data/crane/counter_weight.obj")
    g_ballModel = ObjModel("data/crane/ball.obj")
    g_cableModel = ObjModel("data/crane/cable.obj")

    # the basic magic setup turns off backface culling, here we turn it back in again.
    glEnable(GL_CULL_FACE)


# This code is called by the magic at a good time to do UI stuff, you can actually add UI code whenver, but it is generally best to keep it
# to itself, from a design standpoint - avoids cluttering up the rendering code.
# You can safely ignore the details of this bit of code for this lab, it uses ImGui.
def drawUi():
    global g_cameraDistance
    global g_cameraYaw
    global g_cameraPitch
    global g_lookTargetHeight
    global g_baseRotationDeg
    global g_beamOffset

    if imgui.tree_node("Camera Controls", imgui.TREE_NODE_DEFAULT_OPEN):
        _,g_cameraDistance = imgui.slider_float("CameraDistance", g_cameraDistance, 1.0, 150.0)
        _,g_cameraYaw = imgui.slider_float("CameraYaw", g_cameraYaw, 0.0, 360.0)
        _,g_cameraPitch = imgui.slider_float("CameraPitch", g_cameraPitch, -89.0, 89.0)
        _,g_lookTargetHeight = imgui.slider_float("LookTargetHeight", g_lookTargetHeight, 0.0, 25.0)
        imgui.tree_pop()

    if imgui.tree_node("Crane Controls", imgui.TREE_NODE_DEFAULT_OPEN):
        _,g_baseRotationDeg = imgui.slider_float("BaseRotation(Degrees)", g_baseRotationDeg, 0.0, 360.0)
        _,g_beamOffset = imgui.slider_float("Beam Offset", g_beamOffset, -4.0, 4.0)
        imgui.tree_pop()


#
# Helper function to set the parameters that the ObjModel implementation expects.
# Most of what happens here is beyond the scope of this lab! 
#
def drawObjModel(viewToClipTfm, worldToViewTfm, modelToWorldTfm, model):
    # Lighting/Shading is very often done in view space, which is why a transformation that lands positions in this space is needed
    modelToViewTransform = worldToViewTfm * modelToWorldTfm
    
    # this is a special transform that ensures that normal vectors remain orthogonal to the 
    # surface they are supposed to be even in the prescence of non-uniform scaling.
    # It is a 3x3 matrix as vectors don't need translation anyway and this transform is only for vectors,
    # not points. If there is no non-uniform scaling this is just the same as Mat3(modelToViewTransform)
    modelToViewNormalTransform = lu.inverse(lu.transpose(lu.Mat3(modelToViewTransform)));

    # Bind the shader program such that we can set the uniforms (model.render sets it again)
    glUseProgram(model.defaultShader)

    # transform (rotate) light direction into view space (as this is what the ObjModel shader wants)
    viewSpaceLightDirection = lu.normalize(lu.Mat3(worldToViewTfm) * g_worldSpaceLightDirection)
    glUniform3fv(glGetUniformLocation(model.defaultShader, "viewSpaceLightDirection"), 1, viewSpaceLightDirection);

    # This dictionary contains a few transforms that are needed to render the ObjModel using the default shader.
    # it would be possible to just set the modelToWorld transform, as this is the only thing that changes between
    # the objects, and compute the other matrices in the vertex shader.
    # However, this would push a lot of redundant computation to the vertex shader and makes the code less self contained,
    # in this way we set all the required parameters explicitly.
    transforms = {
        "modelToClipTransform" : viewToClipTfm * worldToViewTfm * modelToWorldTfm,
        "modelToViewTransform" : modelToViewTransform,
        "modelToViewNormalTransform" : modelToViewNormalTransform,
    }
    
    model.render(None, None, transforms)


# This does all the openGL setup and window creation needed
# it hides a lot of things that we will want to get a handle on as time goes by.
magic.runProgram("COSC3000 - Computer Graphics Lab 1, part 2", 1280, 800, renderFrame, initResources, drawUi)

