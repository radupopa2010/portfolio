 SELECT company.comp_companyid,
    company.comp_primaryuserid,
    users.user_firstname
   FROM company
     JOIN users ON users.user_userid::text = company.comp_primaryuserid::text;