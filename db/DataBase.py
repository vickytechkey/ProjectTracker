from abc import ABC,abstractmethod

class MasterDatabase(ABC):
    
    @abstractmethod
    def CreateDB(self,dbname):
        pass
    
    @abstractmethod
    def Connection(self,query):
        pass
    
    @abstractmethod
    def CreateTable(self,query):
        pass
    
    @abstractmethod
    def QueryExecution(self,query):
        pass
    
    @abstractmethod
    def SelectQuery(self,query):
        pass


