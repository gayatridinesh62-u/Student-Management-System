from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_db"
)

cursor = db.cursor()

# Login Page
@app.route('/')
def login():
    return render_template("login.html")


# Login Check
@app.route('/login', methods=['POST'])
def check_login():

    username = request.form['username']
    password = request.form['password']

    sql = "SELECT * FROM admins WHERE username=%s AND password=%s"
    cursor.execute(sql,(username,password))

    result = cursor.fetchone()

    if result:
        return redirect('/dashboard')
    else:
        return "Invalid Login"


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# Add Student Page
@app.route('/add_student')
def add_student():
    return render_template("add_student.html")


# Save Student
@app.route('/save_student', methods=['POST'])
def save_student():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    address = request.form['address']

    sql = "INSERT INTO students (name,email,phone,course,address) VALUES (%s,%s,%s,%s,%s)"

    values = (name,email,phone,course,address)

    cursor.execute(sql,values)
    db.commit()

    return redirect('/view_student')


# View Students
@app.route('/view_student')
def view_student():

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    return render_template("view_student.html", students=data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
