#-------------------------------------------------------------------------------
# Name:        LabNotesPt3
# Purpose:
#
# Author:      Sherbaz
#
# Created:     04/10/2018
# Copyright:   (c) Sherbaz Hashmi 2018
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

#SOIL

#Converting Soils Data into Raster Format

# First Setting Extent to Match the Dem
##demRaster = arcpy.sa.Raster(env.workspace +"/dem.tif")
##arcpy.env.extent = demRaster.extent  # (What does this actually mean (?))
##PolygonToRaster_conversion("Soils_Canberra.shp","LANDSCAPE", env.workspace + "/Soils2", "CELL_CENTER",  "NONE", 30)

# Reclassifying the Soil Types to Rank the Soils2 Raster
##remappedValues =[['COca', 2], ['TRba', 4], ['ERcc', 5], ['TRwi', 2],
 ##['COrh', 2], ['DTxx', 2], ['ERmm', 5], ['VEqn', 4], ['REan', 2],
 ##['ERbo', 4], ['COfoa', 2], ['COfo', 1], ['ALcf', 2], ['VEby', 7],
 ##['ALpda', 6], ['TRnu', 2], ['VEhs', 5], ['ALmga', 9], ['VEhsa', 2],
 ##['ALmg', 9], ['TRbz', 7], ['ALmgb', 2], ['ALhfa', 2], ['ERtc', 2],
 ##['ALpdc', 6], ['ERbe', 3], ['STmx', 8],  ['CObt', 2], ['ERhh', 2],
 ##['TRwn', 7],  ['ALhf', 5],  ['ALpd', 6],  ['WATER', 2]]

##reclassifiedSoilRaster = Reclassify("Soils2","LANDSCAPE",RemapValue(remappedValues))
##reclassifiedSoilRaster.save(env.workspace + "/Soils3");

#Dividing Soils 3 by 10.0 (Should Produce Scale Ranging from 0.0-1.0)

##scaledSoils = Raster("soils3") / 10.0
##scaledSoils.save(env.workspace + "/soils4")

#SLOPE : Differentiate Agricultural Land into Membership of "Suitable Slope"
#   using fuzzy/ continious approach.
# High slope = No Agricultural Activity
# Moderate Slope = Little Machine Agriculture and Erosion could be an issue.
# Low Slopes = Machine Intensive Agriculture is Possible.

# Objective : Calculate Slope from DEM and then Generate Fuzzy Representation
# of suitability

#Getting Slope Raster

##slopeRaster = Slope("dem.tif","DEGREE",1)
##slopeRaster.save("slope2");

#Setting Slopes Over Threshold to NoData

##nodataSlope = SetNull(Raster(env.workspace + "/slope2") >=15,Raster(env.workspace +"/slope2"))
##nodataSlope.save("ag_slope")

# Dividing the Result by 15.0 (to rescale it from 0.0 to 1.0) and subtracting 1
# to invert it (!! Why do we invert it?)

##agSlope = (1  - Raster("ag_slope") / 15)
##agSlope.save("ag_slope2")

# Converting the NODATA values back to zero and retaining values from ag_slope2

##withoutNoDataAgSlope = Con(IsNull(Raster("ag_slope2")),0,Raster("ag_slope2"))
##withoutNoDataAgSlope.save("ag_slope3")

# Merging Raster for Soils and Slope to Create Agricultural Suitability Model
##agriculturalModel = (Raster("soils4") * 0.5) + (Raster("ag_slope3") * 0.5)
##agriculturalModel.save("ag_model_1")


# Forestry Model

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

##reclassifiedForestryValues = [["1",10],["2",0],["3",0],["4",0],["5",5],["6",4],["7",6],["8",0]]

##reclassifiedForestryRaster = Reclassify("veg2_1","VALUE",reclassifiedForestryValues)
##reclassifiedForestryRaster.save("recforrast")
##scaledReclassifiedForestryRaster = Raster("recforrast") / 10.0
##scaledReclassifiedForestryRaster.save("foroval_2")

#Indigenous Model
# Maximum Value = 261 Hence to Scale we are going to divide the values in raster
# by 261

#indigenousRasterScaled = Raster("ASDST_P.tif") / 261.0
#indigenousRasterScaled.save("Fuzz_Indg")



# Building Model Method
# Composed of Two Components
# Cost and Value
# Cost is made of : Slope Cost and Distance Cost
# Slope Cost :
# As slope increases, the higher the cost for building and the land is less
#   suitable for building.
#
# As Distance From Tracks and Roads Increases, the building costs get higher
# the land is less suitable for building.
# Value is composed of Aspect Value and View Value.
# Aspect Value : Composed of Aspects  (Solar Passive Housing)
# View Value : Higher up, the better the views. From the DEM.
# Combining Both Location and View Should give an Overall Location value raster
#Combining Cost and Value Raster Should Give Overall Building Suitability Raster

#Costs

#Slope Raster : slope2 already saved from prior step

#slopeCost = 1 / Raster("slope2")
#slopeCostStandardised = (slopeCost / (slopeCost.maximum)   )
#slopeCostStandardised.save("slopeCost2")

# Distance Cost =  1 / EuDistnace AggTracksRoads

# Combining Road and Track Rasters with Buffers
##aggTrackRoad = Raster("roadgrid3") # + Raster("trackGrid")
##aggTrackRoad.save("aggTrackRoad")

#EuDistance

