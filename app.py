from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host='localhost', user='root', password='',port=3307, database='student_result_db'
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch Students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Fetch Subjects
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    # Fetch Marks with student and subject names using JOIN
    cursor.execute("""
        SELECT marks.id, marks.score, marks.student_id, marks.subject_id,
               students.name AS student_name, subjects.name AS subject_name
        FROM marks
        JOIN students ON marks.student_id = students.id
        JOIN subjects ON marks.subject_id = subjects.id
    """)
    marks = cursor.fetchall()

    conn.close()
    return render_template("index.html", students=students, subjects=subjects, marks=marks)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name,email,attendance) VALUES (%s,%s,%s)",
                (data['name'], data['email'], data['attendance']))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/edit_student', methods=['POST'])
def edit_student():
    data = request.form
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE students SET name=%s,email=%s,attendance=%s WHERE id=%s",
                (data['name'], data['email'], data['attendance'], data['id']))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (request.form['id'],))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/add_subject', methods=['POST'])
def add_subject():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO subjects (name) VALUES (%s)", (request.form['name'],))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/edit_subject', methods=['POST'])
def edit_subject():
    data = request.form
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE subjects SET name=%s WHERE id=%s", (data['name'], data['id']))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/delete_subject', methods=['POST'])
def delete_subject():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE id=%s", (request.form['id'],))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/add_mark', methods=['POST'])
def add_mark():
    d = request.form
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO marks (student_id,subject_id,score) VALUES (%s,%s,%s)",
                (d['student_id'], d['subject_id'], d['score']))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/edit_mark', methods=['POST'])
def edit_mark():
    d = request.form
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE marks SET student_id=%s,subject_id=%s,score=%s WHERE id=%s",
                (d['student_id'], d['subject_id'], d['score'], d['id']))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/delete_mark', methods=['POST'])
def delete_mark():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM marks WHERE id=%s", (request.form['id'],))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
