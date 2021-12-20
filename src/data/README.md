# Data Collection

This project is aimed at using artificial intelligence (AI) to improve water supply sustainability in Osun State, Nigeria in particular and Nigeria at large by making information accessible to governements and non-governmental organisations. Such pieces of information include:

 - areas with clean water supply
 - areas that need urgent clean water suppy
 -  areas with non-functional water supply services. (Source: [omdena-osun-nigeria-improving-water-supply](https://docs.google.com/document/d/1rvFft4z4vCDt6wM7Y_EHST0xVkYX4Eqm/edit))
## Data Lineage
The dataset for this project was curated by "the National Bureau of Statistics (NBS), with technical and financial support from UNICEF, African Development Bank (AfDB), and the World Bank" under the auspices of the Federal Ministry of Water Resources of the Federal Republic of Nigeria ([2019-water-sanitation-hygiene-national-outcome-exercise-mapping](https://www.unicef.org/nigeria/reports/water-sanitation-hygiene-national-outcome-routine-mapping-2019)). The dataset is located at [data](https://catalog.waterpointdata.org/datasets/federal-ministry-of-water-resources-nigeria-5efb3667). 

### Data Dictionary
The clean dataframe derived from the dataset has the following features:

- resident_latitude: The latitude of a resident
- resident_longitude: The longitude of a resident
- lat_lon_deg: Longitude and latitude of a water point
- clean_adm1: State where the water point is located
- clean_adm2: Local Government Area where the water point is located
- water_source_original: Original description of water point
- management_clean: Who manages the water point
- water_source_category: The category of water point whether it is a well, spring or others
- longitude: The longitude of the water point
- status_id: This tells whether the water point is functional or not
- water_source: The type of water source, example borehole
- water_tech_clean: The latest technology of the water point
- water_tech: he original technology of the water point
- adm2: Local Government or administration district where the water point is situated
- management: The management of water point, can be government, community or private
- pay: Whether water is free or paid
- status: Whether the water point is functional (and in use) or   non-functional Technical breakdown
- subjective_quality: The quality of the water 
- water_point_location: The place where the water is located
- latitude: Latitude of the water point
- distance_in_km: Distance between a resident in need of water and the water point. 
​
### Code Usage:
The `etl.py` script inside `task-1-data-collection` folder can be run as follows inside the `task-1-data-collection` directory:

`python etl.py Water_Point_Data_Exchange__WPDx-Basic_.csv Osun water-point.db`.

This happens when the dataset is inside the `task-1-data-collection`. 

