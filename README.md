# Use dashDB data in Watson Dialog conversations
This example shows how to combine the Watson Dialog Service and a database like dashDB (both available on Bluemix) to have dynamic and user-dependent data in a conservation. The services are provisioned on Bluemix and are used by a locally run Python script. The dialog has been registered using the [watson-dialog-tool](https://github.com/data-henrik/watson-dialog-client) from one of my other repositories. Also see my related blog entries:
* [Bluemix: Where Python and Watson are in a Dialog](http://blog.4loeser.net/2016/07/bluemix-where-python-and-watson-are-in.html)

## Overview
The data-backed dialog is driven by a Python script that communicates with the Watson Dialog and dashDB services. The dialog itself needs to be specified in an XML file and registered before invoking that script (see Setup). The database is prepared by creating a single table and inserting some rows. The script reads most of the configuration from a file, only the dialogID needs to be hardcoded (for the sake of simplicity).

Files:
* dialog.py: Python script that drives the dialog with Watson and interacts with dashDB
* dataDialog.xml: Dialog specification, needs to be registered with the Watson Dialog service
* dashDB.sql: SQL statements for dashDB to create a table and populate it with sample data
* config.json: holds the credentials for the Watson Dialog service and for dashDB

## Setup

## Sample

