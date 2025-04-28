with source_data as (select * from {{ ref("type_cast_height") }})

select
    *,
    case
        when instr(life_span, '-') - 1 > 0
        then cast(substr(life_span, 1, instr(life_span, '-') - 1) as integer)
        when instr(life_span, '–') - 1 > 0
        then cast(substr(life_span, 1, instr(life_span, '–') - 1) as integer)
        when instr(life_span, '–') - 1 < 0 and instr(life_span, '-') - 1 < 0
        then cast(regexp_substr(life_span, '^[0-9]*') as integer)
        else null
    end as life_span_lower,
    /* using regex to extract last numer*/
    array_reverse(regexp_extract_all(life_span, r'\d+'))[offset(0)] as life_span_upper
from source_data
