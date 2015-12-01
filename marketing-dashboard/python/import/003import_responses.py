#!/usr/bin/python3

"""

(v.02; 18 May 2015; rbutler, gpopa)

objective:

capturing detail from lead processing logs
 ->    number of positive/negative leads per day
 ->	feed these details into marketing-db

 """

import os, re, pprint, sys, time
startExecTime = time.time()
# PATH_BASE = r'\\crmserver\gpopa\log-parse\logs'+'\\'
# Run from markening-vm

# Define a move fuction to use later, after processing each log file
import shutil,uuid
def move(src, dest):
	try:
		shutil.move(src, dest)
	except:
		dest = '%s_%s' % (dest, uuid.uuid4())
		shutil.move(src, dest)
		
PATH_BASE = os.path.abspath('../../data/insite-responses/pending')
move_path =  os.path.abspath('../../data/insite-responses/processed')
startLog = time.time()
# create a dictionary with exceptions
countErrors = {'no-company': 0, 'no-type': 0}
# create a dictionary with emails
countPasses = {'lead': [], 'remove': [], 'emremove': [], 'reremove': []}
# read each log file in the folder, line by line
lstAllFiles = [l for l in os.listdir(PATH_BASE) if l.endswith('.log')]
print(time.ctime(),'start parsing the log files:', time.ctime())
sys.stdout.flush()
for eaFile in lstAllFiles:
	eaFilepath = PATH_BASE +'/'+ eaFile
	try:
		fh = open(eaFilepath, 'r')
	except Exception as e:
		print(time.ctime(),"Could not open file!", eaFilepath, e)
		sys.stdout.flush()
		continue
	#
	try:
		while True:
			eaLine = fh.readline().lower()
			if eaLine == '':
				eaLine = fh.readline()
				if eaLine == '':
					# print(time.ctime(),"EOF:", eaFile)
					break
				#
			#
			# when text "processing message" is found it means it is the starting of a new email
			try:
				if eaLine.index('processing message:') < 10:
					continue
				#
				# keep reading
			except:
				continue
			#
			seeklen = 0
			seekfound = False
			seektype = ""
			seekcomp = ""
			seeklog = ""
			seekdate = eaFile[-14:-4]
			seekdate = '%s-%s-%s' % (seekdate[-4:], seekdate[3:5], seekdate[0:2])
			while not seekfound:
				seekline = fh.readline().lower()
				seeklen += len(seekline)
				seeklog += seekline
				# if it reaches the end of file, it stops
				if seekline == '':
					# print(time.ctime(),"End of Seek")
					break
				#
				# keep searching until it it finds again "processing message"
				try:
					#
					if seekline.index('processing message:') > 0:
						# print(time.ctime(),"End of Seek")
						break
					#
				except:
					pass
				#
				try:
					if seekline.index('processing as') > 0 and seekline.index('lead') > 0:
						seektype = "lead"
					#
				except:
					pass
				#
				try:
					if seekline.index('lead@taycor.com') > 0:
						seektype = "lead"
					#
				except:
					pass
				#
				try:
					if seekline.index('leohanger99') > 0:
						seektype = "lead"
					#
				except:
					pass
				#
				try:
					if seekline.index('remolax20') > 0:
						seektype = "remove"
					#
				except:
					pass
				try:
					if seekline.index('remove@taycor') > 0:
						seektype = "remove"
					#
				except:
					pass
				#
				try:
					if seekline.index('processing as') > 0 and seekline.index('remove') > 0:
						seektype = "remove"
					#
				except:
					pass
				#
				try:
					if seekline.index('removed 1 person email addresses') > 0:
						seektype = "emremove"
					#
				except:
					pass
				#
				try:
					if (not seekcomp) and (seekline.index('email-people (1): ') > 0):
						seekcompChk = re.sub(r'\(1\)', '', seekline)
						seekcompChk = re.sub('[^0-9]', '', seekcompChk[-16:])
						if seekcompChk:
							seekcomp = "pers="+seekcompChk
						#
					#
				except:
					pass
				#
				try:
					if (not seekcomp) and (seekline.index('email-/home/desktop/Marketing/python_codepeople (2): ') > 0):
						seekcompChk = re.sub(r'\(2\)', '', seekline)
						seekcompChk = re.sub('[^0-9],', '', seekcompChk[-16:])
						seekcompChk = seekcompChk.split(',')
						if seekcompChk:
							seekcomp = "pers="+seekcompChk[0]
						#
					#
				except:
					pass
				#
				try:
					if seekline.index('oldremovals n=1') > 0:
						seektype = "reremove"
						seekcompChk = re.sub('n=[0-9]', '', seekline)
						seekcompChk = re.sub('[^0-9]', '', seekcompChk[-16:])
						if seekcompChk:
							seekcomp = seekcompChk
						#
					#
				except:
					pass
				#
				try:
					if seekline.index('total 1 companies found') > 0:
						seekcompChk = re.sub('[^0-9]', '', seekline[-16:])
						if seekcompChk:
							seekcomp = seekcompChk
						#
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('total 2 companies found') > 0:
						seekcompChk = re.sub('[^0-9,]', '', seekline[-16:])
						seekcompChk = seekcompChk.split(',')
						if seekcompChk:
							seekcomp = seekcompChk[0]
						#
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('new company record') > 0:
						seekcompChk = re.sub('[^0-9]', '', seekline[-16:])
						if seekcompChk:
							seekcomp = seekcompChk
						#
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('incomplete-nonmatching-lead') > 0:
						seekcomp = "incomplete-nomatch"
						seekfound = True
					#
				except Exception as e:
					pass
				#move
				try:
					if seekline.index('multi-company-match-lead') > 0:
						seekcomp = "multi-company"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('failed-email-removal') > 0:
						seekcomp = "remove-failed"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('ref=unhandled-lead') > 0:
						seekcomp = "un-handled"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('changenfo-group') > 0:
						seekcomp = "changenfo"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('no to/from address found') > 0:
						seekcomp = "no-to-from"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('unknown to address') > 0:
						seekcomp = "unk-to-addr"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('un-matched-lead') > 0:
						seekcomp = "un-matched"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('too few companies were') > 0:
						seekcomp = "too-few-comp"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				try:
					if seekline.index('too many companies were found') > 0:
						seekcomp = "too-few-comp"
						seekfound = True
					#
				except Exception as e:
					pass
				#
				
				
				if seekcomp and seektype:
					seekfound = True
				#
			#
			if seekfound:
				# print(time.ctime(),"Found a processed event:", seektype, seekcomp, seekdate)
				countPasses[seektype] += [(seekcomp, seekdate)]
			else:
				try:
					if seeklog.index('exception is'):
						continue
					#
				except:
					pass
				#
				print(time.ctime(),"Found an unclear message...", seektype, seekcomp, seeklog)
				print(time.ctime(),'End of First print ---------------------------------------------------------')#[0:2*1024])
				sys.stdout.flush()
				if not seekcomp:
					countErrors['no-company'] += 1
				#
				if not seektype:
					countErrors['no-type'] += 1
				#
				fh.seek(-seeklen, 1)
		sourcef = PATH_BASE + '/' + eaFile
		dest =  move_path + '/' + eaFile
		move(sourcef, dest)
		#
	except Exception as e:
		print(time.ctime(),"Exception(1):", e)
		print(time.ctime(),'End of Second print ---------------------------------------------------------')
		sys.stdout.flush()
	fh.close()
	
