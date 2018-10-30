#-------------------------------------------------------------------------------
# Name:        MOLA
# Purpose:     Creating MOLA with Highest Position
#
# Author:      Sherbaz
#
# Created:     29/10/2018
# Copyright:   (c) Sherbaz 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Creating MOLA
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import PolygonToRaster_conversion
from arcpy import Append_management


arcpy.CheckOutExtension('Spatial')

from os.path import isfile, isdir
env.overwriteOutput = True
env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"
MOLA = HighestPosition([(1.2 * Raster("fuzz_cons1")),
						(1 * Raster("ag_model_1")),
						(1.1 * Raster("foroval_2")),
						(1.2 *Raster("Fuzz_Indg")),
						(1.5 * Raster("conbModel"))])
MOLA.save("finalMola")
