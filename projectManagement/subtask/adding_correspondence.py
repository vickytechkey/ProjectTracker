from datetime import date
from DataFields.DataField import StringField,PositiveInteger
from generic.generic_values import GenericValue,JsonFileCreater
from db.mongo import MongoDB

class AddingMessage:
    project_name = StringField()
    subtaskname = StringField()
    creation_date = date.today()
    message = StringField()
    
    def __init__(self,projectname,subtaskname,message,user="User"):
        self.project_name = projectname
        self.subtaskname = subtaskname
        self.message = message
        self.user = user
    
    def createcorrespondence(self):
        templatejson = "./projectManagement/subtask/correspondence_template.json"
        correspondence_template = JsonFileCreater(templatejson,"").ReadFile()
        correspondence_template["correspondence_date"] = self.creation_date.strftime("%d-%m-%Y")
        correspondence_template["message"] = self.message
        correspondence_template["subtask_name"] = self.subtaskname
        correspondence_template["project_name"] = self.project_name
        correspondence_template["user"] = self.user
        db_connection = MongoDB(collectionname="correspondence",insertdata=correspondence_template)
        db_connection.insertData()
        
        
        
        
        
        
        
        
    