#
endLog = time.time()
runLog = endLog - startLog
# Dump the result of log parssing to a CSV file
import csv
pathTempCSV =  os.path.abspath('temp-responses.csv')
outputFile = open(pathTempCSV,'w')
print(time.ctime(),'Time necessary to parse the log files', runLog)
sys.stdout.flush()
for eaType in countPasses:
	for eaValue in countPasses[eaType]:
		if 'pers' in eaValue[0].strip() :
			# print(time.ctime(),"ProcAsPerson")
			personId = re.sub(r'[^0-9]','',eaValue[0])
			compId = 'None'
		else:
			personId = 'None'
			compId = eaValue[0].strip()
			compId = re.sub(r'[^0-9]', '', compId)
			if compId == 205223216162: continue
			if not compId: compId = 'None'
		#
#		newrow = {'mres_companyid':compId,
#				  'mres_datetime':eaValue[1],
#				  'mres_type': eaType,
#				  'mres_personid':personId}
		outputWriter = csv.writer(outputFile ,delimiter='\t')
		outputWriter.writerow([compId,personId,eaValue[1],eaType])
outputFile.close()
# Connection to Postgres
import pg8000
pg8000.paramstyle = 'qmark'
dbc = pg8000.connect(
	user=""
	, password=""
	, host=""
	, port=5432
	, database="marketing"
)
dbc.autocommit = True	
db = dbc.cursor()



