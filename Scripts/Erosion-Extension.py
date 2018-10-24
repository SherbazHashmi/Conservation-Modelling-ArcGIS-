#-------------------------------------------------------------------------------
# Name:        Erosion-Extension
# Purpose:     Producing an erosion risk model
#
# Author:      Sherbaz
#
# Created:     24/10/2018
# Copyright:   (c) Sherbaz 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy import PolygonToRaster_conversion
from arcpy import Append_management
import numpy;

arcpy.CheckOutExtension('Spatial')
arcpy.ImportToolbox("C:/Users/Sherbaz/Desktop/GIS/extension-content/Soil Erodibility Tools.tbx")

from os.path import isfile, isdir
env.overwriteOutput = True
env.workspace = "C:/Users/Sherbaz/Desktop/GIS/"


## Soil Erosion Concept: Soil erosion : displacement of upper layer of soil.
##  Natural process caused by activity of erosive agents water, ice, snow, air
## Plants Animals etc
#



## Erosion : Universal Soil Loss Equation
## Developed form erosion plot and rainfall simulator experiments
## The USLE is composed of six favtors to predict the long term average
## annual soil loss. Soil Loss  = R x K x L x S x P x C


## R - Rainfall and Runoff Factor
## We don't create a raster for this part of the equation, only use a value
## in the final raster calculator equation (A constant)
## R is the erosive power of a rainstorm
## Found from Wischmeier 1959 and Wischeimer and Smith 1959/
## When factors other than rainfall are held constant, soil losses from
## cultivated fields are directly propritonal to rainstorm
## parameters : Storm Energy E x Maximum 30-min intensity.
## R is 1,500 based on :  Rainfall Erosivity Values New South Wales

#R = 1500;

## K : Soil Sensitivity

## Logic : We already have the soil k-values from govt.
## We just need to classify the soils by name on a map and then associate those
## With k-values from govt tables.   All values not on govt tables are the avg.

#@ Convert Soils from Poly to Raster

#PolygonToRaster_conversion("Soils_Canberra.shp","NAME","soils_usle","CELL_CENTER","NONE",30)

## Set up Classifcation Matrix  with Scalar of k / 1000
#reclassificationMatrix = [["CAMPBELL",40],["BURRA",42],["CELEYS_CREEK",24],
#                            ["WILLIAMSDALE",34],["ROUND_HILL",35],["DISTURBED_TERRAIN",32],
#                            ["MACANALLY_MOUNTAIN",39],["QUEANBEYAN",33],["ANEMBO",45],
#                            ["BOLLARA",36],["FOXLOW_variant_a",36],["FOXLOW",36],
#                            ["BYWONG",47],["PADDY'S_RIVER_variant_a",3],
#                           ["NUNDORA",29],["HOSKINSTOWN",54],["MOLONGLO_variant_a",54],
#                            ["HOSKINSTOWN_variant_a",54],["MOLONGLO",54],["BUNGENDORE",56],
#                            ["HALFWAY_CREEK_variant_a",47], ["MOLONGLO_variant_b",54],["TAYLORS_CREEK",60],
#                            ["PADDY'S_RIVER_variant_c",3],["BENNINSON",36],["MILLS_CROSS",56],
#                            ["HAMMONDS_HILL",33],["WINNUNGA",36],
#                            ["HALFWAY_CREEK",47],["PADDYS_RIVER",3],["WATER",0],
#                            ["CAPTAINS_FLAT",39],["BUTMAROO",39]]

#npreclassification = numpy.array(reclassificationMatrix)
#average = numpy.mean(npreclassification[:,1].astype(numpy.float),axis = 0)
#print(npreclassification[:,1])
#print(average)

#Average Determined to Be : 38.6 but rounded to 39 to match rest
# Reclassify  Raster with Matrix Above fill in missing with 39.
#print( type(reclassificationMatrix[0][0]))
#remapped = RemapValue(reclassificationMatrix)
#reclassifiedRasterInteger = Reclassify(Raster("soils_usle"), "NAME",RemapValue(reclassificationMatrix))
#reclassifiedRasterInteger.save("soils-k-int")

#finalSoilsK = Raster("soils-k-int3") / 1000.0
#finalSoilsK.save("soils-k-float")


# P & C Values from Rosewell 1993
#     ................Erosion...........
#    |3|DS2 Dry    |       1       |       1
#    |1|Pine       |       1       |                                  s
#    |2|Urban      |      0        |
#    |4|B  Ground  |      0          |
#    |5|M Grassland|     5          |
#    |6|D Grassland|       5         |
#    |7|Woodland  |        1       |
#    |8|Water     |         0        |

#pAndCValues = Reclassify("veg2_1","Value",RemapValue([[1,1],[2,0],[3,1],[4,0],[5,5],[6,5],[7,1],[8,0]]))


#LS = Power((Raster("flow_acc") * 30 /22.1),0.1) * Power(Sin(Raster("slope2")* 0.01745)/0.09,1.1) * 1.1


#finalSoilLossContinous = (R * finalSoilsK * pAndCValues * LS)# / 3645.88
#finalSoilLossContinous.save("eros-cont")


# High Values = High Erosion Risk
# Low Values = Low erosion risk.

#finalSoilBoolean = Con((finalSoilLossContinous >= 50),0,1)
#finalSoilBoolean.save("eros-bool");






##################################
# Extension #2, LAB NOTES PT 5
#################################

##This Extension uses Rasters From National-level soil and lanscape data to run
## the USLE. Rather

## Creating References to Raster Grids

soc = Raster(env.workspace+"/soil_grids/soc")




