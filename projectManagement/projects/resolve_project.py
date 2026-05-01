from DataFields.DataField import IntegerType,PositiveInteger,StringField,DateField,ProjectStatus
from db.sqlitedb import SqliteDB
from DataFields.generic_values import GenericValue

class ResolveProject:
    projectId = PositiveInteger()
    
    
    def __init__(self,projectId):
        self.projectId = projectId
        self.db = SqliteDB(GenericValue.project_tracker_db)
    
    
    def CloseProject(self):
        query = f'''
        UPDATE PROJECTS SET STATUS='DONE' WHERE PROJECT_ID='{self.projectId}'
        '''
        affected_rows = self.db.QueryExecution(query)
        if affected_rows > 0:
            return f"project Resolved successfully"
        else:
            return "Project already resolved or it might be out of date"
    
        
        
        
        