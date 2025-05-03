with source_data as (select * from {{ ref("type_cast_age") }})

select trim(temperament_value) as temperament, breed_group
from source_data, unnest(split(temperament, ',')) as temperament_value
where temperament like '%Friend%'
