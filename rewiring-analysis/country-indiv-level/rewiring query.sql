#rewiring query

#Append ori language
CREATE TABLE flows_full_data_notnull AS 
SELECT 
flows_data_notnull.*,
original_language
FROM flows_data_notnull INNER JOIN loans_data on flows_data_notnull.loans_id = loans_data.id
limit 100;

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

#Step 3: join 1 and 2 put in python
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


---------------------------------------------------------------------
SELECT 


















