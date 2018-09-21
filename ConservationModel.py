#-------------------------------------------------------------------------------
# Name:        Conservation Model
# Purpose:
#
# Author:      Sherbaz
#
# Created:     24/08/2018
# Copyright:   (c) Sherbaz 2018
# Licence:
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"

#Reclassifies the raster.
outReclass1 = Reclassify("veg2_1","Value",RemapValue([[1,0],[2,0],[3,1],[4,0],[5,0],[6,0],[7,0],[8,1]]))

#Saves the Reclassified Raster as Unique_1.
outReclass1.save("C:/Users/Sherbaz/Desktop/GIS/Conservation_Model/unique_1")


