with source_data as (select * from {{ ref("type_cast_weight") }})

select
    source_data.*,
    case
        when
            instr(height.imperial, '-') - 1 > 0
            and length(regexp_substr(height.imperial, '[a-zA-Z]')) > 0
        then 0
        when instr(height.imperial, '-') - 1 > 0
        then
            cast(substr(height.imperial, 1, instr(height.imperial, '-') - 1) as decimal)
        when instr(height.imperial, '–') - 1 > 0
        then
            cast(substr(height.imperial, 1, instr(height.imperial, '–') - 1) as decimal)
        when height.metric = 'NaN'
        then null
        else cast(height.imperial as decimal)
    end as height_imperial_lower,
    case
        when instr(height.imperial, '-') - 1 > 0
        then
            cast(
                substr(
                    height.imperial, instr(height.imperial, '-', -1, 1) + 1
                ) as decimal
            )
        when instr(height.imperial, '–') - 1 > 0
        then
            cast(
                substr(
                    height.imperial, instr(height.imperial, '–', -1, 1) + 1
                ) as decimal
            )
        when height.metric = 'NaN'
        then null
        else cast(height.imperial as decimal)
    end as height_imperial_upper,
    case
        when
            instr(height.metric, '-') - 1 > 0
            and length(regexp_substr(height.metric, '[a-zA-Z]')) > 0
        then 0
        when instr(height.metric, '-') - 1 > 0
        then cast(substr(height.metric, 1, instr(height.metric, '-') - 1) as decimal)
        when instr(height.metric, '–') - 1 > 0
        then cast(substr(height.metric, 1, instr(height.metric, '–') - 1) as decimal)
        when height.metric = 'NaN'
        then null
        else cast(height.metric as decimal)
    end as height_metric_lower,
    case
        when instr(height.metric, '-') - 1 > 0
        then
            cast(substr(height.metric, instr(height.metric, '-', -1, 1) + 1) as decimal)
        when instr(height.metric, '–') - 1 > 0
        then
            cast(substr(height.metric, instr(height.metric, '–', -1, 1) + 1) as decimal)
        when height.metric = 'NaN'
        then null
        else cast(height.metric as decimal)
    end as height_metric_upper
from source_data
