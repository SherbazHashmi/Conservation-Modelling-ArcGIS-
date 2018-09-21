#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Sherbaz
#
# Created:     31/08/2018
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
saveLocation = "C:/Users/Sherbaz/Desktop/GIS/"



def reclassification ():
    #Reclassifies the raster.
    outReclass1 = Reclassify("veg2_1","Value",RemapValue([[1,0],[2,0],[3,1],[4,0],[5,0],[6,0],[7,0],[8,1]]))

    #Saves the Reclassified Raster as Unique_1.
    outReclass1.save("C:/Users/Sherbaz/Desktop/GIS/unique_1")

def flowDirection(inputSurfaceRaster,outFlowDirectionLocation):
    # Perform Flow Direction Calculation
    outflowDirection = FlowDirection(inputSurfaceRaster,"NORMAL")
    outflowDirection.save(outFlowDirectionLocation)
    return outFlowDirectionLocation


def sink(in_flow_direction_raster, out_raster_name):
    out_raster = Sink(in_flow_direction_raster)
    out_raster.save(saveLocation + out_raster_name)
    return out_raster_name

def fill(in_surface_raster, outputSurfaceRaster):
    z_limit = 10;
    fill = Fill(in_surface_raster,z_limit)
    fill.save(saveLocation+outputSurfaceRaster)
    print(saveLocation+outputSurfaceRaster)
    return outputSurfaceRaster


# Running Flow Direction the First Time

#inputSurfaceRaster = "dem.tif"
#flowD = flowDirection(inputSurfaceRaster,"flow_dir");

# Sinking
#sink(flowD, "sinks")

# Filling

#fill(inputSurfaceRaster, "fill_dem")

# Rerunning Flow Direction

#flowDirection("fill_dem","flow_dir2")

# Flow Accumulation

#FlowAccumulation("flow_dir2").save(saveLocation+"flow_acc")



#Creating A Stream Location Raster

#outputRaster = Con(Raster("flow_acc") >=100,1,0)
#outputRaster.save(saveLocation+"streamnet_1")


#Stream Buffers
# Decision Based On : http://www.water.nsw.gov.au/__data/assets/pdf_file/0004/547222/licensing_approvals_controlled_activities_riparian_corridors.pdf
# 60 meters on either side of the stream (2 pixels (30))

#streambuffers = Expand("streamnet_1",'2',1)
#streambuffers.save(saveLocation+ "buffstream")

#Road Buffers

# Goal : Conversion of Road Buffers (Vector Line Format Roads -> Raster)

#Extent environment will only process features or rasters that fall within the extent specified setting.
   #Getting the Extent of dem.tif
#demRaster = arcpy.sa.Raster(saveLocation+"dem.tif")
   # Setting Current Environment Extent to Dem.
#arcpy.env.extent = demRaster.extent

#Converting to Raster
#arcpy.PolylineToRaster_conversion("Main_roads.shp","FID",saveLocation+"roadgrid","MAXIMUM_COMBINED_LENGTH","NONE",30)

# Changing the Value of the Raster Cells that Represent main Roads
# into a single cell value. We need to change background values to 0s
# as at the moment they are NODATA cells.

#changedRoadgrid = Con(IsNull("roadgrid"),0,1)
#changedRoadgrid.save(saveLocation + "roadgrid2")

# Using Expand tool to buffer the main roads
#roadBuffers = Expand("roadgrid2",'2',1)
#roadBuffers.save(saveLocation + "buffroad2")


#Combining The Buffers and Vegetation
initialConservationModel = (Raster(saveLocation+"/Conservation_Model/unique_1") * 0.33) + (Raster(saveLocation+"buffstream") * 0.33) + (Raster(saveLocation+"buffroad2") * 0.33)
initialConservationModel.save(saveLocation+"consm1")

#Setting 0s to NODATA in streamnet grid for EuDistance
