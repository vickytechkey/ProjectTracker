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
    
    def __init__(self,projectName,project_start_end_date,plannedEfforts,spendEfforts=0):
        self.projectName = projectName
        self.project_start_end_date = project_start_end_date
        self.plannedEfforts = plannedEfforts
        self.spendEfforts = spendEfforts
        self.projectStatus = "NOT_STARTED"
    
    def CreateProject(self):
        start_date = self.project_start_end_date["start_date"]
        end_date = self.project_start_end_date["end_date"]
        insert_sql = f'''
        INSERT INTO PROJECTS (PROJECT_NAME,PROJECT_START_DATE,PROJECT_END_DATE,PLANNED_EFFORTS,SPENDED_EFFORTS) 
        VALUES ('{self.projectName}','{start_date}','{end_date}',{self.plannedEfforts},{self.spendEfforts})
        '''
        self.db_connection.QueryExecution(insert_sql)
        
        