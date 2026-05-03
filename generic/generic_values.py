from DataFields.DataField import StringField
import json

class GenericValue:
    project_tracker_db = "projecttracker.db"
    project_folder = "./projects/"


class FileFunctions:
    Filename  = StringField()
    def __init__(self,filename,content):
        self.Filename = filename
        self.content = content
    
    def CreateFile(self):
        with open(self.Filename,"w+",encoding="utf-8") as f:
            json.dump(self.content,f,indent=4)
        print(f"created file {self.Filename}")
    
    def ReadFile(self):
        with open(self.Filename,"r+",encoding="utf-8") as f:
            content = json.load(f)
        return content