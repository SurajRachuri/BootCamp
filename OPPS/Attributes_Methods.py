class car:
    def __init__(self,brand,color):
        self.brand=brand
        self.color=color
    def show(self):
        print(self.brand,self.color) 
        
class bike:
    def __init__(self,model):
        self.model=model
    def show(self):
        print(self.model)    
        
        
def test():
    print("hello world!")        
        