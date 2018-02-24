select 
A.lenders_name,
B.gender as lender_gender,
A.borrowers_genders
from usa_rewiring_data A
left join usa_gender_dict B
on LOWER(A.lenders_name) = LOWER(B.name)

