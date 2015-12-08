#!/usr/bin/python3
import pprint, time
# Connect to Mongo DB
import pymongo
mongo = pymongo.MongoClient('localhost', 3001)
mongodb = mongo.meteor
mdata = mongodb.markdata

# Connect to Postgresql DB
import pg8000
dbc = pg8000.connect(user="", password="", 
                     host="", port=5432, database = '')
db = dbc.cursor()

# Make a list of dictionaries with the marketing days with 
# "_id", "mark_attempted" and "money_spent"

#     get a list of marketing days from Postgresql
print(time.ctime(),'Obtaining data from Postgres with  "_id", "mark_attempted" and "money_spent" ')
db.execute(''' 
                SELECT date(sample_col_1)::text as _id, 
                        count(sample_col_2)::integer as mark_attempted
                FROM mark_attempts
                GROUP BY date(sample_col_1)
                ORDER BY date(sample_col_1) ASC
            ''')
rawMarkDays = db.fetchall()

#    transform the list obtained from Postgresql to a list of dictionaries
markDays = []
estimateCost = 0.02
for eaDate in rawMarkDays:
    if eaDate[0] is None: continue
    markDays += [{
                    '_id':eaDate[0],
                    'mark_attempted': eaDate[1],
                    'money_spent': int(eaDate[1] * estimateCost)
                     }]
# print('sample markDays: ')
# pprint.pprint(markDays[0:5])    
             
# Obtain values for 'mark_success'
#   get a list from Postgresql with '_id' and 'mark_success'
print(time.ctime(),'Obtaining data from Postgres with "_id" and "mark_success" ')
db.execute(''' 
            SELECT date(sample_col_1)::text as _id, 
                   count(sample_col_2)::integer as mark_success
            FROM mark_attempts
            WHERE matt_outcome = 'OK'
            GROUP BY date(sample_col_1)
            ORDER BY date(sample_col_1) ASC
           ''')
rawMarkDays = db.fetchall()
  
#    transform the list obtained from Postgresql to a list of dictionaries
tempList = []
for eaDate in rawMarkDays:
    tempList += [{
                    '_id': eaDate[0],
                    'mark_success': eaDate[1]
                }]

#   Merge the 2 lists based on '_id'
'''
def JoinLists(lonto, lfrom):
    lresult = []
    for eaRowFrom in lfrom:
        for eaRowTo in lonto:
            if eaRowTo['_id'] == eaRowFrom['_id']:
                for eaKeyFrom in eaRowFrom:
                    eaRowTo[eaKeyFrom] = eaRowFrom[eaKeyFrom]         
                    lresult += [eaRowTo]
    return lresult
'''
def JoinLists(lonto, lfrom):
	lresult = []
	for eaRowFrom in lfrom:
		for eaRowTo in lonto:
			if eaRowTo['_id'] == eaRowFrom['_id']:
				for eaKeyFrom in eaRowFrom:
					if eaKeyFrom == 'users' and 'users' in eaRowTo:
						for eaUserName in eaRowFrom['users']:
							if not eaUserName in eaRowTo['users']:
								eaRowTo['users'][eaUserName] = eaRowFrom['users'][eaUserName]
								continue
							for eaUserDataKey in eaRowFrom['users'][eaUserName]:
								eaRowTo['users'][eaUserName][eaUserDataKey] = eaRowFrom['users'][eaUserName][eaUserDataKey]
						continue
					eaRowTo[eaKeyFrom] = eaRowFrom[eaKeyFrom]
				#
				lresult += [eaRowTo]
				continue
	#
	
	return lresult

JoinLists(markDays,tempList)

# Obtain values for 'mark_leads'
#   get a list from Postgresql with '_id' and 'mark_leads'

print(time.ctime(),'Obtaining data from Postgres with "_id" and "mark_leads" ')
db.execute(''' 
            SELECT  date(sample_col_1)::text as _id, 
                    count(mres_companyid)::integer as mark_leads
            FROM v_marketing_response_source
            WHERE mres_type = 'lead'
            GROUP BY date(sample_col_1)
            ORDER BY date(sample_col_1) ASC
           ''')
rawMarkDays = db.fetchall()
#    transform the list obtained from Postgresql to a list of dictionaries
tempList = []
for eaDate in rawMarkDays:
    tempList += [{
                    '_id': eaDate[0],
                    'mark_leads': eaDate[1]
                }]

JoinLists(markDays,tempList)


# Obtain values for 'mark_removes'
#   get a list from Postgresql with '_id' and 'mark_removes'

print(time.ctime(),'Obtaining data from Postgres with "_id" and "mark_removes" ')
db.execute(''' 
            SELECT  date(sample_col_1)::text as _id, 
                    count(mres_responseid)::integer as mark_removes
            FROM v_marketing_response_source
            WHERE mres_type = 'remove' 
            OR    mres_type = 'reremove' 
            GROUP BY date(sample_col_1)
            ORDER BY date(sample_col_1) ASC
           ''')
