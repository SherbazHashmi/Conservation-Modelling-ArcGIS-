#-------------------------------------------------------------------------------
# Name:        Building Model
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

slopeCost = 1 / Raster("slope2")
slopeCostStandardised = (slopeCost / (slopeCost.maximum)   )
slopeCostStandardised.save("slopeCost2")

# Distance Cost =  1 / EuDistnace AggTracksRoads

arcpy.env.extent = Raster("dem.tif").extent
#Combining Road and Track Rasters with Buffers
arcpy.PolylineToRaster_conversion("Minor_roads.shp","FID","minorroadsr","MAXIMUM_COMBINED_LENGTH","NONE",30)
arcpy.PolylineToRaster_conversion("Highway.shp","FID","highwayr","MAXIMUM_COMBINED_LENGTH","NONE",30)

highways = Con(IsNull("highwayr"),0,1)
highways.save("highway")
minorroadsr = Con(IsNull("minorroadsr"),0,1)
minorroadsr.save("minroads")

aggTrackRoad = Raster("roadgrid2") + Raster("highway") + Raster("minroads")

aggTrackRoad.save("finalroads")

# Final Roads Conversion
reclassRoads = Reclassify("finalroads","Value",RemapValue([[0,0],[1,1],[2,1]]))
reclassRoads.save("roadsv2")

# Nullify Roads

nullRoads= SetNull(reclassRoads == 0,1)
nullRoads.save("roadsv3")

#EuDistance

euDistanceTrackRoad = EucDistance(Raster("roadsv3"), cell_size = 30)
euDistanceTrackRoad.save("euctrackroad")


#Standardise EuDistance with FuzzyStreamBufferEquation

fuzzTrackRoad = Con(Raster("euctrackroad") <= 30, 0, Con(Raster("euctrackroad") >= 300, 1, (Raster("euctrackroad") - 30.0) / (300.0 - 30.0)))
fuzzTrackRoad.save("fuzzroad")

#Inverse of FuzzTrackRoad

distanceCost = 1 -  Raster("fuzzroad")
distanceCost.save("distanceCost")

# Merging Costs each with 0.5 weighting

cost = (slopeCostStandardised * 0.5) + (Raster("distanceCost") * 0.5)
cost.save("cost2")

# Value

# Logic : The Higher Up There will Be Better Views (Hence More Value)
# Note : Need to standardise from 0-1

dem = Raster("dem.tif")
minimum = dem.minimum
maximum = dem.maximum
elevationValue = (dem - minimum) / (maximum - minimum)
elevationValue.save("viewValue")

#Aspect Model : Solar Passive Housing
# Aspect Gives you Which Way it is Facing
# Assuming North is 180 - 270 then wecan use reclassification to see how well
# the aspect is.
# Group that with the Trees in the Are which coukld potentially block the sun
# from coming in


aspect = Aspect("dem.tif")
aspect.save("aspect")

#Standardised Raster

newRaster = Con(((aspect >= 90) & (aspect <= 270)),1,0)
newRaster.save("solarpassive2")


value = (newRaster * 0.5)+ (Raster("viewValue") * 0.5)
value.save("value")

buildingModel = (Raster("value") * 0.5) + (Raster("cost2") * 0.5)
buildingModel.save("buildmodel3")


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
#     ................Weight..............ROS............
#    |3|DS2 Dry    |       1.5       |      0.467        .
#    |1|Pine       |     0.5 - 1.5   |       0.583       .
#    |2|Urban      |     1           |          1        .
#    |4|B  Ground  |      0          |       0           .
#    |5|M Grassland|     0.5         |       0.108       .
#    |6|D Grassland|       1         |        0.200      .
#    |7|Woodland  |        1.5       |         0.583     .
#    |8|Water     |         0        |      0            .
#
#

#http://www.nrcresearchpress.com/doi/pdf/10.1139/b82-048

# Setting Up H R W

heatOutput = 18600.0
veg = Raster("veg2_1")
weightOfAvailableFuelInt = Reclassify(Raster("veg2_1"),"VALUE",RemapValue([[1,10],[2,10],[3,15],[4,0],[5,5],[6,10],[7,15],[8,0]]))
weightOfAvailableFuel = weightOfAvailableFuelInt / 10;
rateOfSpreadInt = Reclassify(Raster("veg2_1"),"VALUE",RemapValue([[1,583],[2,1000],[3,486],[4,0],[5,108],[6,200],[7,583],[8,0]]))
rateOfSpread = rateOfSpreadInt / 1000
slope = Raster("dem.tif")

#Calculating NewROS with Noble et al., 1980 Method


newRateOfSpread = rateOfSpread * Exp(0.0693 * slope)

#Creating Fire Intensity Raster

fireIntensity = heatOutput * weightOfAvailableFuel * newRateOfSpread
fireIntensity.save("nstd_fimod")

#Setting Smaller Maximum to Make Data Nicer on Map
smallerMaximum = Con(fireIntensity > 10000, 10000,fireIntensity)
smallerMaximum.save("smallmaxfimod")

#Making it Boolean
boolFireModel = Con(smallerMaximum == 10000, 1,0)
boolFireModel.save("firemod")


# Flood Model
# Slope Model : Steeper means water can't reach if it does flood "too steep to flood"
# Stream Buffer : How far away you can build from a stream
# Multiplying them together gives a 0 1 value.
# Inverting it gives the correct value

# Finding Streams of Order 5 (Mongolo which is highest risk)

streamOrder = StreamOrder(Raster("streamnet_3"),Raster("flow_dir2"),"STRAHLER")
#streamOrder.save("streamo")


#Handling Order 5
unbufferedFive = Con(streamOrder == 5 ,1,0)
noDataUnbufferedFive = SetNull(unbufferedFive == 0, 1)
bufferedFive = Expand(noDataUnbufferedFive,3,1)
floodRisk1Five = Con(IsNull(bufferedFive),0,1)

#Handling Order 6
unbufferedSix = Con(streamOrder == 6 ,1,0)
noDataUnbufferedSix = SetNull(unbufferedSix == 0, 1)
bufferedSix = Expand(noDataUnbufferedSix,3,1)
floodRisk1Six = Con(IsNull(bufferedSix),0,1)

#Handling Order 7
unbufferedSeven = Con(streamOrder == 7 ,1,0)
noDataUnbufferedSeven = SetNull(unbufferedSeven == 0, 1)
bufferedSeven = Expand(noDataUnbufferedSeven,3,1)
floodRisk1Seven = Con(IsNull(bufferedSeven),0,1)

floodRiskFinal = floodRisk1Five + floodRisk1Six + floodRisk1Seven
floodRiskFinal.save("floodriskag_1")



# Handling the Other Streams (Using BuffStream)
floodRisk2 = Raster("buffstream")

# Adding 2 and 3 Together

floodRisk3 = Con((floodRiskFinal == 0) & (floodRisk2 == 0),0,1)
floodRisk3.save("floodrisk_3")



# Creating Slope Component
# Logic : Slopes are greater than 10 degres (too steep to flood) classed as 1
#         Slopes less than or equal to 10 degrees (can flood)

slopeFlood = Con(Raster("slope2") >10, 0,1)
slopeFlood.save("slope_flood")

floodModel = 1 - (Raster("floodrisk_3") * Raster("slope_flood"))
floodModel.save("finalflood")


constrainedBuildingModel = Raster("finalflood") * Raster("firemod") * Raster("eros-bool-2") * Raster("buildmodel3")
constrainedBuildingModel.save("conbModel")

