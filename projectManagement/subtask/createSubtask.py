from datetime import date
from DataFields.DataField import StringField,DateField,PositiveInteger,IntegerType
from generic.generic_values import JsonFileCreater
from db.mongo import MongoDB


class CreateSubTask:
    subTaskname = StringField()
    start_enddate = DateField()
    creationDate = date.today()
    planned_efforts = PositiveInteger()
    subtask_id = PositiveInteger()
    project_id = PositiveInteger()
    def __init__(self,taskname,start_date,end_date,planned_efforts,project_name):
        self.subTaskname = taskname
        self.start_enddate = {
            "start_date":start_date,
            "end_date":end_date
        }
        self.planned_efforts = planned_efforts
        self.project_name = project_name
    
    def CreateSubTask(self):
        subtask_template = JsonFileCreater("./projectManagement/subtask/subtask_template.json","")
        subtask_template = subtask_template.ReadFile()
        subtask_template["project_name"] = self.project_name
        subtask_template["subTask_name"] = self.subTaskname
        subtask_template["creationDate"] = self.creationDate.strftime("%d-%m-%Y")
        subtask_template["start_date"] = self.start_enddate["start_date"]
        subtask_template["end_date"] = self.start_enddate["end_date"]
        subtask_template["planned_efforts"] = self.planned_efforts
        db_connection = MongoDB(collectionname="subtasks",insertdata=subtask_template)
        db_connection.insertData()
        

        
        