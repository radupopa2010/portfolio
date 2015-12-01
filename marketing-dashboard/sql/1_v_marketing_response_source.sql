SELECT a.*,
	   c.*
   FROM mark_attempts a
     JOIN ( SELECT mark_responses.mres_responseid,
            mark_responses.mres_type,
            max(date(mark_attempts.matt_datetime)) AS matt_datetime,
            mark_attempts.matt_companyid
           FROM mark_attempts
             JOIN mark_responses ON mark_attempts.matt_companyid::text = mark_responses.mres_companyid::text AND date(mark_responses.mres_datetime) > date(mark_attempts.matt_datetime)
          GROUP BY mark_responses.mres_responseid, mark_attempts.matt_companyid, mark_responses.mres_type) b ON date(a.matt_datetime) = b.matt_datetime AND a.matt_companyid::text = b.matt_companyid::text
     JOIN mark_responses c ON b.mres_responseid = c.mres_responseid
  ORDER BY a.matt_attemptid;