# Flow Analysis on Kiva, The Online Microlending Platform
### Technology Requirements:
- Python 3
- MATLAB
- PSQL
- PgAdmin (*Optional)
- iPython and Miniconda (*Optional)
- Gephi Software: [Download Link](https://gephi.org/users/download/) (*Optional)
### File Structure:
There exist three data analysis in this repository. Each represented in three different folders listed below:
##### gravity-model 
- This code was written in MATLAB.
- Contains country-to-country analysis using gravity model. 
- Main gravity model can be found in `gravModel.m`.
- Correlation calculation can be found in `correlationScript.m`.
- We listed the SQL Queries that we used to build the PSQL database in `gravity_query.sql`.
##### topological-analysis
- This code was written in Python.
- Contains country-to-country analysis using Bonferroni Validation Procedure (BVP).
- Procedure can be found in `bonferroni.py`.
- We listed the SQL Queries that we used to build the PSQL database in `topological_query.sql` (note that some of the query were used from gravity model).
- We also included Gephi files that we used to visualise the flow in world map.
##### rewiring-analysis
- This code was written in Python.
- Contains country-to-individual(macro) and individual-to-individual(micro) analysis using rewiring analysis.
- This file contains two more folders: `country-to-individual` and `individual-to-individual`.
- The main procedure for macro analysis was written in individual files for each categories. Each can be found in `[category]-rewiring.py`.
- The main procedure for micro analysis can be found in `main-gender-rewiring.py`.
- All files are accompanied with the SQL Queries that we used to build the PSQL database with.
