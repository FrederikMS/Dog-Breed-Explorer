{{ config(materialized="table") }}
with source_data as (select * from bronze.dog_api_raw)

select
    source_data.*,
    case
        when
            instr(weight.imperial, '-') - 1 > 0
            and length(regexp_substr(weight.imperial, '[a-zA-Z]')) > 0
        then 0
        when instr(weight.imperial, '-') - 1 > 0
        then
            cast(substr(weight.imperial, 1, instr(weight.imperial, '-') - 1) as decimal)
        when instr(weight.imperial, '–') - 1 > 0
        then
            cast(substr(weight.imperial, 1, instr(weight.imperial, '–') - 1) as decimal)
        when weight.metric = 'NaN'
        then null
        else cast(weight.imperial as decimal)
    end as weight_imperial_lower,
    case
        when instr(weight.imperial, '-') - 1 > 0
        then
            cast(
                substr(
                    weight.imperial, instr(weight.imperial, '-', -1, 1) + 1
                ) as decimal
            )
        when instr(weight.imperial, '–') - 1 > 0
        then
            cast(
                substr(
                    weight.imperial, instr(weight.imperial, '–', -1, 1) + 1
                ) as decimal
            )
        when weight.metric = 'NaN'
        then null
        else cast(weight.imperial as decimal)
    end as weight_imperial_upper,
    case
        when
            instr(weight.metric, '-') - 1 > 0
            and length(regexp_substr(weight.metric, '[a-zA-Z]')) > 0
        then 0
        when instr(weight.metric, '-') - 1 > 0
        then cast(substr(weight.metric, 1, instr(weight.metric, '-') - 1) as decimal)
        when instr(weight.metric, '–') - 1 > 0
        then cast(substr(weight.metric, 1, instr(weight.metric, '–') - 1) as decimal)
        when weight.metric = 'NaN'
        then null
        else cast(weight.metric as decimal)
    end as weight_metric_lower,
    case
        when instr(weight.metric, '-') - 1 > 0
        then
            cast(substr(weight.metric, instr(weight.metric, '-', -1, 1) + 1) as decimal)
        when instr(weight.metric, '–') - 1 > 0
        then
            cast(substr(weight.metric, instr(weight.metric, '–', -1, 1) + 1) as decimal)
        when weight.metric = 'NaN'
        then null
        else cast(weight.metric as decimal)
    end as weight_metric_upper
from source_data
