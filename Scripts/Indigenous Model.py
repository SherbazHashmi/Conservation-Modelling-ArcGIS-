#-------------------------------------------------------------------------------
# Name:        Indigenous Model
# Purpose:
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


arcpy.CheckOutExtension('Spatial')

from os.path import isfile, isdir
env.overwriteOutput = True
env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"

#Indigenous Model
# Maximum Value = 261 Hence to Scale we are going to divide the values in raster
# by 261

indigenousRasterScaled = Raster("ASDST_P.tif") / 261.0
indigenousRasterScaled.save("Fuzz_Indg")
