"""
requires:
  SendKeys  ~ pip install SendKeys
  pywinauto ~ pip install pywinauto
  pyperclip ~ pip install pyperclip
"""
import threading, pyautogui, time, locale, datetime, smtplib, pyperclip,re
from pywinauto import application
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Set Local time and time format like "Mon May 04 13:09:47 2015"
locale.setlocale(locale.LC_ALL, '')
localtime = time.asctime(time.localtime(time.time()))
# ---------------Launch vSphere application ----------------------
app = application.Application()
app.start_(r"C:\Program Files (x86)\VMware\Infrastructure\Virtual Infrastructure Client\Launcher\VpxClient.exe")
# Set focus on vSphere and type in the login credentials
app.window_(title='VMware vSphere Client')
app.window_().TypeKeys('root{TAB}popa_jn9A{ENTER}')
time.sleep(2)
app.window_().TypeKeys('{ENTER}')
# ------------- END of connection successfully -------------------

#------------- Wait for  192.168.1.208 - vSphere Client ----------
window = None
iTries = 0
while True:
  iTries += 1
  try:
     # catch the "Window not found" error and try again
     window = app.window_(title=u'192.168.1.208 - vSphere Client')
     window["TreeView"].Click()
     break
  except Exception as e:
     # if login takes longer than 27 seconds or fails notify the admin
     if iTries >9:
        print("vShpere faild loging")
        S = smtplib.SMTP('taycor-com.mail.protection.outlook.com', 25)
        Msg = MIMEText("vShpere faild loging", 'Admin attention required')
        Msg['Subject'] = "BackUpBot"
        Msg['From'] = "butler@taycor.com"
        Msg['To'] = "radupopa2010@yahoo.com"
        S.sendmail(Msg['From'], Msg['To'].split(';'), Msg.as_string())
        S.quit()
        exit()
     print("Window '192.168.1.42 - vSphere Client' is loading, please wait ", e)
     time.sleep(3)  #sleep for 3 seconds
  #
#---------- END of Wait for  192.168.1.208 - vSphere Client ------

#------------- After login, send right arrow key 4 times, in order to navigate to the first virtual machine ----------------------
time.sleep(3)
window["TreeView"].Click()
window["TreeView"].TypeKeys('{RIGHT}{RIGHT}{RIGHT}{RIGHT}')
time.sleep(2)
# -------------End of "navigate to target VM" --------------------

def ProcessVmSnapshot(app, window, thisVmName):
  # right click on the virtual machine
  # select "Snapshot" from the menu -> select "Tke Snapshot"
  # name the snapshot and paste in the date and time when the snapshot was taken
  # click "OK"
  import re, time
  window.TypeKeys('+{F10}')
  time.sleep(2)
  window.TypeKeys('{DOWN}')
  time.sleep(1)
  window.TypeKeys('{DOWN}')
  time.sleep(1)
  window.TypeKeys('{DOWN}')
  time.sleep(1)
  window.TypeKeys('{RIGHT}')
  time.sleep(1)
  window.TypeKeys('{ENTER}')
  time.sleep(1)
  snap_window = app.window_(title=u'Take Virtual Machine Snapshot')
  snap_window.TypeKeys(re.sub(r' ', '{SPACE}', '%s - %s' % (thisVmName, time.ctime())))
  time.sleep(1)
  # deselect "Snapshot the virtual machine's memory "
  snap_window.TypeKeys('{TAB}')
  time.sleep(1)
  snap_window.TypeKeys('{TAB}')
  time.sleep(1)
  snap_window.TypeKeys('{SPACE}')
  time.sleep(1)
  snap_window['OK'].Click()
  time.sleep(1)

def GetSelectedVmName():
  #   Send rename command (F2) so I can get access to the VM's name
  #   copy the auto-selected text (^c) from the clipboard
  #   and then stop the rename by pressing "Escape" from the keyboard(ESC)
  window.TypeKeys('{F2}')
  time.sleep(1)
  window.TypeKeys('^c{ESC}')
  vmName = str(pyperclip.paste())
  # Use the data in the clipboard to determine the active VM
  return vmName

#-------- Check the if selected Virtual Machine's name is the one I want to back up ------------------------------
#   If yes, take a snapshot and wait 5 minutes to be sure the process ended successfully
thisVmName = GetSelectedVmName()
print(thisVmName)
time.sleep(1)  # REMINDER  modify this value when done testing the program