# Import the CSV file to the database
print(time.ctime(),"Importing into mark_responses")
sys.stdout.flush()
csvSource = pathTempCSV
try:
	db.execute('''DROP TABLE temp_table;''')
except:
	pass
#
db.execute('''
			-- create temp_table
			CREATE TABLE temp_table
			(
			mres_companyid varchar(255),
			mres_personid varchar(255),
			mres_datetime varchar(255),
			mres_type varchar(255)
			);
			''')
db.execute('''	
			-- import csv file into the temp_table
			 COPY temp_table 
			 FROM '%s' 
			DELIMITER '\t' CSV;
		''' %(csvSource))
db.execute('''
			-- insert data from the temp_table into mark_attempts
			INSERT INTO  mark_responses
				(mres_companyid, mres_personid, mres_datetime, mres_type)
			SELECT mres_companyid, mres_personid, NULLIF(NULLIF(mres_datetime, ''), 'None')::timestamp as mres_datetime, mres_type
				FROM temp_table				
			''')
db.execute('''
			-- delete the temp_table
			DROP TABLE temp_table			   
			''')
dbc.commit()



# Update mres_companyid by referencing mres_personid from person table 
print(time.ctime(),'Start updating companyid based on personId')
sys.stdout.flush()
startUpdate = time.time()
db.execute("""
			update mark_responses
			set mres_companyid = (
			  select pers_companyid
			  from person
			  where pers_personid = mres_personid
			)
			where mres_personid != 'None'
				""")
print(time.ctime(),'Update query run for', time.time()- startUpdate)
dbc.commit()



# Delete the duplicate rows
print(time.ctime(),'Deleting duplicates now')
startDeleteDup = time.time()
db.execute(''' 
DELETE FROM mark_responses 
WHERE mres_responseid IN (SELECT mres_responseid
  FROM (SELECT mres_responseid,
			   ROW_NUMBER() 
				   OVER (partition BY  mres_companyid, 
									   mres_datetime, 
									   mres_type 
									   ORDER BY mres_responseid) AS rnum
		 FROM mark_responses) t
  WHERE t.rnum > 1);
			''')
print(time.ctime(),'Delete duplicate query run for:', time.time()- startDeleteDup)
sys.stdout.flush()
dbc.commit()



# UPDATE the existing companyid with the one that was merged to
# For each row in the source file, run an update query
print(time.ctime(),'Updatating the existing companyid with the one that was merged to')
import time
sratUpCompId = time.time()
import os
basePath = os.path.abspath('../../data/crm-tables/')
sourceFile = open(basePath + '/' + 'comp_mergings')
limit = 0
for eaRow in sourceFile:
	comg_mergefrom, comg_mergeto, junk = eaRow.split('\t')
	db.execute(''' 
			update mark_responses
			set mres_companyid = '%s'
			where mres_companyid = '%s'
			''' %(comg_mergeto, comg_mergefrom, ))
print(time.ctime(),'Rows affected: '+ str(db.rowcount))
print(time.ctime(),'Query ran for:' + str(time.time()- sratUpCompId))



# Clear any responses marked as 'hot leads' and re-assign values for the column
print(time.ctime(),'Updating mres_ishotlead')
db.execute('''
update mark_responses set mres_ishotlead = false;
			''')

db.execute('''
update mark_responses mres_outer set mres_ishotlead = true
where not exists(
	select mres_datetime from mark_responses as mres_inner
	where mres_inner.mres_companyid = mres_outer.mres_companyid
		and mres_inner.mres_datetime > mres_outer.mres_datetime
		and mres_inner.mres_type	= 'lead'
)
and mres_type	= 'lead';
		''')

dbc.commit()


dbc.close()

Delete the CSV file
# print(time.ctime(),'Delteing the tem-CSV file')
# del_path = os.getcwd()
# print(time.ctime(),'Deleting the CSV files')
# lsDeleteFiles = [l for l in os.listdir(del_path) if l.endswith('.csv')]
# for eaFile in lsDeleteFiles:
	# print(time.ctime(),os.remove(del_path +'/'+ eaFile))
	# os.remove(del_path +'/'+ eaFile)


print(time.ctime(),' Done!!!')
print(time.ctime(),'Script run for:', time.time() - startExecTime )
sys.stdout.flush()
