from db.mongo import MongoDB

class ResolveProject:
    
    
    def __init__(self,projectname):
        self.projectname = projectname
        self.connection = MongoDB(collectionname="Projects",findkey={"project_name":self.projectname},filterkey={"project_name":self.projectname},updatekey={"status":"RESOLVED"})

    def checkingprojectexists(self):
        res = self.connection.findOne()
        return res is not None
    
    def closeproject(self):
        project_count  = self.checkingprojectexists()
        if project_count:
            res = self.connection.updateOne()
            if res["modified_count"] > 0:
                return True
            else:
                return False
                
        
        
        
        
        
        
    
        
        
        
        