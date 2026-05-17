from DataFields.DataField import IntegerType,PositiveInteger,StringField,DateField,ProjectStatus
from db.mongo import MongoDB
import json


class CreateProject:
    projectName = StringField()
    project_start_end_date = DateField()
    plannedEfforts = PositiveInteger()
    spendEfforts = PositiveInteger()
    projectStatus = ProjectStatus()
    
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
        with open("./projectManagement/projects/project_template.json") as f:
            project_template = json.load(f)
        project_template["project_name"] = self.projectName
        project_template["start_date"] = start_date
        project_template["end_date"] = end_date
        db_connection = MongoDB(collectionname="Projects",insertdata=project_template)
        db_connection.insertData()
        return True
        
        
        
        