import  math
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def say(self):
        print ("Hi :)")

    def set_age(self, age):
        self.age=age

    def set_name(self,name):
        self.name=name

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def __str__(self):
        return "Person %s is  %d years old" %(self.name,self.age)

class Student(Person):
    def __init__(self,grade_avg,name="John",age=17):
        Person.__init__(self,name,age)
        self.__avg_grade=grade_avg

    def set_grades(self,grades):
        self.__avg_grade=grades

    def __str__(self):
        return "Student %s is %d years old and has a grade average of %d" %(self.name,self.age,self.__avg_grade)


class BigThing:
    def __init__(self, par):
        self.par=par

    def size(self):
        if type(self.par) == int or type(self.par) == float:
            return self.par
        else:
            return len(self.par)

class BigCat(BigThing):
    def __init__(self, parm):
        super().__init__(parm)
    def size(self):
        if super().size()>20:
            return "VeryFat"
        elif super().size()>15:
            return "Fat"
        else:
            return "OK"
b =BigCat(7)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_point(self):
        return (self.x, self.y)

class Circle:
    def __init__(self, p, radius):
        self.center = p
        self.radius = radius

    def get_area(self):
        return self.radius ** 2 * math.pi

    def get_circle_perimeter(self):
        return 2 * self.radius *  math.pi

    def __str__(self):
        return "Circle - \n Center:" + str(self.center.get_point()) +"\n Radius:" + str(self.radius)


class Cylinder(Circle):
    def __init__(self, p, radius, height):
        super().__init__(p, radius)
        self.height = height

    def get_cylinder_area(self):
        return 2 * math.pi * self.radius * self.height + 2 * math.pi * self.radius ** 2
    def get_cylinder_volume(self):
        return super().get_area()* self.height

p =Point(1,3)

c = Cylinder(p,3,7)
print(c.get_cylinder_volume())