rawMarkDays = db.fetchall()
#    transform the list obtained from Postgresql to a list of dictionaries
tempList = []
for eaDate in rawMarkDays:
    if eaDate[1] is None: eaDate[1] = 0
    tempList += [{
                    '_id': eaDate[0],
                    'mark_removes': eaDate[1]
                }]

JoinLists(markDays,tempList)


# print('\n\nStarting Data (join lead data): ')
# pprint.pprint(markDays[0:2])  


#	"leads-given"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": leads_given ')

db.execute('''
			SELECT date(sample_col_1)::text AS sample_col_1, user_firstname,
			count(user_userid)::integer AS leads_given
			FROM v_mongo_user_leads
			GROUP BY sample_col_1, user_firstname
			ORDER BY sample_col_1 ASC			
			''')
qresult = db.fetchall()


# print('\n\nUser Leads Given Database Results: ')
# pprint.pprint(qresult[0:2])  



#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in qresult:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'leads_given':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'leads_given':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  

#	"leads-apps-produced"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": leads_apps_produced ')

db.execute('''
			SELECT b.matt_date::text,
			users.user_firstname,
			b.appcount::integer
		   FROM ( SELECT a.matt_date,
					company.comp_primaryuserid,
					count(a.coev_companyid) AS appcount
				   FROM ( SELECT DISTINCT date(v_marketing_compevent_app_source.sample_col_1) AS matt_date,
							v_marketing_compevent_app_source.coev_companyid
						   FROM v_marketing_compevent_app_source) a
					 JOIN company ON company.comp_companyid::text = a.coev_companyid::text
				  GROUP BY a.matt_date, company.comp_primaryuserid) b
			 JOIN users ON users.user_userid::text = b.comp_primaryuserid::text
		  ORDER BY b.matt_date;			
			''')
apps_produced_result = db.fetchall()


# print('\n\nUser leads-apps-produced Database Results: ')
# pprint.pprint(apps_produced_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in apps_produced_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'leads_apps_produced':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'leads_apps_produced':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  


#	"leads-stalled"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": leads_stalled ')

db.execute('''
			select matt_date::text, user_firstname, stallcount::integer
			from (
				-- Join company data onto 'stalled' marketing attempt leads
				select matt_date, comp_primaryuserid, count(matt_companyid)::integer as stallcount
				from (
					-- Unique groups of 'lead' marketing responses by attempt date/company
					--	where the response has a condition to be qualified as 'stalledlead'
					select distinct date(sample_col_1) as matt_date, matt_companyid
					from v_marketing_response_source as vmrs_outer
					join company on comp_companyid = matt_companyid
					where mres_type = 'lead' AND (
						-- company has been stalled
						comp_status = 'stalledlead'
						-- company has no callback scheduled soon
						OR comp_nextcalldate is null
						--OR comp_nextcalldate > current_timestamp + interval '10' days
					)
					-- A future 'lead' marketing response for the same company
					AND mres_ishotlead = true
				) as foo
				join company on comp_companyid = matt_companyid
				where not exists(
					-- A transaction associated to this marketing attempt
					select sample_col_2 from v_marketing_transaction_source as vmts
					where vmts.sample_col_1 = foo.matt_date
						and vmts.matt_companyid = foo.matt_companyid
				)
				group by matt_date, comp_primaryuserid
			) bar
			join users on user_userid = comp_primaryuserid
			order by matt_date
			''')
leads_stalled_result = db.fetchall()

# print('\n\nUser leads-stalled Database Results: ')
# pprint.pprint(leads_stalled_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in leads_stalled_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'leads_stalled':int(eaRow[2])}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'leads_stalled':int(eaRow[2])} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  


#	"transactions-created"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": transactions_created ')

db.execute('''
		select date(vmts_distinct.sample_col_1)::text as sample_col_1, user_firstname, count(*)::integer
		from (
			select distinct
				sample_col_1, oppo_opportunityid, oppo_primarycompanyid
			from v_marketing_transaction_source
		) as vmts_distinct
		join v_mongo_companyid_to_user_firstname as vmctuf
			on vmts_distinct.oppo_primarycompanyid = vmctuf.comp_companyid
		group by date(vmts_distinct.sample_col_1), user_firstname
		order by sample_col_1
			''')
transactions_created_result = db.fetchall()

# print('\n\nUser transactions-created Database Results: ')
# pprint.pprint(transactions_created_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in transactions_created_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'transactions_created':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'transactions_created':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  


#	"transactions-funded" and "transactions-margin"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": transactions_funded and transactions_margin ')

db.execute('''
			select date(vmts_distinct.sample_col_1)::text as sample_col_1, user_firstname, 
					count(*)::integer, sum("oppo_fund_expCommission")::integer
			from (
				select distinct
					sample_col_1, oppo_opportunityid, 
					oppo_primarycompanyid, "oppo_fund_expCommission"
				from v_marketing_transaction_source
				where "oppo_fund_expCommission" is not null 
				and "oppo_fund_expCommission" != 0
			) as vmts_distinct
			join v_mongo_companyid_to_user_firstname as vmctuf
				on vmts_distinct.oppo_primarycompanyid = vmctuf.comp_companyid
			group by date(vmts_distinct.sample_col_1), user_firstname
			order by sample_col_1
			''')