if thisVmName == "backup_worker_win6":
  ProcessVmSnapshot(app, window, thisVmName)
  time.sleep(1) #sleep for 300 seconds/ 5 minutes
else:
  # notify the admin, by sending an e-mail
  S = smtplib.SMTP('taycor-com.mail.protection.outlook.com', 25)
  Msg = MIMEText("snapshot failed", 'Admin attention required')
  Msg['Subject'] = "BackUpBot"
  Msg['From'] = "butler@taycor.com"
  Msg['To'] = "radupopa2010@yahoo.com"
  S.sendmail(Msg['From'], Msg['To'].split(';'), Msg.as_string())
  S.quit()
  exit()
#------- Make sure 192.168.1.208 is slected in the left side -----
window.TypeKeys('{LEFT}')
time.sleep(1)
window.TypeKeys('{LEFT}')
time.sleep(1)
window.TypeKeys('{LEFT}')
time.sleep(1)
window.TypeKeys('{LEFT}')
time.sleep(1)
window.TypeKeys('{LEFT}')
time.sleep(1)
window.TypeKeys('{LEFT}')
time.sleep(1)
#--------- END of 192.168.1.208 slection process -----------------

'''
----------------- PART 2 OF THE PROGRAM --------------------------

                 COPYING THE VIRTUAL DISK ------------------------------------------------------------------
'''

import time,re, pyperclip
from pywinauto import application
app = application.Application()
# Make sure I connect to the vSphere application
app.connect_(title=u'192.168.1.208 - vSphere Client')   #'192.168.1.208 - vSphere Client'
window = app.window_(title=u'192.168.1.208 - vSphere Client')
# Click on the Summary tab
window[u'Summary'].Click()
time.sleep(2)

# Locate the hard drive where
window["ListViewItem-0"].Click()
time.sleep(2)
window["ListViewItem-0"].TypeKeys('{DOWN}{DOWN}')

def checkHardName():
  #   Send right click ( SHIFT+F10 from the keyboard)  I can get access to Rename option and hardware's name
  #   Select everything with CTRL+A, copy the selected text CTRL+A (^c) from the clipboard
  #   and then stop the rename by pressing "Escape" from the keyboard(ESC)
  window.TypeKeys('+{F10}{DOWN}{DOWN}{ENTER}')
  time.sleep(1)
  window.TypeKeys('^c')
  time.sleep(1)
  window.TypeKeys('{ESC}')
  hardName = str(pyperclip.paste())
  return hardName

# Check hdd name
hddNAme = checkHardName()
print(hddNAme)
if hddNAme == "WD-HDD-2-T":
  # Send Right Click and select Brows data store
  window.TypeKeys('+{F10}{DOWN}{ENTER}')
  # wait 2 second for the window to load
  time.sleep(2)
else:
  # make sure that Western Digital hard is selected
  window["ListViewItem-0"].TypeKeys('{UP}{UP}{DOWN}')
  time.sleep(1)
  hddNAme = checkHardName()
  print(hddNAme)
  if hddNAme == "WD-HDD-2-T":
     # make sure that Western Digital hard is selected
     window.TypeKeys('+{F10}{DOWN}{ENTER}')
     time.sleep(2)
  # wait 2 second for the window to load
# -----------------
# Select the list with the folders containing the virtual machines
window = app.window_(title='Datastore Browser - [WD-HDD-2-T]')
window.Click()
time.sleep(1)
window['tree item'].Click()
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{UP}')
time.sleep(1)

# Search for the folder containing the target virtual machine

def checkFolderName():
  window['ListViewSubItem-0'].TypeKeys('{F2}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('^c')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{ESC}')
  thisFolder = str(pyperclip.paste())
  return thisFolder

thisVmFolderName = checkFolderName()
print(thisVmFolderName)

# search for the folder backup-worker
while "backup-worker" not in thisVmFolderName:
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  thisVmFolderName = checkFolderName()
  print(thisVmFolderName)

# if backup-worker folder is selected press ENTER
if "backup-worker"  in thisVmFolderName:
  window['ListViewSubItem-0'].TypeKeys('{ENTER}')

# search for backup-worker.vmdk file
thisFile = checkFolderName()
while "backup-worker.vmdk" not in thisFile:
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  thisFile = checkFolderName()
  print(thisFile)

