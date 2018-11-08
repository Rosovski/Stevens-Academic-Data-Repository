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
        self._majors =dict()
        self._path = path

        self._get_students(os.path.join(path,'students.txt'))
        self._get_instructors(os.path.join(path,'instructors.txt'))
        self._get_grades(os.path.join(path,'grades.txt'))
        self._get_majors(os.path.join(path,'majors.txt'))
        
        if ptables:
            
            print('\nMajor Summary')
            self.major_summary()
            
            print('\nStudent Summary')
            self.student_summary()
            
            print('\nInstructor Summary')
            self.instructor_summary()
            
    def _get_students(self,path):
        """read the student file, get the information from the text,
           generate the student object using the given info
        """
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
        """read the instructor file, get the information from the text,
           generate the instructor object using the given info
        """
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
        """read the grade text, get the info about which courses student registers and the course about the grade,
           get the info about which courses instructor teaches and how many students have this class
        """
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
        
    def _get_majors(self,path):
        """read the major file, get the information from the text,
           generate the major object using the given info
        """
        try:
            for dept,tag,course in file_reader(path,3,sep='\t',header='True'):
                if dept not in self._majors.keys():
                    self._majors[dept] = Major(dept)
                
                self._majors[dept].add_course(tag,course)
                
        except ValueError as e:
            print(e)
    
    def student_summary(self):
        """use prettytable to print every student's information"""
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Major", "Completed Courses","Remainging Required","Remaining Elective"]

        test_ = list()

        for student in sorted(self._students.values(), key=lambda student: student._cwid):
            completed_courses = sorted(set(student._course.keys()))
            pass_courses = {course for course, grade in student._course.items() if grade in self._majors[student._major]._pass_grades}
            rem_required = sorted(self._majors[student._major]._required - pass_courses)
            if self._majors[student._major]._elective.intersection(pass_courses):
                rem_elective = None
            else:
                rem_elective = sorted(self._majors[student._major]._elective)

            row = student._cwid, student._name, student._major,completed_courses,rem_required,rem_elective
            test_.append(row)
            table.add_row(row)

        print(table)
        
        return test_

    def instructor_summary(self):
        """use prettytable to print every instructor's information"""
        table = PrettyTable()
        table.field_names = ["CWID", "Name", "Dept", "Course", "Students"]

        for instructor in sorted(self._instructors.values(), key=lambda ins: ins._cwid):
            for row in instructor.pt_row():
                table.add_row(row)
        
        print(table)
    
    def major_summary(self):
        """use prettytable to print every major's information"""
        table = PrettyTable()
        table.field_names = ["Dept","Required","Elective"]

        test_ = list()
        for major in sorted(self._majors.values(), key=lambda major: major._dept):
            table.add_row(major.pt_row())
            test_.append(major.pt_row())
        
        print(table)

        return test_


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
        completed_courses, rem_required, rem_electives = self._major.grade_check(self._course)
        return [self._cwid, self._name, self._major, completed_courses, rem_required, rem_electives]  # using sort to sort the courses and their respective keys
    
    #def pt_row(self):
        #return self._cwid, self._name, self._major,sorted([name for name in self._course.keys()])

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

class Major:
    def __init__(self,dept):
        self._dept = dept
        self._required = set()
        self._elective = set()
        self._pass_grades = {'A', 'A-', 'B+', 'B','B-', 'C+', 'C'}
    
    def add_course(self,tag,course):
        if tag == 'R':
            self._required.add(course)
        elif tag == 'E':
            self._elective.add(course)
        else:
            raise ValueError("Tag {} is invalid for course {}".format(tag,course))
    """
    def grade_check(self, courses):
        completed_courses = {course for course, grade in courses.items() if grade in self._pass_grades}
        rem_required = self._required - completed_courses
        if self._elective.intersection(completed_courses):
            rem_electives = None
        else:
            rem_electives = self._elective

        return completed_courses, rem_required, rem_electives
    """ 
    def pt_row(self):
        return self._dept,sorted(list(self._required)),sorted(list(self._elective))

def run():
    repo = Repository("./stevens")
    

if __name__ == "__main__":
    run()