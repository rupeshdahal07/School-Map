class Student:
    def __init__(self, name, roll, section):
        self.name = name
        self.roll = roll
        self.section = section


    def getname(self):
        return self.name

      
    def setname(self, name):
        self.name = name

    def getRoll(self):
        return self.roll
    
    def getRoll(self):
        return self.roll
    
    def setRoll(self, roll):
        self.roll = roll

    def getSection(self):
        return self.section
    
    def setSection(self, roll):
        self.roll = roll

   

    def printALL(self):
        print("Name: "+ self.name)
        print("Roll:"+ str(self.roll))
        print("Section:"+ self.section)


# obj1 = Student("rupesh", 1, "A")
# name= obj1.getname()
# obj1.printALL()
# print(name)

class Section(Student):
    def __init_subclass__(cls):
        return super().__init_subclass__()

        


       
obj2 = Section(name="Rupesh",roll=1, section="A")
obj2.printALL()
