import json
from datetime import date
from DataFields.DataField import StringField,DateField,PositiveInteger,IntegerType
from generic.generic_values import GenericValue


class CreateSubTask:
    subTaskname = StringField()
    start_enddate = DateField()
    creationDate = date.today()
    planned_efforts = PositiveInteger()
    subtask_id = PositiveInteger()
    def __init__(self,taskname,start_date,end_date,planned_efforts,subtask_id):
        self.subTaskname = taskname
        self.start_enddate = {
            "start_date":start_date,
            "end_date":end_date
        }
        self.planned_efforts = planned_efforts
        self.subtask_id = subtask_id
    
    def CreateSubTask(self):
        with open("./projectManagement/subtask/subtask_template.json","r+") as f:
            subtask_template = json.load(f)
        
        subtask_template["subTask_name"] = self.subTaskname
        subtask_template["subTask_id"] = self.subtask_id
        subtask_template["creationDate"] = self.creationDate.strftime("%d-%m-%Y")
        subtask_template["start_date"] = self.start_enddate["start_date"]
        subtask_template["end_date"] = self.start_enddate["end_date"]
        subtask_template["planned_efforts"] = self.planned_efforts
        
        task_path = GenericValue.task_path + self.subTaskname + ".json"
        
        with open(task_path , "w+") as f :
            json.dump(subtask_template, f, indent=4)