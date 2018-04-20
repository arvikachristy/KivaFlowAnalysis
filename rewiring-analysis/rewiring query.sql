###############################################################################
# Rewiring SQL Query
# -----------------------------------------------------------------------------
# This file lists all of the query that we used in the PSQL database in conducting
# rewiring analysis.
###############################################################################

#Step 1: Filter for loans sector
SELECT 
lenders_country,
loans_sector,
count(loans_sector) as weight
FROM test_flows_notnull
group by loans_sector, lenders_country
order by lenders_country, loans_sector;

#Step 2: Create another table to filter sum of all sector in one country (flow/weight to sector existance)
create table test_temp as SELECT
    sectorcount.lenders_country,
    sum(sectorcount.weight) as total_sec
    FROM 
        (SELECT 
        lenders_country,
        loans_sector,
        count(loans_sector) as weight
        FROM test_flows_notnull
        group by loans_sector, lenders_country
        order by lenders_country, loans_sector) as sectorcount 
    group by sectorcount.lenders_country

#Step 3: join 1 and 2 to be connected to python
SELECT
subtable.lenders_country,
subtable.loans_sector,
subtable.weight as sector_flow,
ori.total_sec
FROM
    (SELECT 
    lenders_country,
    loans_sector,
    count(loans_sector) as weight
    FROM test_flows_notnull
    group by loans_sector, lenders_country
    order by lenders_country, loans_sector) as subtable
JOIN test_temp as ori ON ori.lenders_country = subtable.lenders_country


################################################################################################
#Other rewiring query to construct the rewiring analysis
################################################################################################

#Append original language
CREATE TABLE flows_full_data_notnull AS 
SELECT 
flows_data_notnull.*,
original_language
FROM flows_data_notnull INNER JOIN loans_data on flows_data_notnull.loans_id = loans_data.id
limit 100;

\COPY usa_rewiring_data FROM 'C:/Users/User/name-gender-dict.csv' WITH (FORMAT csv);
ALTER TABLE country_weight_flow ADD COLUMN lenders_population TEXT DEFAULT NULL;

create table copy_table as select * from country_weight 
    
DELETE FROM geo_distance WHERE kmdist='kmdist';

UPDATE country_weight_flow AS t1
SET lenders_population = p.popu_rate
FROM population AS p
WHERE t1.from = p.country_code

--Display Backward and forward flow by creating a copy_temp table
SELECT 
    country_weight_flow.country_from,
     country_weight_flow.country_to,
     country_weight_flow.flow_country_count as forward_count,
     copy_temp.flow_country_count as backward_count,     
     country_weight_flow.kmdist,
     country_weight_flow.lenders_population,
     country_weight_flow.loans_population
FROM
    copy_temp, country_weight_flow
WHERE
    country_weight_flow.country_from = copy_temp.country_to AND country_weight_flow.country_to = copy_temp.country_from


INSERT INTO test_backward test_backward test_backward(country)

select 
A.lenders_name,
B.gender as lender_gender,
A.borrowers_genders
from usa_rewiring_data A
left join usa_gender_dict B
on LOWER(A.lenders_name) = LOWER(B.name)












