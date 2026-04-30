from db.DataBase import MasterDatabase
import sqlite3

class SqliteDB(MasterDatabase):
    
    def __init__(self,DBName):
        self.DBName = DBName
    
    def CreateConnection(self):
        return sqlite3.connect(self.DBName)
    
    def CreateDB(self):
        cursor = self.CreateConnection()
        if not cursor:
            raise KeyError("SQLITE DB connection error")
        return True
    
    def Connection(self):
        pass
    
    def CreateTable(self):
        create_table_sql_path = "./db/sql/CreateTable.sql"
        with open(create_table_sql_path,"r+") as f:
            create_table_sql = f.read()
        conn = self.CreateConnection()
        cursor = conn.cursor()
        cursor.executescript(create_table_sql)
        conn.commit()
        conn.close()
        
    
    def QueryExecution(self,query):
        if len(query.strip())==0:
            raise ValueError("query should not be empty")
        conn = self.CreateConnection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    
    def SelectQuery(self,query):
        if len(query.strip())==0:
            raise ValueError("query should not be empty")
        conn = self.CreateConnection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows