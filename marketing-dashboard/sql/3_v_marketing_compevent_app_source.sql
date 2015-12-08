 SELECT a.*,
    c.*
   FROM ( SELECT max(sample_tabe_1.sample_col_1) AS sample_col_1,
            sample_table_2.sample_col_3,
            sample_table_2.coev_companyid
           FROM sample_tabe_1
             JOIN sample_table_2 ON sample_tabe_1.mres_companyid::text = sample_table_2.coev_companyid::text AND sample_table_2.sample_col_3::timestamp without time zone > sample_tabe_1.sample_col_1 AND sample_tabe_1.mres_type::text = 'lead'::text AND (sample_table_2.coev_newstatus::text = 'applicationin'::text OR sample_table_2.coev_newstatus::text = 'qual-pos'::text OR sample_table_2.coev_newstatus::text = 'qual-neg'::text OR sample_table_2.coev_newstatus::text = 'creditpending'::text)
          GROUP BY sample_table_2.sample_col_3, sample_table_2.coev_companyid) b
     JOIN sample_table_2 c ON c.sample_col_3::text = b.sample_col_3::text AND c.coev_companyid::text = b.coev_companyid::text
     JOIN v_marketing_response_source a ON date(a.sample_col_1) = date(b.sample_col_1) AND a.mres_companyid::text = b.coev_companyid::text
  ORDER BY a.matt_datetime, c.sample_col_3;