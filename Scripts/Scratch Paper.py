#-------------------------------------------------------------------------------
# Name:        Scratch Paper
# Purpose:     Quickly Edit Models without Running All Lab Notes
#
# Author:      Sherbaz
#
# Created:     30/10/2018
# Copyright:   (c) Sherbaz 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import PolygonToRaster_conversion
from arcpy import Append_management


arcpy.CheckOutExtension('Spatial')

from os.path import isfile, isdir
env.overwriteOutput = True
env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"
constrainedBuildingModel = Raster("finalflood") * Raster("firemod") * Raster("eros-bool-2")
constrainedBuildingModel.save("conbModel")