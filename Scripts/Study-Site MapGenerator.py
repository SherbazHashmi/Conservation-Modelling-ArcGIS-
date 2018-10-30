#-------------------------------------------------------------------------------
# Name:        Study-Site Map Generator
# Purpose:     Clip Models to Study Site
#
# Author:      Sherbaz
#
# Created:     29/10/2018
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

#Setting Up Study Site Clip
studySite = arcpy.PolygonToRaster_conversion("Study_Site.shp","FID","study_site","CELL_CENTER","",30)
studySiteReclass = Reclassify(Raster("study_site"),"VALUE",RemapValue([[0,1],[1,1]]))
studySiteReclass.save("ss")

# Clip Model Clips the Model to The Study Site Area
def clipModel (model,output):
    model = SetNull(IsNull(Raster("ss")),model)
    model.save(output)

# Clipping All Models to Study Site

clipModel(Raster("fuzz_cons1"),"c_fuzz_cons")
clipModel(Raster("ag_model_1"),"c_ag")
clipModel(Raster("foroval_2"),"c_for")
clipModel(Raster("Fuzz_Indg"),"c_ind")
clipModel(Raster("conbModel"),"c_conb")
clipModel(Raster("finalmola"),"c_mola")


#Clipping Helper Data
clipModel(Raster("soils3"),"c_soils")
clipModel(Raster("dem.tif"),"c_dem")
clipModel(Raster("roadsv3"),"c_roads")


