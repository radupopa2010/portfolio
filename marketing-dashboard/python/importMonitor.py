#!/usr/bin/python3
# Monitor the import folders and if any files there,
# execute the coresponding script

# Redirect the output to a log file
#sys.stdout = open("c:\\lastRun.log", "w")
#
import os, time, datetime
import sys
import schedule

print (time.ctime(),"Import monitor startup: ")
sys.stdout.flush()
base_path = os.path.abspath('../')
# print(base_path)
update_crm_tables = ''.join([base_path,'/data/crm-tables/pending'])
import_insite_attempts = ''.join([base_path,'/data/insite-attempts/pending'])
import_insite_responses = ''.join([base_path,'/data/insite-responses/pending'])

pythonScripts = ''.join([base_path,'/python/import'])
exportToMongo = ''.join([base_path,'/python'])


def UploadsReadyCheck(filelist):
	for filepath in filelist:
		mtimeLastCheck = os.stat(filepath).st_mtime
		time.sleep(5)
		if not (os.stat(filepath).st_mtime == mtimeLastCheck):
			return False
		#
	#
	return True
#

def update_crm_company():
	base_path = os.path.abspath('../')
	pythonScripts = ''.join([base_path,'/python/import'])
	update_crm_tables = ''.join([base_path,'/data/crm-tables/pending'])
	uct_shouldExecute = [update_crm_tables+'/'+l for l in os.listdir(update_crm_tables)]
	if uct_shouldExecute:
		if not UploadsReadyCheck(uct_shouldExecute):
			print(time.ctime(),"Uploads are still in progress...")
			sys.stdout.flush()
			time.sleep(2)
		
		os.chdir(pythonScripts)
		print(time.ctime(),'\n\n-------------- Running ./001import_crm_tables.py ------------------')
		sys.stdout.flush()
		os.system('./001import_crm_tables.py')
		sys.stdout.flush()
		os.chdir(exportToMongo)
		print(time.ctime(),'\n\n\n-------------- Running ./export_to_mongo.py ------------------')
		os.system('./export_to_mongo.py')
		sys.stdout.flush()
		print_timers()
	#
#
# Schedule a run for "./001import_crm_tables.py"
timer_monday = schedule.every().monday.at("21:00").do(update_crm_company)
timer_tuesday = schedule.every().tuesday.at("21:00").do(update_crm_company)
timer_wednesday = schedule.every().wednesday.at("21:00").do(update_crm_company)
timer_thursday = schedule.every().thursday.at("21:00").do(update_crm_company)
timer_friday = schedule.every().friday.at("21:00").do(update_crm_company)

def print_timers():
	print('timer_monday: %s' % (timer_monday,))
	print('timer_tuesday: %s' % (timer_tuesday,))
	print('timer_wednesday: %s' % (timer_wednesday,))
	print('timer_thursday: %s' % (timer_thursday,))
	print('timer_friday: %s' % (timer_friday,))
	
# print_timers()

doLogHeartbeat = True
while 1:
	# Check the folders every minute
	schedule.run_pending()
	#
	iia_shouldExecute = [import_insite_attempts+'/'+l for l in os.listdir(import_insite_attempts)]
	iir_shouldExecute = [import_insite_responses+'/'+l for l in os.listdir(import_insite_responses)]
	#
	if iia_shouldExecute:
		if not UploadsReadyCheck(iia_shouldExecute):
			print(time.ctime(),"Uploads are still in progress...")
			sys.stdout.flush()
			time.sleep(2)
			continue
		#
		print(time.ctime(),'\n\n\niia_shouldExecute: ',iia_shouldExecute)
		sys.stdout.flush()
		sys.stdout.flush()
		os.chdir(pythonScripts)
		print(time.ctime(),'\n\n\n ------------- Running  ./002import_insite_attempts.py -----------')
		os.system('./002import_insite_attempts.py')
		os.chdir(exportToMongo)
		print(time.ctime(),'\n\n ------------- Running  ./export_to_mongo.py -----------')
		os.system('./export_to_mongo.py')
		sys.stdout.flush()
		continue
		#
	#
	if iir_shouldExecute:
		if not UploadsReadyCheck(iir_shouldExecute):
			print(time.ctime(),"Uploads are still in progress...")
			sys.stdout.flush()
			time.sleep(2)
			continue
		#
		os.chdir(pythonScripts)
		print('\n\niir_shouldExecute: ',iir_shouldExecute)
		sys.stdout.flush()
		print(time.ctime(),'\n\n ------------- Running  ./003import_responses.py -----------')
		sys.stdout.flush()
		os.system('./003import_responses.py')
		os.chdir(exportToMongo)
		print(time.ctime(),'\n\n ------------- Running  ./export_to_mongo.py -----------')
		sys.stdout.flush()
		os.system('./export_to_mongo.py')
		sys.stdout.flush()
		continue
		#
	#
	# Print a "sleeping" message once an hour 
	currentHoursMinute = datetime.datetime.now().minute
	if currentHoursMinute > 1:
		if doLogHeartbeat:
			print('sleeping: ',time.ctime())
			sys.stdout.flush()
		#
		doLogHeartbeat = False
	else:
		doLogHeartbeat = True
	#
	sys.stdout.flush()
	time.sleep(1)
		
