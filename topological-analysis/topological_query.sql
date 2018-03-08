#######bonferroni Query

#1 Add Nl and Nr data to the table
create table test_data_gb_au as SELECT 
* FROM test_data_gbau S
INNER JOIN (
    SELECT 
    country_from as dupli1,
    sum(cast(flow as int)) as n_l
    from flows_data_notnull
    GROUP BY country_from
) C ON S.country_from = dupli1
INNER JOIN (
    SELECT 
    country_to as dupli2,
    sum(cast(flow as int)) as n_r
    from flows_data_notnull
    GROUP BY country_to
) X ON S.country_to = dupli2
ORDER BY country_from, country_to

#2 delete dupli from console 
#3 