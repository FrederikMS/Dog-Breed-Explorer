with source_data as (select * from {{ ref("type_cast_age") }})

select
    breed_group,
    count(*) as number_of_counts,
    min(height_imperial_lower) as height_imperial_min,
    max(height_imperial_upper) as height_imperial_max,
    min(height_metric_lower) as height_metric_min,
    max(height_metric_upper) as height_metric_max,
    min(weight_imperial_lower) as weight_imperial_min,
    max(weight_imperial_upper) as weight_imperial_max,
    min(weight_metric_lower) as weight_metric_min,
    max(weight_metric_upper) as weight_metric_max,
    min(life_span_lower) life_span_min,
    max(life_span_upper) life_span_max
from source_data
group by breed_group
order by number_of_counts desc
