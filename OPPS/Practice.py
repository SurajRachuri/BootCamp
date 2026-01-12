# class Car:
#     wheels = 4  # class attribute

# c1 = Car()
# c2 = Car()
# print(c1.wheels, c2.wheels)

# class Car:
#     def __init__(self, color):
#         self.color = color  # instance attribute
# c=Car("red")
# print(c.color)

# class Person:
#     def __init__(self, name):
#         self.name = name

#     def greet(self):
#         return f"Hello, I am {self.name}"
# p=Person("suraj")
# print(p.greet())

# class Animal:
#     def speak(self,name: str):
#         self.name=name
#         return "Some sound"+self.name
    

# class Dog(Animal):
#     def speake(self):
#         return super().speak(self.name) + " + Woof"
# a = Animal()
# d = Dog()

# print(a.speak("Suraj"))   # Output: Some sound
# print(d.speake())   # Output: Some sound + Woof


class car:
    def __init__(self,car,colour):
        self.car=car
        self.colour=colour
    def Final(self):
        return f"car: {self.car} , colour:{self.colour}"    
d=car("bmw","red")
print(d.Final())    
class Car:
    def __init__(self, car, colour):
        self.car = car
        self.colour = colour

    def Final(self):
        return f"car: {self.car}, colour: {self.colour}"


d = Car("bmw", "red")
print(d.Final())

        
