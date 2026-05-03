from datetime import date
from DataFields.DataField import StringField,DateField,PositiveInteger,IntegerType
from generic.generic_values import GenericValue,JsonFileCreater
from db.sqlitedb import SqliteDB


class CreateSubTask:
    subTaskname = StringField()
    start_enddate = DateField()
    creationDate = date.today()
    planned_efforts = PositiveInteger()
    subtask_id = PositiveInteger()
    project_id = PositiveInteger()
    db = SqliteDB(GenericValue.project_tracker_db)
    def __init__(self,taskname,start_date,end_date,planned_efforts,project_id):
        self.subTaskname = taskname
        self.start_enddate = {
            "start_date":start_date,
            "end_date":end_date
        }
        self.planned_efforts = planned_efforts
        self.project_id = project_id
    
    def CreateSubTask(self):
        # getting project name using the project id
        select_sql = f'''
        SELECT PROJECT_NAME FROM PROJECTS WHERE PROJECT_ID={self.project_id}
        '''
        result = self.db.SelectQuery(select_sql)
        project_name =  result[0][0]
        # Reading test project file
        project_file_name = f"./projects/{project_name}.json"
        project_file = JsonFileCreater(project_file_name,"")
        project_file = project_file.ReadFile()
        subtask_template = JsonFileCreater("./projectManagement/subtask/subtask_template.json","")
        subtask_template = subtask_template.ReadFile()
        
        subtask_template["subTask_name"] = self.subTaskname
        subtask_template["subTask_id"] = len(project_file["sub_tasks"])
        subtask_template["creationDate"] = self.creationDate.strftime("%d-%m-%Y")
        subtask_template["start_date"] = self.start_enddate["start_date"]
        subtask_template["end_date"] = self.start_enddate["end_date"]
        subtask_template["planned_efforts"] = self.planned_efforts
        # inserting the subtask in the project
        project_file["sub_tasks"].append(subtask_template)
        # editing the project file
        f1 = JsonFileCreater(project_file_name,project_file)
        f1.CreateFile()
        
        