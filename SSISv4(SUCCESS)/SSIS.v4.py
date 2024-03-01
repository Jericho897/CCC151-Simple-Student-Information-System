import csv
import sys
import os.path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ffffff;")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.course_fields = ['Name', 'Code']
        self.student_fields = ['Name', 'ID', 'Gender', 'Year Level', 'Course Code']
        self.student_database = 'Student_Table.csv'
        self.course_database = 'Course_Table.csv'

        self.course_list = [
           "BACHELOR OF ARTS IN ENGLISH",
            "BACHELOR OF SCIENCE IN PSYCHOLOGY",
            "BACHELOR OF ARTS IN FILIPINO",
            "BACHELOR OF ARTS IN HISTORY",
            "BACHELOR OF ARTS IN POLITICAL SCIENCE",
            "BACHELOR OF SCIENCE IN CIVIL ENGINEERING",
            "BACHELOR OF SCIENCE IN CERAMICS ENGINEERING",
            "BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING",
            "BACHELOR OF SCIENCE IN COMPUTER ENGINEERING",
            "BACHELOR OF SCIENCE IN ELECTRONICS & COMMUNICATIONS ENGINEERING",
            "BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING",
            "BACHELOR OF SCIENCE IN MINING ENG'G.",
            "BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING TECHNOLOGY",
            "BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING",
            "BACHELOR OF SCIENCE METALLURGICAL ENGINEERING",
            "BACHELOR OF SCIENCE IN BIOLOGY (BOTANY)",
            "BACHELOR OF SCIENCE IN CHEMISTRY",
            "BACHELOR OF SCIENCE IN MATHEMATICS",
            "BACHELOR OF SCIENCE IN PHYSICS",
            "BACHELOR OF SCIENCE IN BIOLOGY (ZOOLOGY)",
            "BACHELOR OF SCIENCE IN BIOLOGY (MARINE)",
            "BACHELOR OF SCIENCE IN BIOLOGY (GENERAL)",
            "BACHELOR OF SCIENCE IN STATISTICS",
            "BACHELOR OF SECONDARY EDUCATION (BIOLOGY)",
            "BACHELOR OF SCIENCE IN INDUSTRIAL EDUCATION (DRAFTING)",
            "BACHELOR OF SECONDARY EDUCATION (CHEMISTRY)",
            "BACHELOR OF SECONDARY EDUCATION (PHYSICS)",
            "BACHELOR OF SECONDARY EDUCATION (MATHEMATICS)",
            "BACHELOR OF SECONDARY EDUCATION (MAPEH)",
            "BACHELOR OF SECONDARY EDUCATION (TLE)",
            "BACHELOR OF SECONDARY EDUCATION (GENERAL SCIENCE)",
            "BACHELOR OF ELEMENTARY EDUCATION (ENGLISH)",
            "BACHELOR OF ELEMENTARY EDUCATION (SCIENCE AND HEALTH)",
            "BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (INDUSTRIAL TECH)",
            "BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (DRAFTING TECH)",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS)",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ECONOMICS)",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ENTREPRENEURIAL MARKETING)",
            "BACHELOR OF SCIENCE IN HOTEL AND RESTAURANT MANAGEMENT",
            "BACHELOR OF SCIENCE IN ACCOUNTANCY",
            "BACHELOR OF SCIENCE IN INFORMATION SYSTEMS",
            "BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY",
            "BACHELOR OF SCIENCE IN COMPUTER SCIENCE",
            "BACHELOR OF SCIENCE IN ELECTRONICS AND COMPUTER TECHNOLOGY (EMBEDDED SYSTEMS)",
            "BACHELOR OF SCIENCE IN ELECTRONICS AND COMPUTER TECHNOLOGY (COMMUNICATIONS SYSTEM)",
            "BACHELOR OF SCIENCE IN INDUSTRIAL AUTOMATION & MECHATRONICS",
            "BACHELOR OF SCIENCE IN ENGINEERING TECHNOLOGY MANAGEMENT",
            "BACHELOR OF SCIENCE IN NURSING"
        ]

        self.course_code_mapping = {
            "BACHELOR OF ARTS IN ENGLISH": "BA-ENG",
            "BACHELOR OF SCIENCE IN PSYCHOLOGY": "BS-PSY",
            "BACHELOR OF ARTS IN FILIPINO": "BA-FIL",
            "BACHELOR OF ARTS IN HISTORY": "BA-HIS",
            "BACHELOR OF ARTS IN POLITICAL SCIENCE": "BA-POLSCI",
            "BACHELOR OF SCIENCE IN CIVIL ENGINEERING": "BS-CE",
            "BACHELOR OF SCIENCE IN CERAMICS ENGINEERING": "BS-CERENG",
            "BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING": "BS-CHEMENG",
            "BACHELOR OF SCIENCE IN COMPUTER ENGINEERING": "BS-COMPE",
            "BACHELOR OF SCIENCE IN ELECTRONICS & COMMUNICATIONS ENGINEERING": "BS-ECE",
            "BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING": "BS-EE",
            "BACHELOR OF SCIENCE IN MINING ENG'G.": "BS-MINE",
            "BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING TECHNOLOGY": "BS-ENVENTECH",
            "BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING": "BS-ME",
            "BACHELOR OF SCIENCE METALLURGICAL ENGINEERING": "BS-METENG",
            "BACHELOR OF SCIENCE IN BIOLOGY (BOTANY)": "BS-BIOBOT",
            "BACHELOR OF SCIENCE IN CHEMISTRY": "BS-CHEM",
            "BACHELOR OF SCIENCE IN MATHEMATICS": "BS-MATH",
            "BACHELOR OF SCIENCE IN PHYSICS": "BS-PHYS",
            "BACHELOR OF SCIENCE IN BIOLOGY (ZOOLOGY)": "BS-BIOZOOL",
            "BACHELOR OF SCIENCE IN BIOLOGY (MARINE)": "BS-BIOMAR",
            "BACHELOR OF SCIENCE IN BIOLOGY (GENERAL)": "BS-BIOGEN",
            "BACHELOR OF SCIENCE IN STATISTICS": "BS-STAT",
            "BACHELOR OF SECONDARY EDUCATION (BIOLOGY)": "BSE-BIO",
            "BACHELOR OF SCIENCE IN INDUSTRIAL EDUCATION (DRAFTING)": "BS-INDUSTED-DRAFT",
            "BACHELOR OF SECONDARY EDUCATION (CHEMISTRY)": "BSE-CHEM",
            "BACHELOR OF SECONDARY EDUCATION (PHYSICS)": "BSE-PHYS",
            "BACHELOR OF SECONDARY EDUCATION (MATHEMATICS)": "BSE-MATH",
            "BACHELOR OF SECONDARY EDUCATION (MAPEH)": "BSE-MAPEH",
            "BACHELOR OF SECONDARY EDUCATION (TLE)": "BSE-TLE",
            "BACHELOR OF SECONDARY EDUCATION (GENERAL SCIENCE)": "BSE-GENSCI",
            "BACHELOR OF ELEMENTARY EDUCATION (ENGLISH)": "BEED-ENG",
            "BACHELOR OF ELEMENTARY EDUCATION (SCIENCE AND HEALTH)": "BEED-SCIHEALTH",
            "BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (INDUSTRIAL TECH)": "BSTTE-INDTECH",
            "BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (DRAFTING TECH)": "BSTTE-DRAFTTECH",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS)": "BSBA-BUSECON",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ECONOMICS)": "BSBA-ECON",
            "BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ENTREPRENEURIAL MARKETING)": "BSBA-ENTMARK",
            "BACHELOR OF SCIENCE IN HOTEL AND RESTAURANT MANAGEMENT": "BSHRM",
            "BACHELOR OF SCIENCE IN ACCOUNTANCY": "BS-ACCT",
            "BACHELOR OF SCIENCE IN INFORMATION SYSTEMS": "BS-IS",
            "BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY": "BS-IT",
            "BACHELOR OF SCIENCE IN COMPUTER SCIENCE": "BS-CS",
            "BACHELOR OF SCIENCE IN ELECTRONICS AND COMPUTER TECHNOLOGY (EMBEDDED SYSTEMS)": "BSECT-EMBSYS",
            "BACHELOR OF SCIENCE IN ELECTRONICS AND COMPUTER TECHNOLOGY (COMMUNICATIONS SYSTEM)": "BSECT-COMMSYS",
            "BACHELOR OF SCIENCE IN INDUSTRIAL AUTOMATION & MECHATRONICS": "BS-IAM",
            "BACHELOR OF SCIENCE IN ENGINEERING TECHNOLOGY MANAGEMENT": "BS-ETM",
            "BACHELOR OF SCIENCE IN NURSING": "BS-NURS"
        }

        self.initialize_ui()

    def initialize_ui(self):
        self.create_course_tab()
        self.create_student_tab()

    def create_course_tab(self):
        course_tab = QWidget()
        course_tab_layout = QVBoxLayout(course_tab)

        title_label = QLabel("Courses Management", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white; margin-bottom: 10px;"
            "background-color: maroon;"
            "border-radius: 20px;"
            "border:1px solid black;"
        )
        course_tab_layout.addWidget(title_label)

        # Add course button
        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        add_course_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        course_tab_layout.addWidget(add_course_btn)

        # List courses button
        list_course_btn = QPushButton("List Courses")
        list_course_btn.clicked.connect(self.list_courses)
        list_course_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        course_tab_layout.addWidget(list_course_btn)

        # Update course button
        update_course_btn = QPushButton("Update Course")
        update_course_btn.clicked.connect(self.update_course)
        update_course_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        course_tab_layout.addWidget(update_course_btn)

        # Delete course button
        delete_course_btn = QPushButton("Delete Course")
        delete_course_btn.clicked.connect(self.delete_course)
        delete_course_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        course_tab_layout.addWidget(delete_course_btn)

        self.tabs.addTab(course_tab, "Courses")

    def create_student_tab(self):
        student_tab = QWidget()
        student_tab_layout = QVBoxLayout(student_tab)

        title_label = QLabel("Students Management", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white; margin-bottom: 10px;"
            "background-color: maroon;"
            "border-radius: 20px;"
            "border:1px solid black;"
        )
        student_tab_layout.addWidget(title_label)

        # Add student button
        add_student_btn = QPushButton("Add Student")
        add_student_btn.clicked.connect(self.add_student)
        add_student_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        student_tab_layout.addWidget(add_student_btn)

        # List students button
        list_student_btn = QPushButton("List Students")
        list_student_btn.clicked.connect(self.list_students)
        list_student_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        student_tab_layout.addWidget(list_student_btn)

        # Update student button
        update_student_btn = QPushButton("Update Student")
        update_student_btn.clicked.connect(self.update_student)
        update_student_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        student_tab_layout.addWidget(update_student_btn)

        # Delete student button
        delete_student_btn = QPushButton("Delete Student")
        delete_student_btn.clicked.connect(self.delete_student)
        delete_student_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        student_tab_layout.addWidget(delete_student_btn)

        self.tabs.addTab(student_tab, "Students")

    # Course management functions
    def add_course(self):
        course_name, ok1 = QInputDialog.getItem(self, 'Course Name', 'Select course name:', self.course_list, 0, False)
        if not ok1:
            return

        course_code = self.course_code_mapping[course_name]

        # Check if the course code already exists
        course_codes = []
        course_names = []
        if os.path.exists(self.course_database):
            with open(self.course_database, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                courses = list(reader)
                course_codes = [row['Code'] for row in courses]
                course_names = [row['Name'] for row in courses]

        if course_code in course_codes:
            QMessageBox.warning(self, "Error", "A course with the same code already exists!")
        elif course_name in course_names:
            QMessageBox.warning(self, "Error", "A course with the same name already exists!")
        else:
            if not os.path.exists(self.course_database):
                with open(self.course_database, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Name', 'Code'])

            with open(self.course_database, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([course_name, course_code])
            QMessageBox.information(self, 'Success', 'Course added successfully!')

    def list_courses(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No courses have been added yet.")
            return

        # Create a dialog window to display the list of courses
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Courses")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
        table.setColumnCount(len(self.course_fields))
        table.setHorizontalHeaderLabels(self.course_fields)
        table.verticalHeader().setVisible(False)

        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if set(reader.fieldnames) != set(self.course_fields):
                QMessageBox.warning(self, "Error", "The headers in the CSV file do not match the expected headers.")
                return
            data = [row for row in reader]

        table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, field in enumerate(self.course_fields):
                item = QTableWidgetItem(row_data[field])
                table.setItem(row_index, column_index, item)

        layout.addWidget(table)
        dialog.exec()

    def update_course(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No courses have been added yet.")
            return

        course_name, ok1 = QInputDialog.getText(self, 'Course Name', 'Enter course name:')
        if not ok1:
            return

        course_code = self.course_code_mapping.get(course_name, None)
        if not course_code:
            QMessageBox.warning(self, "Error", "Course not found!")
            return

        new_course_name, ok2 = QInputDialog.getText(self, 'New Course Name', 'Enter new course name:', QLineEdit.Normal, course_name)
        if not ok2:
            return

        new_course_code = self.course_code_mapping.get(new_course_name, None)
        if new_course_code:
            QMessageBox.warning(self, "Error", "A course with the same name already exists!")
            return

        with open(self.course_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        with open(self.course_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.course_fields)
            writer.writeheader()
            for row in rows:
                if row['Name'] == course_name:
                    row['Name'] = new_course_name
                    row['Code'] = self.course_code_mapping.get(new_course_name)
                writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Course updated successfully!')

    def delete_course(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No courses have been added yet.")
            return

        course_name, ok1 = QInputDialog.getText(self, 'Course Name', 'Enter course name:')
        if not ok1:
            return

        course_code = self.course_code_mapping.get(course_name, None)
        if not course_code:
            QMessageBox.warning(self, "Error", "Course not found!")
            return

        with open(self.course_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        with open(self.course_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.course_fields)
            writer.writeheader()
            for row in rows:
                if row['Name'] != course_name:
                    writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Course deleted successfully!')

    # Student management functions
    def add_student(self):
        student_name, ok1 = QInputDialog.getText(self, 'Student Name', 'Enter student name:')
        if not ok1:
            return

        student_id, ok2 = QInputDialog.getText(self, 'Student ID', 'Enter student ID:')
        if not ok2:
            return

        # Check if the student ID already exists
        student_ids = []
        if os.path.exists(self.student_database):
            with open(self.student_database, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                student_ids = [row['ID'] for row in reader]

        if student_id in student_ids:
            QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
            return

        # Get student information
        gender, ok3 = QInputDialog.getItem(self, 'Gender', 'Select gender:', ['Male', 'Female', 'Other'], 0, False)
        if not ok3:
            return

        year_level, ok4 = QInputDialog.getItem(self, 'Year Level', 'Enter year level:', ['First Year', 'Second Year', 'Third Year', 'Fourth Year'], 0, False)
        if not ok4:
            return

        course_code, ok5 = QInputDialog.getItem(self, 'Course Code', 'Select course code:', list(self.course_code_mapping.values()), 0, False)
        if not ok5:
            return

        with open(self.student_database, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([student_name, student_id, gender, year_level, course_code])
        QMessageBox.information(self, 'Success', 'Student added successfully!')

    def list_students(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No students have been added yet.")
            return

        # Create a dialog window to display the list of students
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Students")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
        table.setColumnCount(len(self.student_fields))
        table.setHorizontalHeaderLabels(self.student_fields)
        table.verticalHeader().setVisible(False)

        with open(self.student_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if set(reader.fieldnames) != set(self.student_fields):
                QMessageBox.warning(self, "Error", "The headers in the CSV file do not match the expected headers.")
                return
            data = [row for row in reader]

        table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, field in enumerate(self.student_fields):
                item = QTableWidgetItem(row_data[field])
                table.setItem(row_index, column_index, item)

        layout.addWidget(table)
        dialog.exec()

    def update_student(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No students have been added yet.")
            return

        student_id, ok1 = QInputDialog.getText(self, 'Student ID', 'Enter student ID:')
        if not ok1:
            return

        student_found = False
        with open(self.student_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            for row in rows:
                if row['ID'] == student_id:
                    student_found = True
                    break

        if not student_found:
            QMessageBox.warning(self, "Error", "Student not found!")
            return

        student_name, ok2 = QInputDialog.getText(self, 'Student Name', 'Enter student name:')
        if not ok2:
            return

        gender, ok3 = QInputDialog.getItem(self, 'Gender', 'Select gender:', ['Male', 'Female', 'Other'], 0, False)
        if not ok3:
            return

        year_level, ok4 = QInputDialog.getItem(self, 'Year Level', 'Enter year level:', ['First Year', 'Second Year', 'Third Year', 'Fourth Year'], 0, False)
        if not ok4:
            return

        course_code, ok5 = QInputDialog.getItem(self, 'Course Code', 'Select course code:', list(self.course_code_mapping.values()), 0, False)
        if not ok5:
            return

        with open(self.student_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
            writer.writeheader()
            for row in rows:
                if row['ID'] == student_id:
                    row['Name'] = student_name
                    row['Gender'] = gender
                    row['Year Level'] = year_level
                    row['Course Code'] = course_code
                writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Student information updated successfully!')

    def delete_student(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No students have been added yet.")
            return

        student_id, ok1 = QInputDialog.getText(self, 'Student ID', 'Enter student ID:')
        if not ok1:
            return

        student_found = False
        with open(self.student_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            for row in rows:
                if row['ID'] == student_id:
                    student_found = True
                    break

        if not student_found:
            QMessageBox.warning(self, "Error", "Student not found!")
            return

        with open(self.student_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
            writer.writeheader()
            for row in rows:
                if row['ID'] != student_id:
                    writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Student deleted successfully!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