transactions_funded_margin_result = db.fetchall()

# print('\n\nUser "transactions-funded" and "transactions-margin" Database Results: ')
# pprint.pprint(transactions_funded_margin_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in transactions_funded_margin_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'transactions_funded':eaRow[2],
											'transactions_margin':eaRow[3]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'transactions_funded':eaRow[2],
											  'transactions_margin':eaRow[3]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  


#	"transactions-pending"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": transactions_pending ')

db.execute('''
			select date(vmts_distinct.sample_col_1)::text as sample_col_1, user_firstname, count(*)::integer
			from (
				select distinct
					sample_col_1, oppo_opportunityid, oppo_primarycompanyid
				from v_marketing_transaction_source
				where oppo_status != 'stalled' 
				and oppo_status != 'declined' 
				and(
					"oppo_fund_expCommission" is null 
					or "oppo_fund_expCommission" = 0
					)
			) as vmts_distinct
			join v_mongo_companyid_to_user_firstname as vmctuf
				on vmts_distinct.oppo_primarycompanyid = vmctuf.comp_companyid
			group by date(vmts_distinct.sample_col_1), user_firstname
			order by sample_col_1
			''')
transactions_pending_result = db.fetchall()

# print('\n\nUser transactions-pending Database Results: ')
# pprint.pprint(transactions_pending_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in transactions_pending_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'transactions_pending':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'transactions_pending':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  


#	"transactions-stalled"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": transactions_stalled ')

db.execute('''
			select date(vmts_distinct.sample_col_1)::text as sample_col_1, user_firstname, count(*)::integer
			from (
				select distinct
					sample_col_1, oppo_opportunityid, oppo_primarycompanyid
				from v_marketing_transaction_source
				where oppo_status = 'stalled'
			) as vmts_distinct
			join v_mongo_companyid_to_user_firstname as vmctuf
				on vmts_distinct.oppo_primarycompanyid = vmctuf.comp_companyid
			group by date(vmts_distinct.sample_col_1), user_firstname
			order by sample_col_1
			''')
transactions_stalled_result = db.fetchall()

# print('\n\nUser transactions-stalled Database Results: ')
# pprint.pprint(transactions_stalled_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in transactions_stalled_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'transactions_stalled':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'transactions_stalled':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  

#	"transactions-ucompanies"	Query Postgres for results for each key if user in "users"
print(time.ctime(),'Obtaining data from Postgres with "_id" and "users": transactions_ucompanies , \
		\n that will be used for computing leads-stalled ' )

db.execute('''
			select date(vmts_distinct.sample_col_1)::text as sample_col_1, user_firstname, count(*)::integer
			from (
				select distinct
					sample_col_1, oppo_primarycompanyid
				from v_marketing_transaction_source
			) as vmts_distinct
			join v_mongo_companyid_to_user_firstname as vmctuf
				on vmts_distinct.oppo_primarycompanyid = vmctuf.comp_companyid
			group by date(vmts_distinct.sample_col_1), user_firstname
			order by sample_col_1
			''')
transactions_ucompanies_result = db.fetchall()

# print('\n\nUser transactions_ucompanies_result Database Results: ')
# pprint.pprint(transactions_ucompanies_result[0:2])  

#	transform the list obtained from Postgresql to a list of dictionaries
tempList = []

previousDay = ''
for eaRow in transactions_ucompanies_result:
	currentDay = eaRow[0]
	tempList += [{
					'_id': eaRow[0],
					'users':{str(eaRow[1]):{'transactions_ucompanies':eaRow[2]}}
				}]
	previusDict = eaRow
	if currentDay == previousDay:
		for i in tempList:
			if i['_id'] == currentDay:
				i['users'][str(eaRow[1])] = {'transactions_ucompanies':eaRow[2]} 
	previousDay = eaRow[0]
		

# print('\n\nTransformed Above Data: ')
# pprint.pprint(tempList[0:2])  

#   Merge the 2 lists based on '_id'
JoinLists(markDays,tempList)

# print('\n\nMerged Data: ')
# pprint.pprint(markDays[0:2])  

# ###########################################################################

# Empty the MongoDb 
print(time.ctime(),'Emptying the MongoDb')
mdata.remove({})
# Insert data into MongoDB
print(time.ctime(),'Inserting into Mongo')
mdata.insert_many(markDays)

print(time.ctime(),'.....Done!!!')

# Testing code
#mdata.insert({'_id':'2015-01-02'})
#mdata.delete_many({})
# strftime('%Y-%m-%d'),

# db.stickynotes.remove({})
# // remove all documents in the "stickynotes" collection
