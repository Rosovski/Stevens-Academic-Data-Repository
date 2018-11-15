import sqlite3
from prettytable import PrettyTable

DB_FILE = r"C:\Users\ei_fr\Desktop\810_startup.db"
db = sqlite3.connect(DB_FILE)

query = """select i.CWID,i.Name,i.Dept,g.Course,count(g.Student_CWID) as Students
            from HW11_instructors as i
            join HW11_grades as g on g.Instructor_CWID = i.CWID group by g.Course"""
table = PrettyTable()
table.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
for row in db.execute(query):
    table.add_row(row)

print(table)

db.close()
