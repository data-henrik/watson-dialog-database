# Use dashDB data in Watson Dialog conversations
This example shows how to combine the Watson Dialog Service and a database like dashDB (both available on Bluemix) to have dynamic and user-dependent data in a conservation. The services are provisioned on Bluemix and are used by a locally run Python script. The dialog has been registered using the [watson-dialog-client][watson-dialog-client] from one of my other repositories. Also see my related blog entries:
* [Bluemix: Where Python and Watson are in a Dialog](http://blog.4loeser.net/2016/07/bluemix-where-python-and-watson-are-in.html)

## Overview
The data-backed dialog is driven by a Python script that communicates with the Watson Dialog and dashDB services. The dialog itself needs to be specified in an XML file and registered before invoking that script (see Setup). The database is prepared by creating a single table and inserting some rows. The script reads most of the configuration from a file, only the dialogID needs to be hardcoded (for the sake of simplicity).

**Files**:
* dialog.py: Python script that drives the dialog with Watson and interacts with dashDB
* dataDialog.xml: Dialog specification, needs to be registered with the Watson Dialog service
* dashDB.sql: SQL statements for dashDB to create a table and populate it with sample data
* config.json: holds the credentials for the Watson Dialog service and for dashDB

## Setup
The necessary setup before using the dialog.py script consists of provisioning the [Watson Dialog](https://new-console.ng.bluemix.net/catalog/services/dialog/) and [dashDB](https://new-console.ng.bluemix.net/catalog/services/dashdb/) services in [IBM Bluemix](http://www.ibm.com/cloud-computing/bluemix/), then preparing both.

You need a Python environment with the "watson-developer-cloud" and "ibm_db" modules installed ("pip install ...").

1. Login to Bluemix, provision a Watson Dialog service, copy & paste the service credentials to the config.json file.
2. Next provision a dashDB service, copy the service credentials to the config.json file
3. Launch the dashDB management dashboard and open the "Run SQL" wizard. Past the contents from dashDB.sql into the emptied form and then click "Run" to execute the SQL statements. There should be several success messages with a table created and some rows inserted.
4. If not done already, obtain the [watson-dialog-client][watson-dialog-client]. Register the file dataDialog.xml as new dialog and obtain the dialogID.
5. Edit dialog.py and change the hardcoded dialogID.

Now everything should be set to give it a try.

## Sample Run

The following shows a sample run of the script. The answer to the first question is a simple "Max", followed by a "list tables" and later on a "What is my age". The dialog is ended by answering "bye". Based on the debug output (see the file [dialog.py](dialog.py)), you should be able to see how the script interacts with Watson and dashDB.

```
[henrik@hisMachine]$ python dialog.py 
Starting a dialog, stop by Ctrl+C or saying 'bye'
================================================

Hi, I'm a bot! Who are you?
Please enter:
Max
{"conversation_id": 4132689, "input": "Max", "confidence": 1.0, "response": ["Hi Max!", "", "What service would you like?"], "client_id": 4325014}
{"name_values": [{"name": "username", "value": "Max"}]}
username was set to Max

select * from dialogdata where fname='Max'
{u'name_values': [{u'name': u'lastname', u'value': u'Mustermann'}, {u'name': u'firstname', u'value': u'Max'}, {u'name': u'bdate', u'value': u'1977-09-22'}], u'client_id': 4325014}
Hi Max!

What service would you like?
Please enter:
list tables
{"conversation_id": 4132689, "input": "list tables", "confidence": 1.0, "response": ["", "Mustermann, what other stuff are you in the mood for?", "", "What service would you like?"], "client_id": 4325014}
{"name_values": [{"name": "username", "value": "Max"}, {"name": "lastname", "value": "Mustermann"}, {"name": "firstname", "value": "Max"}, {"name": "bdate", "value": "1977-09-22"}, {"name": "service", "value": "listtables"}]}
username was set to Max

select count(*) from syscat.tables where tabschema = current user
{'1': '14'}

Mustermann, what other stuff are you in the mood for?

What service would you like?
Please enter:
what is my age
{"conversation_id": 4132689, "input": "what is my age", "confidence": 1.0, "response": ["Your birthdate is 1977-09-22", "", "What service would you like?"], "client_id": 4325014}
{"name_values": [{"name": "username", "value": "Max"}, {"name": "lastname", "value": "Mustermann"}, {"name": "firstname", "value": "Max"}, {"name": "bdate", "value": "1977-09-22"}, {"name": "service", "value": "listtables"}]}
username was set to Max

select count(*) from syscat.tables where tabschema = current user
{'1': '14'}
Your birthdate is 1977-09-22

What service would you like?
Please enter:
bye
```

# Links
* Try out IBM Bluemix at http://www.ibm.com/cloud-computing/bluemix/
* See the IBM Bluemix documentation at https://console.ng.bluemix.net/docs/
* Ask Bluemix programming question on Stack Overflow at http://stackoverflow.com/questions/tagged/bluemix


[watson-dialog-client]: https://github.com/data-henrik/watson-dialog-client
