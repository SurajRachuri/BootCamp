from Attributes_Methods import car,bike,test
class student:
    def __init__(self,name,age):
        self.name=name
        self.age=age
        

s1=student("suraj",21)
print(s1.name,s1.age)  
c=car("BMW","White")
c.show()
