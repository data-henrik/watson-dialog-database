# Drive dialog from IBM Watson Dialog Service on Bluemix
#
# It fetches This is a simple Python script I developed to manage my
# dialogs when testing the IBM Watson Dialog Service on Bluemix.
# The script takes some command line arguments and then calls
# the related service API. The entire result is always dumped.
#
# Some of the source is taken from this SDK example:
# https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/dialog_v1.py
#
# Author: Henrik Loeser

import json
from os.path import join, dirname
# API support for Watson Dialog service
from watson_developer_cloud import DialogV1
#Driver for dashDB / DB2
import ibm_db


# Load credentials for Watson Dialog and dashDB from file
with open("config.json") as confFile:
     configs=json.load(confFile)
     dialogConfig=configs['credentials']
     db2cred = configs['dashDB']

# create dialog interface
dialog = DialogV1(
    username=dialogConfig['username'],
    password=dialogConfig['password'])

# hardcoded dialogID - use my watson-dialog-tool with list option to get ID
dialogID = 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'


# connect to DB2 / dashDB
db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")


# fetch record from dashDB
def fetchRecordForName(username):
  sqlstmt="select * from dialogdata where fname='"+username+"'"
  # Some debugging
  print sqlstmt

  # execute SQL query and fetch single result
  stmt = ibm_db.exec_immediate(db2conn, sqlstmt)
  result = ibm_db.fetch_assoc(stmt)
  return result

# get table count from dashDB
def getTableCount():
  sqlstmt="select count(*) from dialogdata"
  print sqlstmt

  # execute SQL query and fetch single result
  stmt = ibm_db.exec_immediate(db2conn, sqlstmt)
  result = ibm_db.fetch_assoc(stmt)
  return result

# get table list from dashDB
def getTableList():
  sqlstmt="select count(*) from syscat.tables where tabschema = current user"
  print sqlstmt

  stmt = ibm_db.exec_immediate(db2conn, sqlstmt)
  result = ibm_db.fetch_assoc(stmt)
  return result

# Start a dialog and converse with Watson
def converse(dialogID):
  dataFetched=False
  print "Starting a dialog, stop by Ctrl+C or saying 'bye'"
  print "================================================\n"
  # Start the dialog
  resp = dialog.conversation(dialogID)
  # Output is printed. It is not pretty, but takes care of all parts...
  for message in resp['response']:
     print message

  # Now loop to chat
  while True:
    # get some input
    dinput = raw_input("Please enter:\n")
    # if we catch a "bye" then exit
    if (dinput == "bye"):
      break
    # send the input to Watson
    resp=dialog.conversation(dialog_id=dialogID,
                             dialog_input=dinput,
                             conversation_id=resp['conversation_id'],
                             client_id=resp['client_id'])
    print(json.dumps(resp))

    # get the profile variables
    dprofile=dialog.get_profile(dialogID, resp['client_id'])
    print(json.dumps(dprofile))

    # now loop over variables to see if we have to react
    for data in dprofile['name_values']:
      # username was set, now fetch details
      if data['name']=='username':
        print "username was set to "+data['value']+"\n"
        if dataFetched==False:
          record=fetchRecordForName(data['value'])
	  dataFetched=True
          # Use of str to convert date to string
          print dialog.update_profile(
            dialogID, client_id=resp['client_id'],
                name_values=[{"name": "lastname", "value": record["LNAME"]},
                {"name": "firstname", "value": record["FNAME"]},
                {"name": "bdate", "value": str(record["BDATE"])}])

      # count of records in the dialogdata table
      if data['name']=='service' and data['value']=='tablecount':
          record=getTableCount()
          print record

      # list of tables in our namespace (database schema)
      if data['name']=='service' and data['value']=='listtables':
          record=getTableList()
          print record

    # print the next message(s)
    for message in resp['response']:
       print message


#
# Main program, for now just converse and then end dashDB connection
#
if __name__ == '__main__':
  
   converse(dialogID)
   ibm_db.close(db2conn)
