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
# Tool Name: Add Total Volume Fields to VRI file geodatabase table
# Source Name: AddTotVolFieldsToVRI.py
# Version: ArcGIS 10.3.1, Python 2.7.8
# Author:  British Columbia Ministry of Forests and Range
#          Coast Forest Region Geomatic Services
#
# Required Arguments: input table (VRI having VEG_COMP(2009) field names)
#
# Description: This tool adds fields to a VRI table for tabulating
#              volume (m3) by species group in polygon
#              at the primary utilization level (17.5 cm dbh.)
#              The AddVphFieldToVRI script must be run first.
# Created: August 22, 2009
#
# Modification History
#    2009.08.24 - corrected to run with 9.3-version Geoprocessor
#    2014.09.06 - updated to run with arcpy ESRI ArcGIS 10.3, updated
#                 to work with updated VRI schema
#
# ------------------------------------------------------------------------
"""

import arcpy
import sys

# Get required input table
inputVRI = sys.argv[1]
arcpy.AddMessage('The input data set is: ' + inputVRI)

# Add fields to input table
arcpy.AddMessage('Adding volume tabulation fields to VRI table... ')
lstNewFields = ["Alder", "Aspen", "Balsam", "Birch", "Cedar", "CtWood", "Cypress",
                "Fir", "Hemlock", "Larch", "Maple", "Pine", "Spruce", "Unknown",
                "Hectares", "M3_175"]
for idField in lstNewFields:
    if not arcpy.ListFields(inputVRI, idField):
        arcpy.AddField_management(inputVRI, idField, "DOUBLE", 8, "", "", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddMessage('    ' + idField + ' added')
    else:
        arcpy.AddMessage('    ' + idField + ' exists - skipping')

# Create featurelayer for this script from the input featureclass
inputLayer = 'inputFeatureLayer'
arcpy.AddMessage('Creating ' + inputLayer + ' ...'),
arcpy.MakeFeatureLayer_management(inputVRI, inputLayer)
arcpy.AddMessage(' Done!')

# Set defaults for new fields
arcpy.AddMessage('Setting defaults for volume tabulation fields in VRI table... ')
for idField in lstNewFields:
    arcpy.CalculateField_management(inputLayer, idField, 0, "VB")
    arcpy.AddMessage('    defaults for ' + idField + ' field set')

# Populate new fields
arcpy.AddMessage('Populating volume tabulation fields in VRI table... ')
uc = arcpy.UpdateCursor(inputVRI)
uc.reset()
row = uc.next()
i = 1
while row:
    Ha = row.getValue('GEOMETRY_Area') / 10000
    DR = row.getValue('dr_vph175')  # Alder
    if DR is None:
        DR = 0
    AT = row.getValue('at_vph175')  # Aspen
    if AT is None:
        AT = 0
    B = row.getValue('b_vph175')  # Balsam
    if B is None:
        B = 0
    BA = row.getValue('ba_vph175')
    if BA is None:
        BA = 0
    BG = row.getValue('bg_vph175')
    if BG is None:
        BG = 0
    BL = row.getValue('bl_vph175')
    if BL is None:
        BL = 0
    EP = row.getValue('ep_vph175')  # Birch
    if EP is None:
        EP = 0
    CW = row.getValue('cw_vph175')  # Cedar
    if CW is None:
        CW = 0
    AC = row.getValue('ac_vph175')  # CtWood
    if AC is None:
        AC = 0
    YC = row.getValue('yc_vph175')  # Cypress
    if YC is None:
        YC = 0
    FD = row.getValue('fd_vph175')  # Fir
    if FD is None:
        FD = 0
    H = row.getValue('h_vph175')  # Hemlock
    if H is None:
        H = 0
    HW = row.getValue('hw_vph175')
    if HW is None:
        HW = 0
    HM = row.getValue('hm_vph175')
    if HM is None:
        HM = 0
    LA = row.getValue('la_vph175')  # Larch
    if LA is None:
        LA = 0
    MB = row.getValue('mb_vph175')  # Maple
    if MB is None:
        MB = 0
    PA = row.getValue('pa_vph175')  # Pine
    if PA is None:
        PA = 0
    PF = row.getValue('pf_vph175')
    if PF is None:
        PF = 0
    PL = row.getValue('pl_vph175')
    if PL is None:
        PL = 0
    PLI = row.getValue('pli_vph175')
    if PLI is None:
        PLI = 0
    PW = row.getValue('pw_vph175')
    if PW is None:
        PW = 0
    PY = row.getValue('py_vph175')
    if PY is None:
        PY = 0
    S = row.getValue('s_vph175')  # Spruce
    if S is None:
        S = 0
    SE = row.getValue('se_vph175')
    if SE is None:
        SE = 0
    SS = row.getValue('ss_vph175')
    if SS is None:
        SS = 0
    SW = row.getValue('sw_vph175')
    if SW is None:
        SW = 0
    VPH = row.getValue('vph175')
    if VPH is None:
        VPH = 0
    TOT = (DR + AT + B + BA + BG + BL + EP + CW + YC + AC + FD + H + HM + HW + LA + MB +
           PA + PF + PL + PLI + PW + PY + S + SE + SS + SW)
    XZ = round((VPH - TOT), 0)  # Unknown or other speces
    row.setValue('Alder', DR * Ha)
    row.setValue('Aspen', AT * Ha)
    row.setValue('Balsam', (B + BA + BG + BL) * Ha)
    row.setValue('Birch', EP * Ha)
    row.setValue('Cedar', CW * Ha)
    row.setValue('CtWood', AC * Ha)
    row.setValue('Cypress', YC * Ha)
    row.setValue('Fir', FD * Ha)
    row.setValue('Hemlock', (H + HM + HW) * Ha)
    row.setValue('Larch', LA * Ha)
    row.setValue('Maple', MB * Ha)
    row.setValue('Pine', (PA + PF + PL + PLI + PW + PY) * Ha)
    row.setValue('Spruce', (S + SE + SS + SW) * Ha)
    row.setValue('Unknown', XZ * Ha)
    row.setValue('Hectares', Ha)
    row.setValue('M3_175', TOT * Ha)
    uc.updateRow(row)
    row = uc.next()
    i += 1
arcpy.AddMessage('    ' + str(i) + ' rows updated!')
del uc  # release table
del row
arcpy.AddMessage('------------------------------------------------------------')
