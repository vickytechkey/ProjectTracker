from DataFields.DataField import IntegerType,PositiveInteger,StringField,DateField,ProjectStatus
from db.sqlitedb import SqliteDB
from generic.generic_values import GenericValue
import json
from generic.file_create import FileCreator

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
        json_file_path = f""
        start_date = self.project_start_end_date["start_date"]
        end_date = self.project_start_end_date["end_date"]
        insert_sql = f'''
        INSERT INTO PROJECTS (PROJECT_NAME,PROJECT_START_DATE,PROJECT_END_DATE,PLANNED_EFFORTS,SPENDED_EFFORTS) 
        VALUES ('{self.projectName}','{start_date}','{end_date}',{self.plannedEfforts},{self.spendEfforts})
        '''
        with open("./projectManagement/projects/project_template.json") as f:
            project_template = json.load(f)
        file_path = f"./projectManagement/projects/{self.projectName}.json"
        project_template["project_name"] = self.projectName
        project_template["start_date"] = start_date
        project_template["end_date"] = end_date
        f = FileCreator(file_path,project_template)
        f.CreateFile()
        self.db_connection.QueryExecution(insert_sql)
        return True
        
        
        