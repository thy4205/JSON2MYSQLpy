# JSON2MYSQLpy
JSON2MYSQLpy is a simple python script that creates Replace statments that inserts JSON data into a pre-made MySQL tables with the help of the OBDC Driver. It is an alternative solution to my previously released JSON2MYSQLphp (formally JSON2MYSQL) 

JSON2MYSQLpy attempt create the `create table` that are exported from MSSQL2JSON. However, index or key is not included.

The script is designed for working alongside MSSQL2JSON. While it would work for any other JSON file with the correct format, there is no reason to do so. 

## Feature
* create insert statement from JSON file created by MSSQL2JSON then inseert the data into a stuctrually compatible table.

## Requirement
* Python 3.10 or newer version due to the use of switch statment in the script
* MySQL OBDC Driver 
* JSON file created from MSSQL2JSON
* Empty Table with columes correctly setup for import (Optional,as the script can help building a simple version of the said table)

## Instructions
1. Download or git clone the project if you feel like being fancy

1. Change the required parameters as stated in the script
  * Database IP address / Hostname 
  * Database Table Name
  * User Name
  * Password
1. Put the JSON files in the same directory of this script. Please be reminded that the JSON files must have "import" as their prefixes.

1. Run the script in Command Prompt/bash with `py json2mysql.py`  

