SELECT b.matt_date,
    users.user_firstname,
    b.appcount
   FROM ( SELECT a.matt_date,
            company.comp_primaryuserid,
            count(a.coev_companyid) AS appcount
           FROM ( SELECT DISTINCT date(v_marketing_compevent_app_source.matt_datetime) AS matt_date,
                    v_marketing_compevent_app_source.coev_companyid
                   FROM v_marketing_compevent_app_source) a
             JOIN company ON company.comp_companyid::text = a.coev_companyid::text
          GROUP BY a.matt_date, company.comp_primaryuserid) b
     JOIN users ON users.user_userid::text = b.comp_primaryuserid::text
  ORDER BY b.matt_date;