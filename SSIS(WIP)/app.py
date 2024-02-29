from flask import Flask, request, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)

@app.route('/add_student', methods=['POST'])
def add_student():
    student_id = request.form['studentID']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    gender = request.form['gender']
    year = request.form['year']
    course = request.form['course']

    with open('students.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_id, first_name, last_name, gender, year, course])

    return 'Student added successfully!'  # Redirect to the homepage after adding course

@app.route('/add_course', methods=['POST'])
def add_course():
    course_code = request.form['courseCode']
    course_name = request.form['courseName']  # Ensure this matches the name in the HTML form
    college = request.form['college']

    with open('courses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([course_code, course_name, college])

    return 'Course added successfully!'  # Redirect to the homepage after adding course

@app.route('/')
def index():
    # Get the path to the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the index.html file
    index_html_path = os.path.join(current_dir, 'index.html')
    # Render the index.html file
    with open(index_html_path, 'r') as file:
        index_html_content = file.read()
    return index_html_content

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