# if backup-worker.vmdk file was found copy it to the clapboard
if "backup-worker.vmdk"  in thisFile:
  window['ListViewSubItem-0'].TypeKeys('+{F10}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{ENTER}')
  time.sleep(1)

# store the file size on backup-worker.vmdk for future reference
fileSize = re.compile(r'[\d]+,[\d]+,[\d]+', re.DOTALL)
mo = fileSize.search(thisFile)
vmdkSize = mo.group()
print('vmdk file size is  ' + vmdkSize)
#--------------------------------

# search for the folder named TEST_April_27_2015_back_up_XP_1
#   first Select the list with the folders congaing the virtual machines
window = app.window_(title='Datastore Browser - [WD-HDD-2-T]')
window.Click()
time.sleep(1)
window['tree item'].Click()
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
#       second, start the search
thisFile = checkFolderName()
while "TEST_April_27_2015_back_up_XP_1" not in thisFile:
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  thisFile = checkFolderName()
  #save all the window info, including file size for later usage
  print(thisFile)

# After finding the folder press ENTER to access it.
if "TEST_April_27_2015_back_up_XP_1" in thisFile:
  window['ListViewSubItem-0'].TypeKeys('{ENTER}')

# Paste in the "backup-worker.vmdk" file
#window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(2)
window['ListViewSubItem-0'].TypeKeys('+{F10}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{DOWN}')
time.sleep(1)
window['ListViewSubItem-0'].TypeKeys('{ENTER}')
# sleep 5 seconds so the file starts copying
time.sleep(5)
# -------------- END of COPY - PASTE phase -----------------------

#---------- Verify if the virtual disk file was copied -----------
import time, pyperclip
from pywinauto import application
app = application.Application()
app.connect_(title=u'192.168.1.208 - vSphere Client')   #'192.168.1.208 - vSphere Client'
window = app.window_(title='Datastore Browser - [WD-HDD-2-T]')

def checkFolderName():
  window['ListViewSubItem-0'].TypeKeys('{F2}')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('^c')
  time.sleep(1)
  window['ListViewSubItem-0'].TypeKeys('{ESC}')
  thisFolder = str(pyperclip.paste())
  return thisFolder
# ----------------------------

# press refresh button so the new vmdk file is visible
time.sleep(5)
window["refreshButton"].Click()

# Search in the folder TEST_April_27_2015_back_up_XP_1, for the backup-worker.vmdk file and send call checkFolderName function
filesToCheck = 0    # number of files to check in the folder
thisFile = checkFolderName()
while("backup-worker.vmdk" not in thisFile) and (filesToCheck < 20 ):
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  thisFile = checkFolderName()
  print(thisFile)
  filesToCheck = filesToCheck + 1

if filesToCheck ==20:
window['ListViewSubItem-0'].TypeKeys('{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}{UP}')
time.sleep(3)

filesToCheck = 0
thisFile = checkFolderName()
while("backup-worker.vmdk" not in thisFile) and (filesToCheck < 20) :
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  thisFile = checkFolderName()
  print(thisFile)
  filesToCheck = filesToCheck + 1

# After finding sleep 5 seconds, send checkFolderName again to get file size of vmdk file as a text
filesToCheck =0   # number of files to check
timer = 0     # time  the while loop last and check if
while (vmdkSize not in thisFile) and (timer < 600):   # for my project and testing speed time , 10 minutes
  thisFile = checkFolderName()
  window['ListViewSubItem-0'].TypeKeys('{DOWN}')
  print("copying please wait")
  timer = timer +1
  filesToCheck = filesToCheck +1
  if filesToCheck > 20:
     window["refreshButton"].Click()
     filesToCheck =0
     time.sleep(5)
print("File copied successfully ")
#------------ END of waiting for files to copy -------------------
#------------Send confirmation email code ------------------------
import smtplib
from email.mime.text import MIMEText
S = smtplib.SMTP('taycor-com.mail.protection.outlook.com', 25)
Msg = MIMEText("Virtual disk copied SUCCESSFULLY", 'Virtual disk copied SUCCESSFULLY')
Msg['Subject'] = "BackUpBot"
Msg['From'] = "butler@taycor.com"
Msg['To'] = "radupopa2010@yahoo.com"
S.sendmail(Msg['From'], Msg['To'].split(';'), Msg.as_string())
S.quit()
exit()
#-----------End of confirmation email code -----------------------
