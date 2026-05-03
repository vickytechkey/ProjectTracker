from generic.Jsonfile import JsonFunctions

class GenericValue:
    project_tracker_db = "projecttracker.db"
    project_folder = "./projects/"


class JsonFileCreater(JsonFunctions):
    
    def __init__(self, filename, content):
        super().__init__(filename, content)
