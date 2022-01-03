#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import os
import sys
import re
import json

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtk import vtkWindowToImageFilter

# from vtk import vtkAVIWriter
from vtkmodules.vtkIOOggTheora import vtkOggTheoraWriter 

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkHull
from vtkmodules.vtkFiltersExtraction import vtkExtractEdges
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkPlaneSource,
)
from vtkmodules.vtkCommonDataModel import (
    vtkHexahedron,
    vtkUnstructuredGrid
)
from vtk import vtkTextActor
from vtkmodules.vtkRenderingAnnotation import (
    vtkAxesActor,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkProperty,
    vtkTextProperty,
)
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints
)

EPS = 1.0e-2
color_names = ['antique_white', 'azure', 'bisque', 'blanched_almond', 'cornsilk', 'eggshell', 'floral_white', 'gainsboro',
                       'ghost_white', 'honeydew', 'ivory', 'lavender', 'lavender_blush', 'lemon_chiffon', 'linen', 'mint_cream',
                       'misty_rose', 'moccasin', 'navajo_white', 'old_lace', 'papaya_whip', 'peach_puff', 'seashell', 'snow',
                       'thistle', 'titanium_white', 'wheat', 'white', 'white_smoke', 'zinc_white','cold_grey', 'dim_grey', 
                       'grey', 'light_grey', 'slate_grey', 'slate_grey_dark', 'slate_grey_light', 'warm_grey', 
                       'black', 'ivory_black', 'lamp_black', 'alizarin_crimson', 'brick', 'cadmium_red_deep', 'coral',
                       'coral_light', 'deep_pink', 'english_red', 'firebrick','geranium_lake', 'hot_pink', 'indian_red', 
                       'light_salmon', 'madder_lake_deep', 'maroon', 'pink', 'pink_light', 'raspberry', 'red', 'rose_madder', 
                       'salmon', 'tomato', 'venetian_red', 'beige', 'brown', 'brown_madder', 'brown_ochre', 'burlywood', 
                       'burnt_sienna', 'burnt_umber', 'chocolate', 'deep_ochre', 'flesh', 'flesh_ochre', 'gold_ochre',
                       'greenish_umber', 'khaki', 'khaki_dark', 'light_beige', 'peru', 'rosy_brown', 'raw_sienna', 'raw_umber', 
                       'sepia', 'sienna', 'saddle_brown', 'sandy_brown', 'tan', 'van_dyke_brown', 'cadmium_orange', 
                       'cadmium_red_light', 'carrot','dark_orange', 'mars_orange', 'mars_yellow', 'orange', 'orange_red', 
                       'yellow_ochre', 'aureoline_yellow', 'banana', 'cadmium_lemon','cadmium_yellow', 'cadmium_yellow_light', 
                       'gold', 'goldenrod', 'goldenrod_dark', 'goldenrod_light', 'goldenrod_pale', 'light_goldenrod', 
                       'melon', 'naples_yellow_deep', 'yellow', 'yellow_light', 'chartreuse', 'chrome_oxide_green', 
                       'cinnabar_green', 'cobalt_green', 'emerald_green', 'forest_green', 'green', 'green_dark', 'green_pale', 
                       'green_yellow', 'lawn_green', 'lime_green', 'mint', 'olive', 'olive_drab', 'olive_green_dark', 
                       'permanent_green', 'sap_green', 'sea_green', 'sea_green_dark', 'sea_green_medium', 'sea_green_light', 
                       'spring_green', 'spring_green_medium', 'terre_verte', 'viridian_light', 'yellow_green', 'aquamarine', 
                       'aquamarine_medium', 'cyan', 'cyan_white', 'turquoise', 'turquoise_dark', 'turquoise_medium',
                       'turquoise_pale', 'alice_blue', 'blue', 'blue_light', 'blue_medium', 'cadet', 'cobalt', 'cornflower', 
                       'cerulean', 'dodger_blue', 'indigo', 'manganese_blue', 'midnight_blue', 'navy', 'peacock', 'powder_blue',
                       'royal_blue', 'slate_blue', 'slate_blue_dark', 'slate_blue_light', 'slate_blue_medium', 'sky_blue', 
                       'sky_blue_deep', 'sky_blue_light', 'steel_blue', 'steel_blue_light', 'turquoise_blue', 'ultramarine', 
                       'blue_violet', 'cobalt_violet_deep', 'magenta', 'orchid', 'orchid_dark', 'orchid_medium',
                       'permanent_red_violet', 'plum', 'purple', 'purple_medium', 'ultramarine_violet', 'violet',
                       'violet_dark', 'violet_red', 'violet_red_medium', 'violet_red_pale'
                  ]

# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# Some stuff for boundary box creation 

def MakeHexahedron(boundary_coords):
    numberOfVertices = 8

    # Create the points
    points = vtkPoints()
    points.InsertNextPoint(boundary_coords['x_min'], boundary_coords['y_min'], boundary_coords['z_min'])
    points.InsertNextPoint(boundary_coords['x_max'], boundary_coords['y_min'], boundary_coords['z_min'])
    points.InsertNextPoint(boundary_coords['x_max'], boundary_coords['y_max'], boundary_coords['z_min'])
    points.InsertNextPoint(boundary_coords['x_min'], boundary_coords['y_max'], boundary_coords['z_min'])
    
    points.InsertNextPoint(boundary_coords['x_min'], boundary_coords['y_min'], boundary_coords['z_max'])
    points.InsertNextPoint(boundary_coords['x_max'], boundary_coords['y_min'], boundary_coords['z_max'])
    points.InsertNextPoint(boundary_coords['x_max'], boundary_coords['y_max'], boundary_coords['z_max'])
    points.InsertNextPoint(boundary_coords['x_min'], boundary_coords['y_max'], boundary_coords['z_max'])
    # Create a hexahedron from the points
    hex_ = vtkHexahedron()
    for i in range(0, numberOfVertices):
        hex_.GetPointIds().SetId(i, i)

    # Add the points and hexahedron to an unstructured grid
    uGrid = vtkUnstructuredGrid()
    uGrid.SetPoints(points)
    uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())

    return uGrid
            
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================

def main():
    colors = vtkNamedColors()
    
    backProperty = vtkProperty()
    backProperty.SetColor(colors.GetColor3d('PeachPuff'))
    
#     with open('vis_conf.txt') as f:
    with open(sys.argv[2]) as f:
        data = f.read()
        configuration_parameters = json.loads(data)
    
    fps = int(configuration_parameters['fps'])
    resolution = (configuration_parameters['resolution'])
    
    pattern = re.compile(".*metadata.json")
    for i in sorted(os.listdir(sys.argv[1])):
        if pattern.match(i):
            with open(os.path.join(sys.argv[1],i)) as f:
                data = f.read()
                meta_parameters = json.loads(data)

    balls_count = int(meta_parameters['balls_count'])
    max_time = float(meta_parameters['max_time'])
    boundary_coords = json.loads(meta_parameters['boundary_coords'])
    boundary_keys = json.loads(meta_parameters['boundary_coords'])
#   ==================

    ren = vtkRenderer()
    
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetOffScreenRendering(True)
#   ==================

#     Create a set of spheres with defined properties 
    balls = {}
    mappers_balls = {}
    actors_balls = {} 
    
    for i in range(balls_count):
        ball = vtkSphereSource()
        ball.SetCenter(meta_parameters[f'ball_id_{i}']['initial_center_position'])
        ball.SetRadius(meta_parameters[f'ball_id_{i}']['radius'])
        ball.SetPhiResolution(30)
        ball.SetThetaResolution(30)
        balls[i] = ball
        mappers_balls[i] = vtkPolyDataMapper()
        mappers_balls[i].SetInputConnection(balls[i].GetOutputPort())
        actors_balls[i] = vtkActor()
        actors_balls[i].SetMapper(mappers_balls[i])
        actors_balls[i].GetProperty().SetColor(colors.GetColor3d(meta_parameters[f'ball_id_{i}']['color']))
        ren.AddActor(actors_balls[i])
        
#   ==================

#     Create a boundary box  
    hexahedron = MakeHexahedron(boundary_coords)
    mapper_hex = vtkDataSetMapper()
    mapper_hex.SetInputData(hexahedron)
    actor_hex = vtkActor()
    actor_hex.SetMapper(mapper_hex)
    actor_hex.GetProperty().SetColor(colors.GetColor3d('Moccasin'))
    actor_hex.GetProperty().SetSpecular(0.7)
    actor_hex.GetProperty().SetOpacity(0.3)
    actor_hex.SetBackfaceProperty(backProperty)
    ren.AddActor(actor_hex)

#   ==================

