from DataFields.DataField import IntegerType,PositiveInteger,StringField,DateField,ProjectStatus
from db.sqlitedb import SqliteDB
from DataFields.generic_values import GenericValue
class CreateProject:
    projectName = StringField()
    project_start_end_date = DateField()
    plannedEfforts = PositiveInteger()
    spendEfforts = PositiveInteger()
    projectStatus = ProjectStatus()
    db_connection = SqliteDB(GenericValue.project_tracker_db)
    
    def __init__(self,projectName,project_start_end_date,plannedEfforts,spendEfforts):
        self.projectName = projectName
        self.project_start_end_date = project_start_end_date
        self.plannedEfforts = plannedEfforts
        self.spendEfforts = spendEfforts
        self.projectStatus = "NOT_STARTED"
    
    def CreateProject(self):
        insert_sql = '''
        
        '''
        
        