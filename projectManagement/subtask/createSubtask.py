import json
from datetime import date
from DataFields.DataField import StringField,DateField,PositiveInteger,IntegerType
from generic.generic_values import GenericValue,FileCreator
from db.sqlitedb import SqliteDB


class CreateSubTask:
    subTaskname = StringField()
    start_enddate = DateField()
    creationDate = date.today()
    planned_efforts = PositiveInteger()
    subtask_id = PositiveInteger()
    project_id = PositiveInteger()
    db = SqliteDB(GenericValue.project_tracker_db)
    def __init__(self,taskname,start_date,end_date,planned_efforts,subtask_id,project_id):
        self.subTaskname = taskname
        self.start_enddate = {
            "start_date":start_date,
            "end_date":end_date
        }
        self.planned_efforts = planned_efforts
        self.subtask_id = subtask_id
        self.project_id = project_id
    
    def CreateSubTask(self):
        with open("./projectManagement/subtask/subtask_template.json","r+") as f:
            subtask_template = json.load(f)
        
        subtask_template["subTask_name"] = self.subTaskname
        subtask_template["subTask_id"] = self.subtask_id
        subtask_template["creationDate"] = self.creationDate.strftime("%d-%m-%Y")
        subtask_template["start_date"] = self.start_enddate["start_date"]
        subtask_template["end_date"] = self.start_enddate["end_date"]
        subtask_template["planned_efforts"] = self.planned_efforts
        
        # getting project name using the project id
        select_sql = f'''
        SELECT PROJECT_NAME FROM PROJECTS WHERE PROJECT_ID={self.project_id}
        '''
        result = self.db.SelectQuery(select_sql)
        project_name =  result[0][0]
        # Reading test project file
        project_file_name = f"./projects/{project_name}.json"
        print(project_file_name)
        with open(project_file_name,"r+") as f:
            project_file = json.load(f)
        # inserting the subtask in the project
        project_file["sub_tasks"].append(subtask_template)
        # editing the project file
        with open(project_file_name,"w+") as f:
            json.dump()
        
        