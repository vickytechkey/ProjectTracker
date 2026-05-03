from DataFields.DataField import StringField
import json

class GenericValue:
    project_tracker_db = "projecttracker.db"
    project_folder = "./projects/"


class FileCreator:
    Filename  = StringField()
    def __init__(self,filename,content):
        self.Filename = filename
        self.content = content
    
    def CreateFile(self):
        with open(self.Filename,"w+",encoding="utf-8") as f:
            json.dump(self.content,f,indent=4)
        print(self.Filename)