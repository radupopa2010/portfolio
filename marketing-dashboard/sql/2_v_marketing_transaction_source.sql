 SELECT a.*,
        c.*
   FROM v_marketing_response_source a
     JOIN ( SELECT sample_table_1.sample_col_1,
            sample_table_1.mres_type,
            max(sample_table_1.mres_datetime) AS mres_datetime,
            sample_table_1.mres_companyid,
            sample_table_3.oppo_primarycompanyid,
            sample_table_3.oppo_sample_table_3id
           FROM sample_table_1
             JOIN sample_table_3 ON sample_table_1.mres_companyid::text = sample_table_3.oppo_primarycompanyid::text AND sample_table_3.oppo_createddate::date > sample_table_1.mres_datetime::date
          GROUP BY sample_table_1.sample_col_1, sample_table_1.mres_companyid, sample_table_1.mres_type, sample_table_3.oppo_primarycompanyid, sample_table_3.oppo_sample_table_3id) b ON date(a.mres_datetime) = date(b.mres_datetime) AND a.mres_companyid::text = b.mres_companyid::text
     JOIN sample_table_3 c ON b.oppo_sample_table_3id::text = c.oppo_sample_table_3id::text
  ORDER BY a.sample_col_1;