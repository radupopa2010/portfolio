#!/usr/bin/python3


# Redirect the output to a log file
#import sys
#sys.stdout = open("c:\\lastRun.log", "w")
#
import pg8000
import time, datetime, sys
startTime = time.time()
# Connection to Postgres
pg8000.paramstyle = 'qmark'
dbc = pg8000.connect(
	user="otherUser"
	, password="otherPassword"
	, host="marketing-vm"
	, port=5432
	, database="marketing"
)
dbc.autocommit = True	
db = dbc.cursor()
startTime = time.time()
# Get a list of available files
import os
CONF_DATAPATH = os.path.abspath('../../data/insite-attempts/pending')
move_path = os.path.abspath('../../data/insite-attempts/processed')
lsDataFiles = [l for l in os.listdir(CONF_DATAPATH) if l.endswith('.db')]
print(len(lsDataFiles),lsDataFiles)
import sqlite3
import csv
# db.execute(''' 
			# -- empty mark_attempts
			# DELETE FROM mark_attempts
			# ''')
# Define a move fuction to use later, after processing each db file
import shutil
import uuid
def move(src, dest):
	try:
		shutil.move(src, dest)
	except:
		dest = '%s_%s' % (dest, uuid.uuid4())
		shutil.move(src, dest)
	
	#
	
#

# Loop over the available attempt databases
for dbFileName in lsDataFiles:
	# Handel possible db errors
	try:
		dbFilePath = CONF_DATAPATH + "/" + dbFileName
		dbDonePath = move_path + "/" + dbFileName
		csvTempPath = CONF_DATAPATH + "/temp_%s.csv" % (uuid.uuid4(), )
		conn = sqlite3.connect(dbFilePath)
		print(time.ctime(),"Working with: ", dbFileName)
		sys.stdout.flush(
		cur = conn.cursor()
		# Select all data from the database
		cur.execute("""
			select
				comp_companyid as matt_companyid
				, txDate as matt_datetime
				, txFaxResult as matt_outcome
			from txlog join impcontacts on txFaxNum = faxnum
		""")
		# Dump the result to a result CSV file
		outputFile = open(csvTempPath, 'w', newline='')
		outputWriter = csv.writer(outputFile, delimiter='\t')
		outputWriter.writerows(cur)
		outputFile.close()
		
		# Import result file into the mark_attempts table
		print(time.ctime(),"Importing into mark_attepts")
		sys.stdout.flush(
		#	- Create a temporary table
		db.execute('''
			CREATE TABLE temp_table (
				temp_companyid varchar(255),
				temp_datetime varchar(255),
				temp_outcome varchar(255)
			);
		''')
		#	- Import data to the temporary table
		db.execute('''	
			COPY temp_table 
			FROM '%s' 
			DELIMITER '\t' CSV;
		''' % (csvTempPath, ))
		#	- Migrate the data from the temporary table to the destination
		db.execute('''
			INSERT INTO mark_attempts
				(matt_companyid, matt_datetime, matt_outcome)
			SELECT
				temp_companyid as matt_companyid
				, NULLIF(NULLIF(temp_datetime, ''), 'None')::timestamp as matt_datetime
				, temp_outcome as matt_outcome
			FROM temp_table
		''')
		#	- Cleanup the temporary table
		db.execute('''
			DROP TABLE temp_table
		''')
		#	- Save the results
		dbc.commit()
		#	- Mark the file as processed
		#   - Delete de CSV file
		move(dbFilePath, dbDonePath)
		print(time.ctime(),"... Complete!")
		sys.stdout.flush()
	except Exception as e:
		print(time.ctime(),"Database issue! file=", dbFileName, "error=", e)
		os.rename(CONF_DATAPATH +'/' + dbFileName,
			 CONF_DATAPATH+'/' + dbFileName + '_Exception')

		
	#

print(time.ctime(),'Total run time', time.time()- startTime)
# Delete the CSV files
print(time.ctime(),'Deleting the CSV files')
lsDeleteFiles = [l for l in os.listdir(CONF_DATAPATH) if l.endswith('.csv')]
for eaFile in lsDeleteFiles:
	os.remove(CONF_DATAPATH +'/'+ eaFile)

# UPDATE the existing companyid with the one that was merged to
# For each row in the source file, run an update query
print(time.ctime(),'Updatating the existing companyid with the one that was merged to')
import time
sratUpCompId = time.time()
import os
basePath = os.path.abspath('../../data/crm-tables')
sourceFile = open(basePath + '/' + 'comp_mergings')
limit = 0
for eaRow in sourceFile:
	comg_mergefrom, comg_mergeto, junk = eaRow.split('\t')
	db.execute(''' 
			update mark_attempts
			set matt_companyid = '%s'
			where matt_companyid = '%s'
			''' %(comg_mergefrom, comg_mergeto))
print(time.ctime(),'Rows affected: '+ str(db.rowcount))
print(time.ctime(),'Query ran for:' + str(time.time()- sratUpCompId))

# Delete the duplicate rows
print(time.ctime(),'Deleting duplicates now')
startDeleteDup = time.time()
db.execute(''' 
DELETE FROM mark_attempts 
WHERE matt_attemptid IN (
	SELECT matt_attemptid
	FROM (
		SELECT matt_attemptid,
			ROW_NUMBER() OVER (partition BY matt_companyid, 
			matt_datetime, 
			matt_outcome 
		ORDER BY matt_attemptid) AS rnum
		FROM mark_attempts
	) t
	WHERE t.rnum > 1
);''')
dbc.commit()

print(time.ctime(),'Delete duplicate query run for:', time.time()- startDeleteDup)
# Delete all the records that have no datetime
print(time.ctime(),'Deleting rows that have no datetime')
db.execute("""  delete from mark_attempts where matt_datetime is null  """)
dbc.commit()

# Convert matt_datetime to timestamp
try:
	db.execute(''' 
				ALTER TABLE mark_attempts 
				ALTER COLUMN matt_datetime TYPE timestamp
				USING to_timestamp(matt_datetime, 'YYYY-MM-DD');
				''')
	dbc.commit()
	dbc.close()
except Exception as e:
	print(time.ctime(),'INGORE THIS ERROR', e)

print(time.ctime(),'Done!!!')
sys.stdout.flush()