##euDistanceTrackRoad = EucDistance(Raster("aggTrackRoad"), cell_size = 30)
##euDistanceTrackRoad.save("euctrackroad")

#Standardise EuDistance with FuzzyStreamBufferEquation

#fuzzTrackRoad = Con(Raster("euctrackroad") <= 30, 0, Con(Raster("euctrackroad") >= 300, 1, (Raster("euctrackroad") - 30.0) / (300.0 - 30.0)))
#fuzzTrackRoad.save("fuzzroad")

#Inverse of FuzzTrackRoad

#distanceCost = 1 -  Raster("fuzzroad")
#distanceCost.save("distanceCost")

# Merging Costs each with 0.5 weighting

#cost = (slopeCostStandardised * 0.5) + (Raster("distanceCost") * 0.5)
#cost.save("cost2")

# Value

# Logic : The Higher Up There will Be Better Views (Hence More Value)
# Note : Need to standardise from 0-1

#dem = Raster("dem.tif")
#minimum = dem.minimum
#maximum = dem.maximum
#elevationValue = (dem - minimum) / (maximum - minimum)
#elevationValue.save("viewValue")

#Aspect Model : Solar Passive Housing
# Aspect Gives you Which Way it is Facing
# Assuming North is 180 - 270 then we can use reclassification to see how well
# the aspect is.
# Group that with the Trees in the Are which coukld potentially block the sun
# from coming in


#aspect = Aspect("dem.tif")
#aspect.save("aspect")

#Standardised Raster

#newRaster = Con(((aspect >= 90) & (aspect <= 270)),1,0)
#newRaster.save("solarpassive2")


#value = (Raster("solarpassive2") * 0.5)+ (Raster("viewValue") * 0.5)
#value.save("value")

#buildingModel = (Raster("value") * 0.5) + (Raster("cost2") * 0.5)
#buildingModel.save("buildmodel2")


#Fire Model

#Fire intensity is calculated by a worst case situation
# 1. Construct Extreme Climactic Conditions
#   - Calculate days since rain : 15
#   - Calculate Last Rain Fall Event 4mm
# 2. Determine McArthur Drought Index: 10
# 3. Apply the other constructed parameters
#   - Temperature : 380C
#   - Relative Humidity : 15%
#   - Wind Speed : 40Km/Hr
# 4. Produce a Fire Danger Index According to the conditions : 74.
# 5. Determine Rate of Spread for Fuel Quantities (according to the Fire Hazard Maps)
# 5. Fire intensity can be calcualted using the equation :
#   I = H x R x W
#   I : Intensity in Kw/m
#   H : Heat output in Kj/Kg of fuel
#   W : Weight of the avaibale fuel in kg/m^3
#   R : The Expected Rate of Spread.

# Setting Up H R W
#heatOutput = 18600.0
#veg = Raster("veg2_1")
#weightOfAvailableFuel = Con(((veg == 5) | (veg == 6)), 0.5, Con(veg == 3, 1.5,Con(veg == 1, 1.25,0)))
#rateOfSpread =  Con(((veg == 5) | (veg == 6)), 0.108, Con(veg == 3, 0.328,Con(veg == 1, 1.25,0.583)))
#slope = Raster("dem.tif")
# Calculating NewROS with Noble et al., 1980 Method

#newRateOfSpread = rateOfSpread * Exp(0.0693 * slope)

#Creating Fire Intensity Raster

#fireIntensity = heatOutput * weightOfAvailableFuel * newRateOfSpread
#fireIntensity.save("nstd_fimod")

#Setting Smaller Maximum to Make Data Nicer on Map
#smallerMaximum = Con(fireIntensity > 10000, 10000,fireIntensity)
#smallerMaximum.save("smallmaxfimod")

#Making it Boolean
#boolFireModel = Con(smallerMaximum == 10000, 1,0)
#boolFireModel.save("firemod")


# Flood Model
# Slope Model : Steeper means water can't reach if it does flood "too steep to flood"
# Stream Buffer : How far away you can build from a stream
# Multiplying them together gives a 0 1 value.
# Inverting it gives the correct value

# Finding Streams of Order 5 (Mongolo which is highest risk)

#streamOrder = StreamOrder(Raster("streamnet_3"),Raster("flow_dir2"),"STRAHLER")
#streamOrder.save("stream_o")

#unbufferedMongolo = Con(streamOrder == 5 ,1,0)
#noDataUnbufferedMongolo = SetNull(unbufferedMongolo == 0, 1)
#noDataUnbufferedMongolo.save("ndunbuffmon")

# Expanding the High Risk Stream
#bufferedMongolo = Expand(noDataUnbufferedMongolo,3,1)
floodRisk1 = Con(IsNull(bufferedMongolo),0,1)
floodRisk1.save("floodrisk_1")


# Handling the Other Streams (Using BuffStream)
floodRisk2 = Raster("buffstream")

# Adding 2 and 3 Together

floodRisk3 = Con((floodRisk1 == floodRisk2) & (floodRisk1 ==1),1,floodRisk1 + floodRisk2)
floodRisk3.save("floodrisk_3")



# Creating Slope Component
# Logic : Slopes are greater than 10 degres (too steep to flood) classed as 1
#         Slopes less than or equal to 10 degrees (can flood)

slopeFlood = Con(Raster("slope2") >10, 1,0)
slopeFlood.save("slope_flood")

floodModel = 1 - (Raster("floodrisk_3") * Raster("slope_flood"))
floodModel.save("floodrisk")




