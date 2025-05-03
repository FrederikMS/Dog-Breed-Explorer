select count(*) as row_count from {{ ref("type_cast_age") }} having row_count != 172
