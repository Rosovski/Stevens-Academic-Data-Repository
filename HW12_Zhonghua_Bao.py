import sqlite3
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome! please type in http://127.0.0.1.5000/student_courses"

@app.route('/student_courses')              
def student_courses():
    DB_FILE = r"C:\Users\ei_fr\Desktop\810_startup.db"
    db = sqlite3.connect(DB_FILE)
    
    query = """select s.CWID, s.Name, s.Major, count(g.Course) as Completed_courses
               from HW11_students as s 
               join HW11_grades as g on s.CWID = g.Student_CWID group by s.cwid, s.name, s.major"""
    
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    data = [{'cwid': cwid, 'name': name, 'major': major, 'complete': complete} for cwid, name, major, complete in results]
    db.close()
    
    return render_template('student_courses.html', title="Stevens Repository", table_title="Number of completed courses by student", students=data)

app.run(debug=True)