from DataFields.DataField import IntegerType,NegativeInteger


class Person:
    age = NegativeInteger()
    def __init__(self,age):
        self.age = age


p =  Person(-23)
print(p.age)

