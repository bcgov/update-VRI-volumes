"""
Copyright 2011-16 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# -------------------------------------------------------------------------
# Tool Name: Add VPH Fields to VRI file geodatabase table
# Source Name: AddVPH_FieldsToVRI.py
# Version: ArcGIS 10.3.1, Python 2.7.8
# Author:  British Columbia Ministry of Forests and Range
#          Coast Forest Region Geomatic Services
#
# Required Arguments: input table (VRI having VEG_COMP(2009) field names)
#
# Description: This tool adds fields to a VRI table for tabulating
#              volume per hectare by species and by volume per hectare
#              at the primary utilization level (17.5 cm dbh.)
# Created: August 20, 2009
#
# Modification History
#    2009.08.21 - renamed fields to better identify content,
#                 dropped fields dependent on geometry [GEOMETRY_Area]
#    2009.08.24 - corrected to run with 9.3-version Geoprocessor
#    2014.09.06 - updated to run with arcpy ESRI ArcGIS 10.3, updated
#                 to work with updated VRI schema
# ------------------------------------------------------------------------
"""

import arcpy
import sys

# Get required input table
inputVRI = sys.argv[1]
arcpy.AddMessage('The input data set is: ' + inputVRI)

# Add fields to input table
arcpy.AddMessage('Adding volume tabulation fields to VRI table... ')
lstNewFields = ["ac_vph1git75", "at_vph175", "b_vph175", "ba_vph175", "bg_vph175",
                "bl_vph175", "cw_vph175", "dr_vph175", "ep_vph175", "fd_vph175",
                "h_vph175", "hm_vph175", "hw_vph175", "la_vph175", "mb_vph175",
                "pa_vph175", "pf_vph175", "pl_vph175", "pli_vph175",
                "pw_vph175", "py_vph175", "s_vph175", "se_vph175", "ss_vph175",
                "sw_vph175", "yc_vph175", "vph175"]
for idField in lstNewFields:
    # arcpy.AddMessage('    adding ' + idField + ' field...'),
    if not arcpy.ListFields(inputVRI, idField):
        arcpy.AddField_management(inputVRI, idField, "DOUBLE", 8, "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.AddMessage('    ' + idField + ' added')
    else:
        arcpy.AddMessage('    ' + idField + ' exists - skipping')

# Create featurelayer for this script from the input featureclass
inputLayer = 'inputFeatureLayer'
arcpy.AddMessage('Creating ' + inputLayer + ' ...'),
arcpy.MakeFeatureLayer_management(inputVRI, inputLayer)
arcpy.AddMessage('Done!')

# Set defaults for new fields
arcpy.AddMessage('Setting defaults for volume tabulation fields in VRI table... ')
for idField in lstNewFields:
    arcpy.CalculateField_management(inputLayer, idField, 0, "VB")
    arcpy.AddMessage('    defaults for ' + idField + ' field set')

# Populate new fields
arcpy.AddMessage('Populating volume tabulation fields in VRI table... ')

# Calculate volume per hectare at the 17.5 cm dbh utilization level and populate vph175 field
uc = arcpy.UpdateCursor(inputVRI)
uc.reset()
row = uc.next()
i = 1
while row:
    totalvol = 0
    vol = row.getValue('live_vol_per_ha_spp1_175')
    if vol is None:
        vol = 0
    totalvol += vol
    vol = row.getValue('live_vol_per_ha_spp2_175')
    if vol is None:
        vol = 0
    totalvol += vol
    vol = row.getValue('live_vol_per_ha_spp3_175')
    if vol is None:
        vol = 0
    totalvol += vol
    vol = row.getValue('live_vol_per_ha_spp4_175')
    if vol is None:
        vol = 0
    totalvol += vol
    vol = row.getValue('live_vol_per_ha_spp5_175')
    if vol is None:
        vol = 0
    totalvol += vol
    vol = row.getValue('live_vol_per_ha_spp6_175')
    if vol is None:
        vol = 0
    totalvol += vol
    row.setValue('vph175', totalvol)
    uc.updateRow(row)
    row = uc.next()
    i += 1
arcpy.AddMessage('    vph175 field updated. ' + str(i) + ' rows updated!')
del uc  # release table
del row

# select each species then populate its vph field
lstSpeciesOrder = [6, 5, 4, 3, 2, 1]  # do each species code field in the record

# cottonwood
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'AC%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[0], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[0] + ' field updated ')

# aspen
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'AT%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[1], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[1] + ' field updated ')

# balsam genus, species not identified
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'B\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[2], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[2] + ' field updated ')

# balsam - amabilis fir
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'BA\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[3], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[3] + ' field updated ')

# balsam - grand fir
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'BG\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[4], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[4] + ' field updated ')

# balsam - subalpine fir
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'BL\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[5], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[5] + ' field updated ')

# cedar - western redcedar
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'C%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[6], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[6] + ' field updated ')

# red alder 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'D%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[7], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[7] + ' field updated ')

# birch - all native (paper, water, Alaska paper, Alaska x paper)
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'E%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[8], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[8] + ' field updated ')

# Douglas-fir
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'F%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[9], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[9] + ' field updated ')

# hemlock genus, species not identified
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'H\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[10], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[10] + ' field updated ')

# hemlock - mountain hemlock 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'HM\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[11], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[11] + ' field updated ')

# hemlock - western hemlock 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'HW\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[12], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[12] + ' field updated ')

# larch - all native species (alpine, tamarack, western) 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'L%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[13], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[13] + ' field updated ')

# maple - all native species (big leaf or vine)
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'M%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[14], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[14] + ' field updated ')

# pine - whitebark pine 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PA\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[15], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[15] + ' field updated ')

# pine - limber pine
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PF\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[16], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[16] + ' field updated ')

# pine - lodgepole pine
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PL\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[17], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[17] + ' field updated ')

# pine - interior lodgepole pine 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PLI\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[18], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[18] + ' field updated ')

# pine - western white pine
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PW\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[19], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[19] + ' field updated ')

# pine - ponderosa pine
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'PY\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[20], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[20] + ' field updated ')

# spruce genus
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'S\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[21], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[21] + ' field updated ')

# spruce - Engelmann spruce 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'SE\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[22], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[22] + ' field updated ')

# spruce - Sitka spruce 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'SS\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[23], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[23] + ' field updated ')

# spruce - white spruce 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" = \'SW\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[24], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[24] + ' field updated ')

# cypress - yellow-cedar 
for i in lstSpeciesOrder:
    query = "\"SPECIES_CD_" + str(i) + "\" LIKE \'Y%\'"
    exprfield = "[live_vol_per_ha_spp" + str(i) + "_175]"
    arcpy.SelectLayerByAttribute_management(inputLayer, "NEW_SELECTION", query)
    arcpy.CalculateField_management(inputLayer, lstNewFields[25], exprfield, "VB")
arcpy.AddMessage('    ' + lstNewFields[25] + ' field updated ')

arcpy.AddMessage('------------------------------------------------------------')
