 SELECT b.matt_companyid,
    b.matt_datetime,
    b.mres_companyid,
    b.mres_type,
    b.comp_companyid,
    b.comp_primaryuserid,
    users.user_userid,
    users.user_firstname,
    users.user_lastname
   FROM users
     JOIN ( SELECT a.matt_companyid,
            date(a.matt_datetime) AS matt_datetime,
            a.mres_companyid,
            a.mres_type,
            company.comp_companyid,
            company.comp_primaryuserid
           FROM v_marketing_response_source a
             JOIN company ON a.mres_companyid::text = company.comp_companyid::text
          WHERE a.mres_type::text = 'lead'::text
          GROUP BY a.matt_companyid, date(a.matt_datetime), a.mres_companyid, a.mres_type, company.comp_companyid, company.comp_primaryuserid
          ORDER BY date(a.matt_datetime)) b ON users.user_userid::text = b.comp_primaryuserid::text;