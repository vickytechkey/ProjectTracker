from db.DataBase import MasterDatabase
import sqlite3

class SqliteDB(MasterDatabase):
    
    def __init__(self,DBName):
        self.DBName = DBName
    
    def CreateConnection(self):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        return cursor
    
    def CreateDB(self):
        cursor = self.CreateConnection()
        if not cursor:
            raise KeyError("SQLITE DB connection error")
        return True
    
    def Connection(self):
        conn = self.CreateConnection()
        return conn
    
    def CreateTable(self):
        create_table_sql_path = "./db/sql/CreateTable.sql"
        with open(create_table_sql_path,"r+") as f:
            create_table_sql = f.read()
        conn = self.CreateConnection()
        conn.execute(create_table_sql)
        print(conn)
        
    
    def QueryExecution(self,query):
        pass
    
    def SelectQuery(self,query):
        pass