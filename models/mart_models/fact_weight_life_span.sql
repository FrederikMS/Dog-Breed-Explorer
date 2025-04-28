with source_data as (select * from {{ ref("type_cast_age") }})

select
    life_span_lower,
    life_span_upper,
    count(weight_imperial_lower) as number_of_counts,
    min(weight_imperial_lower) as weight_imperial_lower_min,
    avg(weight_imperial_lower) as weight_imperial_lower_avg,
    max(weight_imperial_lower) as weight_imperial_lower_max,
    min(weight_imperial_upper) as weight_imperial_upper_min,
    avg(weight_imperial_upper) as weight_imperial_upper_avg,
    max(weight_imperial_upper) as weight_imperial_upper_max,
    min(weight_metric_lower) as weight_metric_lower_min,
    avg(weight_metric_lower) as weight_metric_lower_avg,
    max(weight_metric_lower) as weight_metric_lower_max,
    min(weight_metric_upper) as weight_metric_upper_min,
    avg(weight_metric_upper) as weight_metric_upper_avg,
    max(weight_metric_upper) as weight_metric_upper_max,
    min(height_imperial_lower) as height_imperial_lower_min,
    avg(height_imperial_lower) as height_imperial_lower_avg,
    max(height_imperial_lower) as height_imperial_lower_max,
    min(height_imperial_upper) as height_imperial_upper_min,
    avg(height_imperial_upper) as height_imperial_upper_avg,
    max(height_imperial_upper) as height_imperial_upper_max,
    min(height_metric_lower) as height_metric_lower_min,
    avg(height_metric_lower) as height_metric_lower_avg,
    max(height_metric_lower) as height_metric_lower_max,
    min(height_metric_upper) as height_metric_upper_min,
    avg(height_metric_upper) as height_metric_upper_avg,
    max(height_metric_upper) as height_metric_upper_max
from source_data
group by life_span_lower, life_span_upper
order by number_of_counts desc
