SELECT a.*,
	   c.*
   FROM sample_table_1 a
     JOIN ( SELECT sample_table_2.mres_responseid,
            sample_table_2.mres_type,
            max(date(sample_table_1.matt_datetime)) AS matt_datetime,
            sample_table_1.matt_companyid
           FROM sample_table_1
             JOIN sample_table_2 ON sample_table_1.matt_companyid::text = sample_table_2.mres_companyid::text AND date(sample_table_2.mres_datetime) > date(sample_table_1.matt_datetime)
          GROUP BY sample_table_2.mres_responseid, sample_table_1.matt_companyid, sample_table_2.mres_type) b ON date(a.matt_datetime) = b.matt_datetime AND a.matt_companyid::text = b.matt_companyid::text
     JOIN sample_table_2 c ON b.mres_responseid = c.mres_responseid
  ORDER BY a.matt_attemptid;