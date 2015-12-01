 SELECT a.*,
    c.*
   FROM ( SELECT max(mark_responses.mres_datetime) AS mres_datetime,
            comp_events.coev_timestamp,
            comp_events.coev_companyid
           FROM mark_responses
             JOIN comp_events ON mark_responses.mres_companyid::text = comp_events.coev_companyid::text AND comp_events.coev_timestamp::timestamp without time zone > mark_responses.mres_datetime AND mark_responses.mres_type::text = 'lead'::text AND (comp_events.coev_newstatus::text = 'applicationin'::text OR comp_events.coev_newstatus::text = 'qual-pos'::text OR comp_events.coev_newstatus::text = 'qual-neg'::text OR comp_events.coev_newstatus::text = 'creditpending'::text)
          GROUP BY comp_events.coev_timestamp, comp_events.coev_companyid) b
     JOIN comp_events c ON c.coev_timestamp::text = b.coev_timestamp::text AND c.coev_companyid::text = b.coev_companyid::text
     JOIN v_marketing_response_source a ON date(a.mres_datetime) = date(b.mres_datetime) AND a.mres_companyid::text = b.coev_companyid::text
  ORDER BY a.matt_datetime, c.coev_timestamp;