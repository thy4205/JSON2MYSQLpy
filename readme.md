# JSON2MYSQLpy
JSON2MYSQLpy is a simple python script that creates Replace statments that inserts JSON data into a pre-made MySQL table with the help of the MySQLi plugin. It is an alternative solution to my previously released JSON2MYSQLphp (formally JSON2MYSQL) 

JSON2MYSQLpy attempt create the `create table` that are exported from MSSQL2JSON. However, there is index or key feature

The script is designed for working alongside MSSQL2JSON. While it would work for any other JSON file with the correct format, there is no reason to do so. 

## Feature
* create insert statement from JSON file created by MSSQL2JSON then inseert the data into a stuctrually compatible table.

## Requirement
* PHP with MySQLi plug-in installed
* JSON file created from MSSQL2JSON
* Empty Table with columes correctly setup for import 

## Instructions
1. Download or git clone the project if you feel like being fancy

1. Change the required parameters as stated in the script
  * Database IP address / Hostname 
  * Database Table Name
  * User Name
  * Password
1. Run the script in Command Prompt/bash with `py json2mysql.py`  

