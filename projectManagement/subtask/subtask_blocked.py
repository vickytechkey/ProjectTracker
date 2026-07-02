from db.mongo import MongoDB
from DataFields.DataField import StringField

class BlockSubtask:
    project_name = StringField()
    subtask_name = StringField()
    
    def __init__(self,projectname,subtaskname):
        self.project_name = projectname
        self.subtask_name = subtaskname
    
    def checksubtask(self):
        db = MongoDB(collectionname="subtasks",findkey={"subTask_name":self.subtask_name,"project_name":self.project_name})
        res = db.findOne()
        return res is not None
    
    def block_task(self):
        check_project = self.checksubtask()
        if check_project:
          db = MongoDB(collectionname="subtasks",filterkey={"subTask_name":self.subtask_name,"project_name":self.project_name},updatekey={"status":"BLOCKED"})
          db.updateOne()
          return db
        return False
        
        
    