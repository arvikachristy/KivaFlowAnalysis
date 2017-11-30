/*relationship between three tables*/

SELECT 
lenders_data.id as lenders_id,
loans_data.id as loans_id
FROM loans_data INNER JOIN relationship_data ON loans_data.id = relationship_data.loan_id INNER JOIN lenders_data ON lenders_data.id = relationship_data.lender_ids
limit 10

/*split by comma to rationalise to 1nf*/
CREATE TABLE relationship_1nf AS
    SELECT
        loan_id, 
        regexp_split_to_table(lender_ids, E',')
    FROM relationship_data

/*combine everything into one table*/
CREATE TABLE flows_data AS
    SELECT 
    lenders_data.id as lenders_id,
    lenders_data.name as lenders_name,
    lenders_data.city as lenders_city,
    lenders_data.state as lenders_state,
    lenders_data.country_code as lenders_country,
    lenders_data.occupation as lenders_occupation,
    lenders_data.loan_count as lenders_loan_count,
    lenders_data.invited_by as lenders_invited_by,
    loans_data.id as loans_id,
    loans_data.name as loans_name,
    loans_data.loan_amount as loans_loan_amount,
    loans_data.funded_amount as funded_amount,
    loans_data.status as status,
    loans_data.country_code as loans_country_code,
    loans_data.country_name as loans_country_name,
    loans_data.town as loans_town,
    loans_data.currency as loans_currency,
    loans_data.sector as loans_sector,
    loans_data.partner_id as partner_id,    
    loans_data.posted_time as posted_time,
    loans_data.disbursed_time as disbursed_time,
    loans_data.funded_time as funded_time,
    loans_data.lender_count as lender_count,
    loans_data.borrowers_names as borrowers_names,
    loans_data.borrowers_genders as borrowers_genders,
    loans_data.repayment_interval as repayment_interval
    FROM loans_data INNER JOIN relationship_1nf ON loans_data.id = relationship_1nf.loan_id INNER JOIN lenders_data ON lenders_data.id = relationship_1nf.lender_ids    

/*update a user details for their missing countries*/
UPDATE flows_data
SET lenders_country = 'US'
WHERE lenders_id='gooddogg1'    

/*checker for above*/
SELECT * 
FROM flows_data
WHERE country_code = 'GB'
limit 10

/*Select flow from country to countries*/
SELECT 
	DISTINCT lenders_country,
    loans_country_name,
    count(loans_country_name) as counter
FROM flows_data 
WHERE lenders_country = 'GB'
GROUP BY lenders_country, loans_country_name
ORDER BY lenders_country, loans_country_name
limit 250;

/*checker for above*/
SELECT 
	lenders_country,
    loans_country_name,
    borrowers_names 
FROM flows_data 
WHERE lenders_country = 'GB' AND loans_country_name='Bulgaria'
limit 250;

SELECT 
COUNT(*)
FROM lenders_data LEFT JOIN flows_data ON flows_data.lenders_id = lenders_data.id
WHERE (loan_count IS NOT NULL AND NOT loan_count= '0' )AND flows_data IS NULL

SELECT count(lenders_data.id)
FROM lenders_data 
LEFT JOIN relationship_1nf ON lenders_data.id = relationship_1nf.lender_ids
WHERE relationship_1nf.lender_ids IS NULL

SELECT 
geo_dist.from,
geo_dist.to,
geo_dist.kmdist
FROM 
    flows_data LEFT JOIN geo_dist ON flows_data.lenders_country = geo_dist.from
    LEFT JOIN geo_dist ON flows_data.loans_country_code = geo_dist.to

SELECT 
geo_distance.from,
geo_distance.to,
geo_distance.kmdist
FROM 
    flows_data, geo_distance
WHERE
    flows_data.lenders_country = geo_distance.from AND flows_data.loans_country_code = geo_distance.to