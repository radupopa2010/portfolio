#!/usr/bin/python3


# Redirect the output to a log file
# import sys
# sys.stdout = open("c:\\lastRun.log", "w")
#
"""
objective:
	load crm table data into the marketing database
"""
import os, sys, time
CONF_INPATH = os.path.abspath('../../data/crm-tables/pending/')
move_path = os.path.abspath('../../data/crm-tables/processed/')
CONF_TABLES = (
#	('crm-table-name', 'crm-column-names')
 	('company', 'comp_companyid, comp_name, comp_primaryuserid ,comp_nextcalldate, comp_status,comp_duns')
 ,	('comp_events', 'coev_companyid, coev_timestamp, coev_oldstatus, coev_newstatus')
 ,	('person', 'pers_personid, pers_emailaddress, pers_companyid')
 ,	('phone', 'phon_phoneid, phon_fullnumber, phon_companyid, phon_type')
 ,	('opportunity', 'oppo_opportunityid, oppo_primarycompanyid, oppo_createddate, \
		oppo_fund_expDate, oppo_fund_expCommission, oppo_status, oppo_assigneduserid, \
		oppo_doc_totalamt_withtax, oppo_approval_lender, oppo_customlendername \
		')
 ,	('users', 'user_userid, user_firstname, user_lastname')
 # ,	('dnb_results', 'dres_datetime, dres_companyid, dres_html, dres_json')
 ,
)

# Define a move fuction to use later, after processing each db file
import shutil
def move(src, dest):
    shutil.move(src, dest)

# Move the comp_mergings file to processed/
lsDataFiles = [l for l in os.listdir(CONF_INPATH)]
for xfile in lsDataFiles:
	if xfile == 'comp_mergings':
		move(CONF_INPATH + '/' + xfile, move_path + "/" + xfile)
#

def main():
	import pg8000
	import pdb
	pg8000.paramstyle = 'qmark'
	dbc = pg8000.connect(
		user="someUser"
		, password="somePassword"
		, host="marketing-vm"
		, port=5432
		, database="marketing"
	)
	dbc.autocommit = True	
	db = dbc.cursor()
	
	for eaTable in CONF_TABLES:
		try:	
			eaTblName, eaTblCols = eaTable
			print(time.ctime()," \n Processing table", eaTblName, eaTblCols)
			sys.stdout.flush()
			eaTblSrc = ''.join([CONF_INPATH, '/', eaTblName])
			eaTblMove = ''.join([move_path ,'/' ,eaTblName])
			print(time.ctime(),"  - source path: ", eaTblSrc)
			sys.stdout.flush()
			# First check if the "pending" folder has data to consume
			if not lsDataFiles:
				print(time.ctime(),'No files in "pending" folder, program will exit()')
				exit()
			db.execute('delete from %s;' % (eaTblName ))
			db.execute("\
				COPY %s \
				FROM '%s' \
				DELIMITER '\t' \
				NULL 'None' \
				CSV; \
			" % (eaTblName, eaTblSrc))
			dbc.commit()
			print(time.ctime(),"  - done (%s rows) !" % (db.rowcount, ))
			move(eaTblSrc,eaTblMove)  
		except Exception as e:
			print("Error found: ",e)
			continue
	#
	print(time.ctime(),'Removing extra spaces from opportunity table')
	sys.stdout.flush()
	db.execute(''' 
	update opportunity set
	oppo_status = rtrim(oppo_status)
	, "oppo_fund_expDate" = rtrim("oppo_fund_expDate")
	''')
	print(time.ctime(),"Complete!")
	sys.stdout.flush()
	#
	print(time.ctime(),'Removing extra spaces from users table')
	db.execute(''' 
	update users 
	set user_lastname = rtrim(user_lastname)
	''')
	print(time.ctime(),"Complete!")
	sys.stdout.flush()
	dbc.commit()
	print(time.ctime(),'Removing extra spaces from company table')
	db.execute(''' 
	update company 
	set comp_status = rtrim(comp_status)
	''')
	print(time.ctime(),"Complete!")
	sys.stdout.flush()
	dbc.commit()
	# Update values COLUMN "oppo_fund_expCommission" from "opportunity" TABLE
	# string 'None' to string '0'
	try:
		print(time.ctime(),'Updating COLUMN oppo_fund_expCommission values from "None" to "0"')
		db.execute(''' 
					UPDATE opportunity 
					SET oppo_fund_expCommission = '0'
					WHERE oppo_fund_expCommission = 'None'
					''')
		dbc.commit()
	except Exception as e:
		#print(time.ctime(),'IGNORE THIS ERROR IF APPEARS', e)
		pass
	# Convert COLUMN "oppo_fund_expCommission" from "opportunity" TABLE
	# "character varying" to "numeric"
	try:
		print(time.ctime(),'Converting COLUMN oppo_fund_expCommission from \
		"character varying" to "numeric"')
		db.execute(''' 
					ALTER TABLE opportunity 
					ALTER COLUMN oppo_fund_expCommission TYPE numeric
					USING to_number(oppo_fund_expCommission,'0000000.00');
					''')
		dbc.commit()
		print(time.ctime(),"Complete!")
		sys.stdout.flush()

	except Exception as e:
		#print(time.ctime(),'IGNORE THIS ERROR IF APPEARS', e)
		pass
	
	dbc.close()
#

if __name__ == '__main__':
	main()
#
