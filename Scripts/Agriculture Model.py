#-------------------------------------------------------------------------------
# Name:        Agriculture Model
# Purpose:
#
# Author:      Sherbaz
#
# Created:     30/10/2018
# Copyright:   (c) Sherbaz 2018
# Licence:     <your licence>
# Note : Due to String Type Remap, the classification has to be done in ArcMap
#-------------------------------------------------------------------------------


import arcpy
from arcpy import env
from arcpy.sa import *


arcpy.CheckOutExtension('Spatial')

from os.path import isfile, isdir
env.overwriteOutput = True
env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"

#SOIL

#Converting Soils Data into Raster Format

# First Setting Extent to Match the Dem
demRaster = arcpy.sa.Raster(env.workspace +"/dem.tif")
arcpy.env.extent = demRaster.extent  # (What does this actually mean (?))
PolygonToRaster_conversion("Soils_Canberra.shp","LANDSCAPE", env.workspace + "/Soils2", "CELL_CENTER",  "NONE", 30)

# Reclassifying the Soil Types to Rank the Soils2 Raster
remappedValues =[['COca', 2], ['TRba', 4], ['ERcc', 5], ['TRwi', 2],
 ['COrh', 2], ['DTxx', 2], ['ERmm', 5], ['VEqn', 4], ['REan', 2],
 ['ERbo', 4], ['COfoa', 2], ['COfo', 1], ['ALcf', 2], ['VEby', 7],
 ['ALpda', 6], ['TRnu', 2], ['VEhs', 5], ['ALmga', 9], ['VEhsa', 2],
 ['ALmg', 9], ['TRbz', 7], ['ALmgb', 2], ['ALhfa', 2], ['ERtc', 2],
 ['ALpdc', 6], ['ERbe', 3], ['STmx', 8],  ['CObt', 2], ['ERhh', 2],
 ['TRwn', 7],  ['ALhf', 5],  ['ALpd', 6],  ['WATER', 2]]

reclassifiedSoilRaster = Reclassify("Soils2","LANDSCAPE",RemapValue(remappedValues))
reclassifiedSoilRaster.save(env.workspace + "/Soils3");

#Dividing Soils 3 by 10.0 (Should Produce Scale Ranging from 0.0-1.0)

scaledSoils = Raster("soils3") / 10.0
scaledSoils.save(env.workspace + "/soils4")

#SLOPE : Differentiate Agricultural Land into Membership of "Suitable Slope"
#   using fuzzy/ continious approach.
# High slope = No Agricultural Activity
# Moderate Slope = Little Machine Agriculture and Erosion could be an issue.
# Low Slopes = Machine Intensive Agriculture is Possible.

# Objective : Calculate Slope from DEM and then Generate Fuzzy Representation
# of suitability

#Getting Slope Raster

slopeRaster = Slope("dem.tif","DEGREE",1)
slopeRaster.save("slope2");

#Setting Slopes Over Threshold to NoData

nodataSlope = SetNull(Raster(env.workspace + "/slope2") >=15,Raster(env.workspace +"/slope2"))
nodataSlope.save("ag_slope")

# Dividing the Result by 15.0 (to rescale it from 0.0 to 1.0) and subtracting 1
# to invert it

agSlope = (1  - Raster("ag_slope") / 15)
agSlope.save("ag_slope2")

# Converting the NODATA values back to zero and retaining values from ag_slope2

withoutNoDataAgSlope = Con(IsNull(Raster("ag_slope2")),0,Raster("ag_slope2"))
withoutNoDataAgSlope.save("ag_slope3")

# Merging Raster for Soils and Slope to Create Agricultural Suitability Model
agriculturalModel = (Raster("soils4") * 0.5) + (Raster("ag_slope3") * 0.5)
agriculturalModel.save("ag_model_1")


