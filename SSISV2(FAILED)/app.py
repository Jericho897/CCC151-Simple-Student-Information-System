from flask import Flask, request, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)
import os
print("Current Working Directory:", os.getcwd())

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

# Add route for deleting a student
@app.route('/delete_student', methods=['POST'])
def delete_student():
    try:
        student_id = request.json['studentID']
        with open('students.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open('students.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[0] != student_id:
                    writer.writerow(row)
        return {'success': True, 'message': 'Student deleted successfully!'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while deleting the student: {str(e)}'}

# Add route for deleting a course
@app.route('/delete_course', methods=['POST'])
def delete_course():
    try:
        course_code = request.json['courseCode']
        with open('courses.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open('courses.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[0] != course_code:
                    writer.writerow(row)
        return {'success': True, 'message': 'Course deleted successfully!'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while deleting the course: {str(e)}'}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
