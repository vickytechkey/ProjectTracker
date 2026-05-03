from datetime import date
from DataFields.DataField import StringField,PositiveInteger
from generic.generic_values import GenericValue,JsonFileCreater
from db.sqlitedb import SqliteDB

class AddingMessage:
    project_name = StringField()
    subtask_id = PositiveInteger()
    creation_date = date.today()
    message = StringField()
    
    def __init__(self,projectname,subtaskid,message):
        self.project_name = projectname
        self.subtask_id = subtaskid
        self.message = message
    
    def createcorrespondence(self):
        # Reading project file
        project_file = f"./projects/{self.project_name}.json"
        project_content = JsonFileCreater(project_file,"").ReadFile()
        # Reading subtasks correspondence
        print(type(project_content))
        print(project_content)
        templatejson = "./projectManagement/subtask/correspondence_template.json"
        correspondence_template = JsonFileCreater(templatejson,"").ReadFile()
        correspondence_template["correspondence_id"] = len(project_content["sub_tasks"][self.subtask_id]["correspondence"])
        correspondence_template["correspondence_date"] = self.creation_date.strftime("%d-%m-%Y")
        correspondence_template["message"] = self.message
        # correspondence = project_content["sub_tasks"][self.subtask_id]["correspondence"].append(correspondence_template)
        # print(project_content["sub_tasks"])
        # updating the project file
        # JsonFileCreater(project_file,correspondence).CreateFile()
        
        
        
        
        
        
        
        
    