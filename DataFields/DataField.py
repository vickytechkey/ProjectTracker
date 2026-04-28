from datetime import datetime

class StringField:
    def __set_name__(self,owner,name):
        self.private_name = "_" + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance,self.private_name,None)
    
    def validate_string(self,value):
        if not isinstance(value,str):
            raise ValueError("value Must be string")
        if len(value.strip())==0:
            raise ValueError("string must not be empty")
    def __set__(self, instance, value):
       self.validate_string(value)
       setattr(instance,self.private_name,value)


class IntegerType:
    def __set_name__(self,owner,name):
        self.private_name = "_" + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        return getattr(instance,self.private_name,None)
    
    def validate_integer(self,value):
            if not isinstance(value,int):
               raise ValueError("Data should be Integer")
        
    
    def __set__(self, instance, value):
        self.validate_integer(value)
        setattr(instance,self.private_name,value)


class PositiveInteger(IntegerType):
    def validate_integer(self,value):
        super().validate_integer(value)
        
        if value < 0:
            raise ValueError("Value must be greater than zero")

class NegativeInteger(IntegerType):
    def validate_integer(self, value):
         super().validate_integer(value)
         if value >= 0 :
             raise ValueError("Value must be less than zero")


class ProjectStatus(StringField):
    def validate_string(self, value):
        super().validate_string(value)
        if value not in ["started","inprogress","blocked","review","done"]:
            raise ValueError("Invalid project status")


class DateField:
    def __set_name__(self,owner,name):
        self.private_name = "_" + name
    
    def __get__(self,instance,owner):
        if instance is None:
            return self
        return getattr(instance,self.private_name,None)
    
    def validate_date(self,date):
        try:
            parsed_date = datetime.strptime(date,"%d-%m-%Y")
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format")
    
    
    def validate_start_end_date(self,start_date,end_date):
        start_date = datetime.strptime(start_date , "%d-%m-%Y")
        end_date = datetime.strptime(end_date,"%d-%m-%Y")
        if start_date > end_date:
            raise ValueError("start date should not be greater than end date")
        
    
    def __set__(self, instance, value:dict):
       self.validate_date(value["start_date"])
       self.validate_date(value["end_date"])
       self.validate_start_end_date(value["start_date"],value["end_date"])
       setattr(instance,self.private_name,value)        