 SELECT a.*,
        c.*
   FROM v_marketing_response_source a
     JOIN ( SELECT mark_responses.mres_responseid,
            mark_responses.mres_type,
            max(mark_responses.mres_datetime) AS mres_datetime,
            mark_responses.mres_companyid,
            opportunity.oppo_primarycompanyid,
            opportunity.oppo_opportunityid
           FROM mark_responses
             JOIN opportunity ON mark_responses.mres_companyid::text = opportunity.oppo_primarycompanyid::text AND opportunity.oppo_createddate::date > mark_responses.mres_datetime::date
          GROUP BY mark_responses.mres_responseid, mark_responses.mres_companyid, mark_responses.mres_type, opportunity.oppo_primarycompanyid, opportunity.oppo_opportunityid) b ON date(a.mres_datetime) = date(b.mres_datetime) AND a.mres_companyid::text = b.mres_companyid::text
     JOIN opportunity c ON b.oppo_opportunityid::text = c.oppo_opportunityid::text
  ORDER BY a.mres_responseid;