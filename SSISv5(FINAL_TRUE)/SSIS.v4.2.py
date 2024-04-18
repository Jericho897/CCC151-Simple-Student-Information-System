import csv
import sys
import os.path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QMessageBox, QFormLayout, QDialogButtonBox, QInputDialog
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ffffff;")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.course_fields = ['Code','Name']
        self.student_fields = ['StudentID', 'StudentName', 'Gender', 'Year', 'CourseCode']  # Switched places of StudentID and StudentName
        self.student_database = 'Student_Table.csv'
        self.course_database = 'Course_Table.csv'

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

        button_layout = QHBoxLayout()

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
        button_layout.addWidget(add_course_btn)

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
        button_layout.addWidget(delete_course_btn)

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
        button_layout.addWidget(update_course_btn)

        refresh_course_btn = QPushButton("Refresh")
        refresh_course_btn.clicked.connect(self.show_courses)
        refresh_course_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        button_layout.addWidget(refresh_course_btn)

        course_tab_layout.addLayout(button_layout)

        # Filter layout
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Code:", self)
        filter_layout.addWidget(filter_label)

        self.course_filter_input = QLineEdit()
        filter_layout.addWidget(self.course_filter_input)

        filter_button = QPushButton("Filter")
        filter_button.clicked.connect(self.filter_courses)
        filter_layout.addWidget(filter_button)

        course_tab_layout.addLayout(filter_layout)

        self.course_table = QTableWidget()
        self.show_courses()
        course_tab_layout.addWidget(self.course_table)

        self.tabs.addTab(course_tab, "Courses")

    def filter_courses(self):
        filter_text = self.course_filter_input.text().strip()
        if not filter_text:
            self.show_courses()
            return

        filtered_courses = []
        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if filter_text.lower() in row['Code'].lower():
                    filtered_courses.append(row)

        self.populate_course_table(filtered_courses)

    def populate_course_table(self, data):
        self.course_table.clearContents()
        self.course_table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, field in enumerate(self.course_fields):
                item = QTableWidgetItem(row_data[field])
                self.course_table.setItem(row_index, column_index, item)

    def add_course(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Course")

        layout = QVBoxLayout(dialog)

        course_name_input = QLineEdit()
        course_code_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Course Name:", course_name_input)
        form_layout.addRow("Course Code:", course_code_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            course_name = course_name_input.text().strip()
            course_code = course_code_input.text().strip()
            
            if not course_name or not course_code:
                QMessageBox.warning(self, "Error", "Both course name and code are required!")
                return

            if self.course_exists(course_name):
                QMessageBox.warning(self, "Error", "A course with the same name already exists!")
                return

            if self.course_exists(course_code, by_code=True):
                QMessageBox.warning(self, "Error", "A course with the same code already exists!")
                return

            if not os.path.exists(self.course_database):
                with open(self.course_database, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Name', 'Code'])

            with open(self.course_database, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([course_name, course_code])

            QMessageBox.information(self, 'Success', 'Course added successfully!')
            self.show_courses()

    def delete_course(self):
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No courses have been added yet.")
            return

        course_code, ok1 = QInputDialog.getText(self, 'Course Code', 'Enter course code:')
        if not ok1:
            return

        if not self.course_exists(course_code, by_code=True):
            QMessageBox.warning(self, "Error", "Course not found!")
            return

        # Update student records
        if os.path.exists(self.student_database):
            with open(self.student_database, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)

            with open(self.student_database, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
                writer.writeheader()
                for row in rows:
                    if row['CourseCode'] == course_code:
                        row['CourseCode'] = 'N/A'
                    writer.writerow(row)

        # Delete course
        with open(self.course_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        with open(self.course_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.course_fields)
            writer.writeheader()
            for row in rows:
                if row['Code'] != course_code:
                    writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Course deleted successfully!')
        self.show_courses()

    def update_course(self):
        selected_rows = self.course_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No course selected for update!")
            return

        selected_course_code = selected_rows[0].text()
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Course")

        layout = QVBoxLayout(dialog)

        course_name_input = QLineEdit()
        course_code_input = QLineEdit()
        course_code_input.setText(selected_course_code)  # Prefill current course code

        form_layout = QFormLayout()
        form_layout.addRow("Course Name:", course_name_input)
        form_layout.addRow("Course Code:", course_code_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            course_name = course_name_input.text().strip()
            course_code = course_code_input.text().strip()

        if not course_name or not course_code:
            QMessageBox.warning(self, "Error", "Both course name and code are required!")
            return

        if course_code != selected_course_code and self.course_exists(course_code, by_code=True):
            QMessageBox.warning(self, "Error", "A course with the same code already exists!")
            return

        with open(self.course_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            course_data = list(reader)

        with open(self.course_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.course_fields)
            writer.writeheader()
            for row in course_data:
                if row['Code'] == selected_course_code:
                    row['Name'] = course_name
                    row['Code'] = course_code
                writer.writerow(row)

        # Update student records
        with open(self.student_database, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            student_data = list(reader)

        with open(self.student_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
            writer.writeheader()
            for student in student_data:
                if student['CourseCode'] == selected_course_code:
                    student['CourseCode'] = course_code
                writer.writerow(student)

        QMessageBox.information(self, 'Success', 'Course updated successfully!')
        self.show_courses()

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

        button_layout = QHBoxLayout()

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
        button_layout.addWidget(add_student_btn)

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
        button_layout.addWidget(delete_student_btn)

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
        button_layout.addWidget(update_student_btn)

        refresh_student_btn = QPushButton("Refresh")
        refresh_student_btn.clicked.connect(self.show_students)
        refresh_student_btn.setStyleSheet(
            "QPushButton {"
            "background-color: maroon;"
            "color: white;"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #510400;"
            "}"
        )
        button_layout.addWidget(refresh_student_btn)

        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by:", self)
        filter_layout.addWidget(filter_label)

        self.filter_input = QComboBox()
        self.filter_input.addItem("All")
        self.filter_input.addItems(self.student_fields[:-1])  # Excluding CourseCode
        self.filter_input.addItem("CourseCode")  # Adding CourseCode back to filter
        filter_layout.addWidget(self.filter_input)

        self.filter_text = QLineEdit()
        self.filter_text.setPlaceholderText("Enter filter value")
        filter_layout.addWidget(self.filter_text)

        filter_button = QPushButton("Filter")
        filter_button.clicked.connect(self.filter_students)
        filter_layout.addWidget(filter_button)

        student_tab_layout.addLayout(button_layout)
        student_tab_layout.addLayout(filter_layout)

        self.student_table = QTableWidget()
        self.show_students()
        student_tab_layout.addWidget(self.student_table)

        self.tabs.addTab(student_tab, "Students")

    def filter_students(self):
        filter_field = self.filter_input.currentText()
        filter_value = self.filter_text.text().strip()

        if not filter_value:
            self.show_students()  # If filter value is empty, show all students
            return

        if filter_field == "All":
            self.show_students()
            return

        with open(self.student_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            filtered_data = [row for row in reader if filter_value.lower() in row[filter_field].lower()]

        self.student_table.setRowCount(len(filtered_data))
        for row_index, row_data in enumerate(filtered_data):
            for column_index, field in enumerate(self.student_fields):
                item = QTableWidgetItem(row_data[field])
                self.student_table.setItem(row_index, column_index, item)

    def show_students(self):
        if not os.path.exists(self.student_database):
            return

        with open(self.student_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]

        self.student_table.setColumnCount(len(self.student_fields))
        self.student_table.setHorizontalHeaderLabels(self.student_fields)
        self.student_table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, field in enumerate(self.student_fields):
                item = QTableWidgetItem(row_data[field])
                self.student_table.setItem(row_index, column_index, item)

    def add_student(self):
        dialog = AddStudentDialog(self.get_course_codes())  # Changed to get_course_codes
        if dialog.exec() == QDialog.DialogCode.Accepted:
            student_id = dialog.id_input.text()
            student_name = dialog.name_input.text()  # Switched places of StudentID and StudentName
            gender = dialog.gender_input.currentText()
            year_level = dialog.year_level_input.currentText()
            course_code = dialog.course_code_input.currentText()  # Updated to get course code

            if student_name and student_id:
                if student_id in self.get_student_ids():
                    QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
                    return

                if not os.path.exists(self.student_database):
                    with open(self.student_database, 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(self.student_fields)

                with open(self.student_database, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([student_id, student_name, gender, year_level, course_code])  # Updated to write course code
                QMessageBox.information(self, 'Success', 'Student added successfully!')
                self.show_students()
            else:
                QMessageBox.warning(self, "Error", "Student name and ID are required!")

    def delete_student(self):
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
                if row['StudentID'] == student_id:
                    student_found = True
                    break

        if not student_found:
            QMessageBox.warning(self, "Error", "Student not found!")
            return

        with open(self.student_database, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
            writer.writeheader()
            for row in rows:
                if row['StudentID'] != student_id:
                    writer.writerow(row)

        QMessageBox.information(self, 'Success', 'Student deleted successfully!')
        self.show_students()

    def update_student(self):
        selected_rows = self.student_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No student selected for update!")
            return

        selected_student_id = selected_rows[0].text()
        dialog = UpdateStudentDialog(selected_student_id, self.get_course_codes())  # Updated to get_course_codes
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_student_id = dialog.id_input.text()
            updated_student_name = dialog.name_input.text()  # Switched places of StudentID and StudentName
            updated_gender = dialog.gender_input.currentText()
            updated_year_level = dialog.year_level_input.currentText()
            updated_course_code = dialog.course_code_input.currentText()  # Updated to get course code

            with open(self.student_database, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)

            with open(self.student_database, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
                writer.writeheader()
                for row in rows:
                    if row['StudentID'] == selected_student_id:
                        row['StudentID'] = updated_student_id
                        row['StudentName'] = updated_student_name
                        row['Gender'] = updated_gender
                        row['Year'] = updated_year_level
                        row['CourseCode'] = updated_course_code
                    writer.writerow(row)

            QMessageBox.information(self, 'Success', 'Student updated successfully!')
            self.show_students()

    def get_student_ids(self):
        if not os.path.exists(self.student_database):
            return []

        with open(self.student_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row['StudentID'] for row in reader]

    def get_course_codes(self):
        if not os.path.exists(self.course_database):
            return []

        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row['Code'] for row in reader]

    def show_courses(self):
        if not os.path.exists(self.course_database):
            return

        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]

        self.course_table.setColumnCount(len(self.course_fields))
        self.course_table.setHorizontalHeaderLabels(self.course_fields)
        self.populate_course_table(data)

    def course_exists(self, item, by_code=False):
        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if by_code:
                    if row['Code'] == item:
                        return True
                else:
                    if row['Name'] == item:
                        return True
        return False

class AddStudentDialog(QDialog):
    def __init__(self, course_codes):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Student ID")
        layout.addWidget(self.id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Student Name")
        layout.addWidget(self.name_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.gender_input)

        self.year_level_input = QComboBox()
        self.year_level_input.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year"])
        layout.addWidget(self.year_level_input)

        self.course_code_input = QComboBox()
        self.course_code_input.addItems(course_codes)
        layout.addWidget(self.course_code_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

class UpdateStudentDialog(QDialog):
    def __init__(self, student_id, course_codes):
        super().__init__()
        self.setWindowTitle("Update Student")
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.id_input = QLineEdit(student_id)
        self.id_input.setReadOnly(True)
        layout.addWidget(self.id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Student Name")
        layout.addWidget(self.name_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.gender_input)

        self.year_level_input = QComboBox()
        self.year_level_input.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year"])
        layout.addWidget(self.year_level_input)

        self.course_code_input = QComboBox()
        self.course_code_input.addItems(course_codes)
        layout.addWidget(self.course_code_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
