# Author: Alan

#model层

from  lib import common
class OldboyBaseClass:

    @classmethod
    def get_obj(cls,name):
        return common.query_obj(cls.__name__,name)

    def save(self):
        common.save_obj(self)

class Admin(OldboyBaseClass):
    def __init__(self,name,pwd):
        self.name=name
        self.pwd=pwd
        self.save()
    def create_campus(self,campus_name):
        Campus(campus_name)
    def create_course(self,campus_name,course_name,course_price,course_period):
        Course(campus_name,course_name,course_price,course_period)
    def create_teacher(self,campus_name,name,pwd):
        Teacher(campus_name,name,pwd)
    def create_classes(self,campus_name,teacher_name,course_name,classes_name):
        Classes(campus_name,teacher_name,course_name,classes_name)

class Teacher(OldboyBaseClass):
    def __init__(self,campus_name,name,pwd):
        self.campus_name=campus_name
        self.name=name
        self.pwd=pwd
        self.classes_list=[]
        self.save()
    def add_classes(self,classes_name):
        self.classes_list.append(classes_name)
        self.save()

class Student(OldboyBaseClass):
    def __init__(self,name,pwd):
        self.name=name
        self.pwd=pwd
        self.classes_list=[]
        self.grade={}
        self.cost={}
        self.save()
    def update_grade(self,classes_name,new_score):
        self.grade[classes_name]=new_score
        self.save()

    def pay_to(self,classes_name,num):
        if self.cost[classes_name]==0:
            return True
        else:self.cost[classes_name]-=num

        if self.cost[classes_name] == 0:
            self.save()
            return True
        else:
            return False

    def choose_classes(self,classes_name,classes_price):
        if classes_name not in self.classes_list:
            self.classes_list.append(classes_name)
            self.grade[classes_name]=0
            self.cost[classes_name]=classes_price
            self.save()
            return True
        return False


class Campus(OldboyBaseClass):
    def __init__(self,name):
        self.name=name
        self.classes_list=[]
        self.teacher_list=[]
        self.course_list=[]
        self.save()

class Course(OldboyBaseClass):
    def __init__(self,campus_name,name,price,period):
        self.campus_name=campus_name
        self.name=name
        self.price=price
        self.period=period
        self.save()

class Classes(OldboyBaseClass):
    def __init__(self,campus_name,teacher_name,course_name,name):
        self.name=name
        self.campus_name=campus_name
        self.teacher_name=teacher_name
        self.course_name=course_name
        self.student_list=[]
        self.save()

    def add_student(self,student_name):
        self.student_list.append(student_name)
        self.save()
