#-------------------------------------------------------------------------------
# Name:        Lab Notes Pt2
# Purpose:     Producing a Conservation Model
#
# Author:      Sherbaz
#
# Created:     31/08/2018
# Copyright:   (c) Sherbaz 2018
# Comments:   Ignore All Commented Code that are
#             not notes as It Was Not Used in Assessment
#
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
    outReclass1 = Reclassify("veg2_1","Value",RemapValue([[1,5],[2,0],[3,10],[4,0],[5,8],[6,8],[7,6],[8,0]]))
    outReclass1 = outReclass1 / 10.0
    outReclass1 = 1 - outReclass1 # Inverting  

    #Saves the Reclassified Raster as Unique_2.
    outReclass1.save("C:/Users/Sherbaz/Desktop/GIS/unique_2")

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

# Reclassifying Veg2
reclassification();

# Running Flow Direction the First Time

inputSurfaceRaster = "dem.tif"
flowD = flowDirection(inputSurfaceRaster,"flow_dir");

# Sinking
sink(flowD, "sinks")

# Filling

fill(inputSurfaceRaster, "fill_dem")

# Rerunning Flow Direction

flowDirection("fill_dem","flow_dir2")

# Flow Accumulation

FlowAccumulation("flow_dir2").save(saveLocation+"flow_acc")



#Creating A Stream Location Raster

outputRaster = Con(Raster("flow_acc") >=100,1,0)
outputRaster.save(saveLocation+"streamnet_1")


#Stream Buffers
# Decision Based On : http://www.water.nsw.gov.au/__data/assets/pdf_file/0004/547222/licensing_approvals_controlled_activities_riparian_corridors.pdf
# 60 meters on either side of the stream (2 pixels (30))

# streambuffers = Expand("streamnet_1",'2',1)
# streambuffers.save(saveLocation+ "buffstream")

#Road Buffers

# Goal : Conversion of Road Buffers (Vector Line Format Roads -> Raster)

#Extent environment will only process features or rasters that fall within the extent specified setting.
   #Getting the Extent of dem.tif
demRaster = arcpy.sa.Raster(saveLocation+"dem.tif")
   # Setting Current Environment Extent to Dem.
arcpy.env.extent = demRaster.extent

#Converting to Raster
arcpy.PolylineToRaster_conversion("Main_roads.shp","FID",saveLocation+"roadgrid","MAXIMUM_COMBINED_LENGTH","NONE",30)

# Changing the Value of the Raster Cells that Represent main Roads
# into a single cell value. We need to change background values to 0s
# as at the moment they are NODATA cells.

# changedRoadgrid = Con(IsNull("roadgrid"),0,1)
# changedRoadgrid.save(saveLocation + "roadgrid2")

# Using Expand tool to buffer the main roads
# roadBuffers = Expand("roadgrid2",'2',1)
# roadBuffers.save(saveLocation + "buffroad2")


# Combining The Buffers and Vegetation
# initialConservationModel = (Raster(saveLocation+"/Conservation_Model/unique_1") * 0.33) + (Raster(saveLocation+"buffstream") * 0.33) + (Raster(saveLocation+"buffroad2") * 0.33)
# initialConservationModel.save(saveLocation+"consm1")

# Euclidian Distance (FUZZY CONSERVATION!!! Minus the Unique Aspect)

# Setting 0s to NODATA in streamnet grid for EuDistance
nodataStreamnet= SetNull(Raster(saveLocation+"streamnet_1") < 1,1)
nodataStreamnet.save("streamnet_3")

# Calculating EU Distance
euDistanceRaster = EucDistance(Raster("streamnet_3"), cell_size = 30)
euDistanceRaster.save("eucstream")

fuzzStream = Con(Raster("eucstream") <= 30, 0, Con(Raster("eucstream") >= 300, 1, (Raster("eucstream") - 30.0) / (300.0 - 30.0)))
fuzzStream.save("fuzzstream")

# Creating Fuzzy Buffers for Roads and Unique Vegetation

# Vegetation and Vegetation
# Setting anything under 1 to a no data in preperation for EuDistance

#nodataUnique = SetNull(Raster(saveLocation+"Conservation_Model/unique_1")<1,1)
#nodataUnique.save(saveLocation+"unique_2")

nodataRoads = SetNull(Raster(saveLocation+"roadgrid2")<1,1)
nodataRoads.save(saveLocation+"roadgrid3")

# Calculating EU Distance
euDistanceRasterRoads = EucDistance(Raster("roadgrid3"), cell_size = 30)
euDistanceRasterRoads.save("eucroads")

#euDistanceRasterUnique = EucDistance(Raster("unique_2"), cell_size = 30)
#euDistanceRasterUnique.save("eucunique")

# Rescaling the Figures to give a "Fuzzy" range of 0.0 to 1.0

fuzzRoads = Con(Raster("eucroads") <= 30, 0, Con(Raster("eucroads") >= 300, 1, (Raster("eucroads") - 30.0) / (300.0 - 30.0)))
#fuzzUnique = Con(Raster("eucunique") <= 30, 0, Con(Raster("eucunique") >= 300, 1, (Raster("eucunique") - 30.0) / (300.0 - 30.0)))

fuzzRoads.save(saveLocation+"fuzzroads")
#fuzzUnique.save(saveLocation + "fuzzunique")


#CONSERVATION MCE
# MCE Calculation Combining all Fuzzy Rasters to Build Fuzzy Conservation Model

fuzzyConservationModel = (Raster(saveLocation+"fuzzstream") * 0.33) + (Raster(saveLocation+"fuzzroads") * 0.33) + (Raster(saveLocation+"unique_2") * 0.33)
fuzzyConservationModel.save(saveLocation + "fuzz_cons1")







