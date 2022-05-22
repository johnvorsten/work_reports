# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:07:14 2019

@author: z003vrzk
"""
import pyodbc
import pandas as pd
import sqlalchemy


def create_master_connection():
    """Used for connection to the master database under the server
    .\DT_SQLEXPR2008 where . is the users desktop and DT_SQLEXPR2008
    is the SQL server setup on each users desktop.
    
    return cursorMaster, connMaster"""
    #Create pyodbc connection
    connMaster = pyodbc.connect('DRIVER={SQL Server Native Client 10.0}; SERVER=.\DT_SQLEXPR2008;DATABASE=master;Trusted_Connection=yes;')
    cursorMaster = connMaster.cursor()
    return cursorMaster, connMaster

def check_db_exist(database, cursorMaster):
    sql = """SELECT name FROM master.sys.databases"""
    cursorMaster.execute(sql)
    names = cursorMaster.fetchall() #get all names
    names = [name[0] for name in names] #convert row object to list object
    
    return names.__contains__(database) #True if database is connected

def create_JobDB_test_connection():
    """Used in connection to PBJobDB database.  This is the connection to
    the database specifeid by the user, and the job database.  User the standard
    global outputs "conn" (pyodbc) and "engine" (sqlalchemy) to execute sql
    querys or manipulate data with pandas
    
    return engine, conn, cursor"""

    engine = sqlalchemy.create_engine('mssql+pyodbc://.\DT_SQLEXPR2008/JobDB_test?driver=SQL+Server+Native+Client+10.0') #TODO Change JobDB_test
    engine.connect()
    
    conn = pyodbc.connect('DRIVER={SQL Server Native CLient 10.0};SERVER=.\DT_SQLEXPR2008;DATABASE=JobDB_test;Trusted_Connection=yes;') #TODO Change JobDB_test
    cursor = conn.cursor()
    return engine, conn, cursor

def create_JobDB_connection():
    """Used in connection to JobDB database.  This is the connection to
    the database specifeid by the user, and the job database.  User the standard
    global outputs "conn" (pyodbc) and "engine" (sqlalchemy) to execute sql
    querys or manipulate data with pandas
    
    return engine, conn, cursor"""

    engine = sqlalchemy.create_engine('mssql+pyodbc://.\DT_SQLEXPR2008/JobDB?driver=SQL+Server+Native+Client+10.0')
    engine.connect()
    
    conn = pyodbc.connect('DRIVER={SQL Server Native CLient 10.0};SERVER=.\DT_SQLEXPR2008;DATABASE=JobDB;Trusted_Connection=yes;') 
    cursor = conn.cursor()
    return engine, conn, cursor

def attach(pathMDF, connMaster, cursorMaster):
    """Used to attach PBJobDB. Note: The database added
    will have the default name PBJobDB to distinguish it from any databases.
    
    path = user specified path to .MDF file. LDF file must be in same directory.
    Assumed names are JobDB.mdf and JobDB_Log.ldf
    """
    if check_db_exist('JobDB_test', cursorMaster):
        print('Database name: {} is already connected'.format('JobDB_test')) #
        return
    
#        server = '.\DT_SQLEXPR2008' #may need to have this be a user-entered value for computer name
#        scriptLocation = 'C:\SQLTest\AttachDatabase.sql' #may need o be dynamically defined w/ os.getcwd()
#        subprocess.call(['sqlcmd','-S',server,'-i',scriptLocation])
    dirPathIndex = pathMDF.find('JobDB_test.mdf')
    dirPath = pathMDF[0:dirPathIndex]
    pathLDF = dirPath + 'JobDB_test_Log.ldf'
            
    sql1 = "CREATE DATABASE JobDB_test"
    sql2 = "ON (Filename = '{pathMDF}'), (Filename = '{pathLDF}')".format(pathMDF = pathMDF, pathLDF = pathLDF)
    sql3 = "FOR Attach"
    sql = sql1 + " " + sql2 + " " + sql3

    connMaster.autocommit = True
    cursorMaster.execute(sql)
    connMaster.autocommit = False
    print('Database connected')
    
def main():
    global cursorMaster, connMaster, engine, conn, cursor
    pathMDF = r'C:\SQLTest\ChangePointsAddress\JobDB_test.mdf'
    cursorMaster, connMaster = create_master_connection()
    attach(pathMDF)
    engine, conn, cursor = create_JobDB_test_connection()
    
def change_value(myString, dbName, newValue, cursor, engine, tableName='POINTFUN'):
    """Change POINT address in [LAN, DROP, POINT] where the database
    point name contains a certain string 'myString'.
    ex. usage: change all points with .CCV in a job to point 17 on the controller they
    are assigned to
    parameters
    ----------
    myString : identifier string (ex CCV)
    dbName : database name (JobDB)
    tableName : table name, default is POINTFUN
    newValue : new POINT address (int)
    cursor : pyodbc cursor object"""
    if not(type(newValue) == int):
        print('only int data types are valid for newValue')
        raise ValueError
    global pointidList
    pointidList = []
    global pointbas, pointfun
    pointbas = pd.read_sql_table('POINTBAS', engine)
    pointfun = pd.read_sql_table('POINTFUN', engine)
    for index, name in enumerate(pointbas['NAME']):
        if name.__contains__(myString):
            pointidList.append(pointbas.loc[index, 'POINTID'])
            print('Name: {} | ID: {}'.format(name, pointbas.loc[index, 'POINTID']))
           
    sql = """UPDATE [JobDB_test].[dbo].[POINTFUN] 
    SET [POINT] = ? 
    WHERE [POINTID] = ?"""
    for pointid in pointidList:
        cursor.execute(sql, (str(newValue), pointid)) #TODO Change JobDB_test
        cursor.commit()
    
def change_value2(myString, dbName, newValue, cursor, engine, tableName='POINTFUN'):
    """Change POINT address in [LAN, DROP, POINT] where the database
    point name contains a certain string 'myString'.
    ex. usage: change all points with .CCV in a job to point 17 on the controller they
    are assigned to
    parameters
    ----------
    myString : identifier string (ex CCV)
    dbName : database name (JobDB)
    tableName : table name, default is POINTFUN
    newValue : new POINT address (int)
    cursor : pyodbc cursor object"""
    if not(type(newValue) == int):
        print('only int data types are valid for newValue')
        raise ValueError
    global pointidList
    pointidList = []
    global pointbas, pointfun
    pointbas = pd.read_sql_table('POINTBAS', engine)
    pointfun = pd.read_sql_table('POINTFUN', engine)
    for index, name in enumerate(pointbas['NAME']):
        if name.__contains__(myString):
            pointidList.append(pointbas.loc[index, 'POINTID'])
            print('Name: {} | ID: {}'.format(name, pointbas.loc[index, 'POINTID']))
           
    sql = """UPDATE [JobDB].[dbo].[POINTFUN] 
    SET [POINT] = ? 
    WHERE [POINTID] = ?"""
    for pointid in pointidList:
        cursor.execute(sql, (str(newValue), pointid)) #TODO Change JobDB_test
        cursor.commit()
    
#pathMDF = r'C:\SQLTest\ChangePointsAddress\JobDB_test.mdf'
#cursorMaster, connMaster = create_master_connection()
#attach(pathMDF, connMaster, cursorMaster)
#engine, conn, cursor = create_JobDB_test_connection()
#myString = 'SAF-DP'
#dbName = 'JobDB_test'
#newValue = 6
#change_value(myString, dbName, newValue, cursor, engine)

def test():
    pathMDF = r'C:\SQLTest\ChangePointsAddress\JobDB_test.mdf' #TODO Change JobDB_test
#    cursorMaster, connMaster = create_master_connection() #TODO dont call this
#    attach(pathMDF, connMaster, cursorMaster) #TODO Change JobDB_test (or dont connect)
#    engine, conn, cursor = create_JobDB_test_connection()
    engine, conn, cursor = create_JobDB_connection()
    myString = 'SAF-DP'
    dbName = 'JobDB' #TODO Change JobDB_test
    newValue = 6
    change_value(myString, dbName, newValue, cursor, engine)

myDict = {'CCV':1, 'CCV-FB':2, 'CCT':3, 'MAT':4, 'FIL':5, 'SAF-DP':6, 
          'SSP-1':7, 'SSP-2':8, 'SAF-EA':9, 'SAF-WA':9, 'SAF-NA':9,
          'SAF-EB':10, 'SAF-WB':10, 'SAF-NB':10, 'SAF-EC':11, 'SAF-WC':11,
          'SAF-ED':12, 'SAF-WD':12, 'SVD1':13, 'SVD1-FB':14, 'SVD2':15, 'SVD2-FB':16,
          'SVF1':17, 'SVF2':18, '.RAH':19, '.FA':25, '.HSP':26, '.WD':27,
          '.SAF1':29, '.SAF2':30}

def test2(myString, newValue): #use for actually changing main database
    """parameters
    -------
    myString : point name string you wish to change (ex CCV)
    newValue : new POINT address (int)"""
    
    engine, conn, cursor = create_JobDB_connection()
    dbName = 'JobDB'
    newValue = newValue
    change_value2(myString, dbName, newValue, cursor, engine) 

#for label in myDict:
#    test2(label, myDict[label])




