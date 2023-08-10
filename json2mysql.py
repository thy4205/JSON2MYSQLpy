import json
import os
import glob
import pprint
import mysql.connector
import pyodbc
import codecs

#link = mysql.connector.connect( host='127.0.0.1', user='kf4', password ='Kf6655caton!', database ='test',port='3306' );
server = '127.0.0.1'
database = 'test'
username = ''
password = ''



link = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';autocommit=False')
cursor = link.cursor()
numberOfChunkInEachQuery = 20
keywordList = []
try:
    path = os.path.dirname(__file__)
    link.autocommit = False
    link.execute("SET autocommit=0")
    cursor.execute("START TRANSACTION")

    clearedTable = []

    for filename in glob.glob(os.path.join(path, 'import_*.json')): #only process .JSON files in folder.  

        with open(filename, encoding='utf-8', mode='r') as json_file:
            data = json.load(json_file)
            tablename = data['tablename'].lower()
            datatype = data['datatype']
            columnSize = data['columnSize']
            nullable = data['nullable']
            trueRowCount = len(data['rows'])
            clearTableStatus = data['clearTable'] 
            
            if clearTableStatus == True and tablename not in clearedTable:
                cursor.execute('Truncate '+tablename)
                print('Truncated '+tablename)
                clearedTable.append(tablename)

            
            createTableQuery = "CREATE TABLE IF NOT EXISTS "+tablename+"(";
            colIndex= 0;
            print ('importing: '+tablename+'...')
            for colume in data['columns']:
                createTableQuery+=colume
                match datatype[colIndex]:
                    case "bit":
                        createTableQuery+=" "+str(datatype[colIndex])+"("+str(columnSize[colIndex])+")"
                    case "varchar":
                        createTableQuery+=" "+str(datatype[colIndex])+"("+str(columnSize[colIndex])+")"
                    case "float":
                        createTableQuery+=" DOUBLE"
                    case "int identity":
                        createTableQuery+=" INT"
                    case "smalldatetime":
                        createTableQuery+=" DATETIME"
                    case _:
                        createTableQuery+=" "+datatype[colIndex]
                if nullable[colIndex]:
                    createTableQuery+=str(" NOT NULL")
                
                
                colIndex += 1
                if int(colIndex)<len(columnSize):
                    createTableQuery+=str(",")
            createTableQuery+=str(");")
            if clearTableStatus == True and tablename not in clearedTable:
                print("Creating Table: "+tablename)
                cursor.execute(createTableQuery)
            #print("SET FOREIGN_KEY_CHECKS=0")
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            tempjson = []
            for row in data['rows']:
                #print (datatype)
                tempjson.append(dict(zip(data['columns'], row)))
            #for i in data['rows']:
            
            start = 0
            end = len(tempjson)
            jsonchunck = []
            
            #rearrage the json file so the insert speed is reasonable
            for i in range(start, end, numberOfChunkInEachQuery):
                x = i
                jsonchunck.append (tempjson[x:x+numberOfChunkInEachQuery])
            
            x=0
        #print (len(tempjson));
        for chunkrow in jsonchunck:
            
            query=  "REPLACE INTO "+ tablename +" ("+(", ".join(data['columns']))+") VALUES "
            
            i=0
            #print ('\n')
            #print (row)
            #row = row[0]
            
            fieldNo = range(len(chunkrow[0]))
            
            chunkLoop = 0;
            while chunkLoop<len(chunkrow):
                query+="("
                for i in fieldNo:
                    query+='?,'
                query = query[:-1]+"),"
                chunkLoop+=1
            query = query[:-1]           
            
            insertContent = []
            for row in chunkrow:
                i=0
                for rvalue in row:
                
                    key = rvalue
                    value = row[rvalue]
                    #print (key+"->"+str(value))
                    #if value is None or value=='':
                    if (value=='' and 'bit' not in datatype[i]) or value is None  :
                        insertContent.append(None)
                    else:                
                        if 'bit' in datatype[i]:
                            #insertContent.append(int(1 if str(value)=="True" else 0))
                            insertContent.append(bool(1) if str(value).lower()=="true" else bool(0))
                            # if str(value).lower()=="true":
                                # print(key+"ha")
                            # else:
                                # print(key+"he")
                        else:
                            if 'date' in datatype[i]:
                                if str(value)=='0000-00-00 00:00:00':
                                    insertContent.append(None)
                                else:
                                    insertContent.append(str(value))
                            else:
                                insertContent.append(str(value))
                    i+=1
                
            x+=1 
            processPercentagge = str(trueRowCount) if x*numberOfChunkInEachQuery>trueRowCount else str(x*numberOfChunkInEachQuery)
            print (processPercentagge+"/"+str(trueRowCount)) 

            #insertContent = "("+','.join(insertContent)+")"
            #print (query)  
            #print (insertContent)  
            cursor.execute(query,insertContent)
            cursor.execute("ALTER TABLE "+tablename+" AUTO_INCREMENT = 1000")
        os.remove(filename)
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    cursor.commit()
    print("import success")
except Exception as e:
    cursor.rollback()
    print(e)