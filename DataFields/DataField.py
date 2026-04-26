class StringField:
    def __set_name__(self,owner,name):
        self.private_name = "_" + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance,self.private_name,None)
    
    def __set__(self, instance, value):
        if not instance(value,str):
            raise ValueError("value Must be string")
        if len(value.strip())==0:
            raise ValueError("string must not be empty")
        
        setattr(instance,self.private_name,value)



            
        