#     Create a plane
    planeSource = vtkPlaneSource()
    x_box_size = boundary_coords['x_max'] - boundary_coords['x_min']
    y_box_size = boundary_coords['y_max'] - boundary_coords['y_min']
    planeSource.SetOrigin(boundary_coords['x_min'] - x_box_size, boundary_coords['y_min'] - y_box_size, boundary_coords['z_min'] - 0.1)
    planeSource.SetPoint1(boundary_coords['x_max'] + x_box_size, boundary_coords['y_min'] - y_box_size, boundary_coords['z_min'] - 0.1)
    planeSource.SetPoint2(boundary_coords['x_min'] - x_box_size, boundary_coords['y_max'] + y_box_size, boundary_coords['z_min'] - 0.1)
    planeSource.SetXResolution(100)
    planeSource.Update()
    mapper_plane = vtkPolyDataMapper()
    mapper_plane.SetInputData(planeSource.GetOutput())
    actor_plane = vtkActor()
    actor_plane.SetMapper(mapper_plane)
    actor_plane.GetProperty().SetColor(colors.GetColor3d('goldenrod_dark'))
    ren.AddActor(actor_plane)
    
#   ==================

    # Set up the lighting and other property of camera
    light = vtkLight()
    light.SetFocalPoint(1.875, 0.6125, 0)
    light.SetPosition(-100, 100, 300)
    
    
    transform = vtkTransform()
    transform.Translate(boundary_coords['x_min'], boundary_coords['y_min'], boundary_coords['z_min'])
    actor_axis = vtkAxesActor()
    actor_axis.SetUserTransform(transform)
    actor_axis.SetConeRadius(0.2)
    actor_axis.SetTotalLength(1.5 * boundary_coords['x_max'], 1.5 * boundary_coords['y_max'], 1.5 * boundary_coords['z_max'])
    label_text_property = vtkTextProperty()
    label_text_property.SetColor(0, 0, 0)
    label_text_property.SetFontFamilyToArial()
    label_text_property.SetOpacity(0.8)
    for label in [
        actor_axis.GetXAxisCaptionActor2D(),
        actor_axis.GetYAxisCaptionActor2D(),
        actor_axis.GetZAxisCaptionActor2D(),
        ]:
        label.SetWidth(label.GetWidth() * 0.5)
        label.SetHeight(label.GetHeight() * 0.5)
        label.SetCaptionTextProperty(label_text_property)
    ren.AddActor(actor_axis)
    
    timer_actor = vtkTextActor()
    timer_actor.GetTextProperty().SetFontSize(30)
    timer_actor.GetTextProperty().SetColor(colors.GetColor3d('Red'))
    timer_actor.SetPosition2((0, 0))
    timer_actor.SetInput('0.0 sec')
    ren.AddActor(timer_actor)
    
    
    ren.AddLight(light)
    ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
    ren.GetActiveCamera().SetPosition(50, 50, 70)
    ren.GetActiveCamera().SetViewUp(0, 0, 1)
#     ren.GetActiveCamera().Azimuth(180)
#     ren.GetActiveCamera().Yaw(np.pi/2)
#     ren.GetActiveCamera().Pitch(np.pi/2)
#     ren.GetActiveCamera().Elevation(100)
#     ren.GetActiveCamera().Roll(90)
    ren.GetActiveCamera().Zoom(0.5)
    ren.ResetCamera()
    ren.GetActiveCamera().SetParallelScale(2.0)
    ren.SetBackground(colors.GetColor3d('ivory'))
    renWin.SetSize(resolution['x'], resolution['y'])
    renWin.Render()
#   ==================   
    
    windowToImageFilter = vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.SetInputBufferTypeToRGB()
    windowToImageFilter.ReadFrontBufferOff()
    windowToImageFilter.Update()
    
    
    OTwriter = vtkOggTheoraWriter()
    OTwriter.SetRate(fps)
    OTwriter.SetInputConnection(windowToImageFilter.GetOutputPort())
    OTwriter.SetFileName("bouncing_balls.ogv")
    
    renWin.Render()
    OTwriter.Start()
    OTwriter.Write()
    
    
    pattern = re.compile(".*data_[0-9]+.json")
    for i in sorted(os.listdir(sys.argv[1])):
        if(pattern.match(i)):
            with open(os.path.join(sys.argv[1], i)) as f:
                data = f.read()
                parameters = json.loads(data)
            indices_to_delete = []
            for j, ball in balls.items():
                    if f'ball_id_{j}' in parameters.keys():
                        ball.SetCenter(tuple(parameters[f'ball_id_{j}']['position']))
                    else:
                        indices_to_delete.append(j)
            for j in indices_to_delete:
                ren.RemoveActor(actors_balls[j]);
                del(balls[j])
                del(mappers_balls[j])
                del(actors_balls[j])
            del(indices_to_delete)
            curr_time = parameters['metadata']['current_time']
            timer_actor.SetInput(f'{curr_time:.3f} sec')
            renWin.Render()
            windowToImageFilter.Modified()
            OTwriter.Write()
    
    
    
    OTwriter.End()
    
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================

if __name__ == '__main__':
    main()

