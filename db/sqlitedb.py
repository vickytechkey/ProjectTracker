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
    
    def Connection(self, query):
        pass
    
    def CreateTable(self,query):
        pass
    
    def QueryExecution(self,query):
        pass
    
    def SelectQuery(self,query):
        pass