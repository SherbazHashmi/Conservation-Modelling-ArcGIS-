#-------------------------------------------------------------------------------
# Name:        Forestry Model
# Purpose:     Illustrating Forestry Value
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

# Forestry Model
# Logic : Forest Types + Inverted Erodability           \
# Converting Forest Types into Forest Value
# Logic : Scale of 1 - 10
#   High Value : Pine Forest is Relatively Mature (10)
#     Pine Plantation
#   Medium Value : Eucalypt forests with some potential market value as sawn timber   (6)
#     Dry Eucalypt Woodland
#
#   Low Value : Land that can be planted on. <INTEGRATE AGRICULTURAL MODEL!> (4)
#     Moist Grassland
#     Dry Grassland (Potentially plant dry Eucalypt)
#
#   No Value : Bare Ground (0)
#                  Urban
#                  Agricultural Model gives 0.
#
# Erodability : Low Erodability Values = More Valuable.
# Hence we need to invert the values for suitability

reclassifiedForestryValues = [["1",10],["2",0],["3",0],["4",0],["5",5],["6",4],["7",6],["8",0]]

reclassifiedForestryRaster = Reclassify("veg2_1","VALUE",RemapValue(reclassifiedForestryValues))
reclassifiedForestryRaster.save("recforrast")
scaledReclassifiedForestryRaster = Raster("recforrast") / 10.0

# Scaling Erodability to 0-1
originalErosion = Raster("eros-cont")
thresholdErosion = Con(originalErosion>50,50,originalErosion)
scaledErosion = thresholdErosion / 50
invertedErosion = 1- scaledErosion

forestryValue = (scaledReclassifiedForestryRaster * 0.5) + (scaledErosion * 0.5)
scaledReclassifiedForestryRaster.save("foroval_2")

