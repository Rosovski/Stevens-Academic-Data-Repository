from collections import defaultdict
from prettytable import PrettyTable
from HW08_Zhonghua_Bao import file_reader
import os

class Repository:
    """define a class which contains all the information of the student, instructor, grade from one directory
       read these three texts and make a summary about each student and instructor
    """
    def __init__(self,path,ptables=True):
        self._students = dict()
        self._instructors = dict()
        self._path = path

        self._get_students(os.path.join(path,'students.txt'))
        self._get_instructors(os.path.join(path,'instructors.txt'))
        self._get_grades(os.path.join(path,'grades.txt'))

        if ptables:
            print('\nStudent Summary')
            self.student_summary()

            print('\nInstructor Summary')
            self.instructor_summary()
    
    def _get_students(self,path):
        try:
            for cwid,name,major in file_reader(path,3,sep='\t',header=False):
                if not cwid.isdigit():
                    raise ValueError("STUDENTS: Incorrect Student CWID: " + cwid)
            
                if cwid in self._students.keys():
                    raise ValueError("STUDENTS: Duplicated Student CWID: " + cwid)
                
                self._students[cwid] = Student(cwid,name,major)
                
        except ValueError as e:
            print(e)
    
    def _get_instructors(self,path):
        try:
            for cwid,name,dept in file_reader(path,3,sep='\t',header=False):
                if not cwid.isdigit():
                    raise ValueError("INSTRUCTORS: Incorrect Instructor CWID: " + cwid)
            
                if cwid in self._instructors.keys():
                    raise ValueError("INSTRUCTORS: Duplicated Instructor CWID: " + cwid)
                
                self._instructors[cwid] = Instructor(cwid,name,dept)

        except ValueError as e:
            print(e)
    
    def _get_grades(self,path):
        try:
            for student_cwid,course,grade,insrtuctor_cwid in file_reader(path,4,sep='\t',header=False):
                if student_cwid in self._students.keys():
                    if course in self._students[student_cwid]._course.keys():
                        raise ValueError("GRADES: Duplicated grade: " + str(course))
                    else:
                        self._students[student_cwid].add_course(course,grade)
                else:
                    print("Found grade for unknown student {}".format(student_cwid))
                
                if insrtuctor_cwid in self._instructors.keys():
                    self._instructors[insrtuctor_cwid].add_student(course)
                else:
                    print("Found grade for unknown instructor {}".format(insrtuctor_cwid))
        
        except ValueError as e:
            print(e)
    
    def student_summary(self):
        """use prettytable to print every student's information"""
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Completed Courses"]

        for student in sorted(self._students.values(), key=lambda student: student._cwid):
            table.add_row(student.pt_row())

        print(table)
    
    def instructor_summary(self):
        """use prettytable to print every instructor's information"""
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Dept", "Course", "Students"]

        for instructor in sorted(self._instructors.values(), key=lambda ins: ins._cwid):
            for row in instructor.pt_row():
                table.add_row(row)
        
        print(table)


class Student:
    """store student's information, contain a method which declares itself
    """
    def __init__(self,cwid,name,major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._course = defaultdict(str)
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._major, " ".join(self._course.keys())])
    
    def add_course(self,course,grade):
        self._course[course] = grade
    
    def pt_row(self):
        return self._cwid, self._name, sorted([name for name in self._course.keys()])

class Instructor:
    """store instructor's information, contain a function which declares itself
    """
    def __init__(self,cwid,name,major):
        self._cwid = cwid
        self._name = name
        self._dept = major
        self._course = defaultdict(int)
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._dept, " ".join(self._course.keys())])

    def add_student(self,course):
        self._course[course] += 1
    
    def pt_row(self):
        course_list = list()
        for course in self._course.keys():
            row = (self._cwid, self._name, self._dept, course, self._course[course])
            course_list.append(row)
        
        return course_list

def run():
    repo = Repository("./stevens")

if __name__ == "__main__":
    run()
