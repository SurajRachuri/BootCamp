from datetime import datetime 
class Names:
    def __init__(self,name,age):
        self.name=name
        self.age=age
        
    def Show_age(self,date=None):   
        print(f"hi {self.name} you age is {self.age} and date ")
        
nam=Names("manas","23")
now = datetime.now() 
nam.Show_age(now) 
        
        

        
    