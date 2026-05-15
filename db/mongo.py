from pymongo import MongoClient

class MongoDB:
    
    def __init__(self,collectionname,insertdata="",findkey="",filterkey="",updatekey=""):
        self.client = MongoClient("mongodb://127.0.0.1:27017/")
        self.db = self.client["projecttracker"]
        self.collectionname = collectionname
        self.insertdata = insertdata
        self.findkey = findkey
        self.filterkey = filterkey
        self.updatekey = updatekey
        
        
        
    def createCollection(self):
        self.db[self.collectionname]
        
    
    def insertData(self):
        collection = self.db[self.collectionname]
        collection.insert_one(self.insertdata)
        print("Data inserted")
    
    def findOne(self):
        collection = self.db[self.collectionname]
        res = collection.find_one(self.findkey)
        return res
    
    def findOne(self):
        collection = self.db[self.collectionname]
        res = collection.find(self.findkey)
        return res
        
    
    def updateOne(self):
        collection = self.db[self.collectionname]
        res = collection.update_one(self.filterkey,{
            "$set":self.updatekey
        })
        
        return {"modified_count":res.modified_count,"matched_count":res.matched_count}
        
    
    def deleteOne(self):
        collection = self.db[self.collectionname]
        collection.delete_one(self.filterkey)
        return True
    
    def deleteMany(self):
        collection = self.db[self.collectionname]
        collection.delete_many(self.filterkey)
        return True
        