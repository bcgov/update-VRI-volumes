# Update VRI Volumes

## Usage
Add the VRI_Tools.tbx toolbox to ArcToolBox to run these scripts. Each tool takes one argument - a featureclass that contains standard VRI formatted species fields.

NOTE: Must run AddVphFieldstoVRI first.

## Script Descriptions
**AddVphFieldstoVRI.py script**

This tool adds fields to a VRI table for tabulating volume per hectare by species and calculates volume per hectare at the primary utilization level (17.5 cm dbh.)

Notes: 
* Adds new fields to an existing standard VRI table / feature class.
* Calculates new fields with m3/ha for each species in the polygon.
* This cript only needs to be run once for the feature class

**AddTotVolFieldsToVRI.py script**

This tool adds fields to a VRI table for tabulating volume (m3) by species group in polygon at the primary utilization level (17.5 cm dbh.)

Notes:
* Run this script after adding the m3/ha field with the first script
* The script should be run after completion of geoprocessing operations as the volumes are calculated for each polygon based on area
* The table can then be summarized using the named species volume fields

## Requirements
Requires ESRI ArcInfo licensing & ArcMap 10.0+.

## Getting Help or Reporting an Issue
Use the Issues tab to get help or report any issues.

## License

    Copyright 2015-2016 Province of British Columbia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at 

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
