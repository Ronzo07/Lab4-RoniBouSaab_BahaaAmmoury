from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTreeView, QMessageBox, QFileDialog, QInputDialog, QApplication, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTreeView, QFileDialog, QMessageBox, QInputDialog, QTabWidget, QTableWidget, QTableWidgetItem
import json
import csv
import re
import sys


class Person:
    """
    A class to represent a person.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person.
    :type age: int
    :param email: The email of the person.
    :type email: str
    """
    def __init__(self, name, age, email):
        """
        Constructs all the necessary attributes for the person object.

        :param name: The name of the person.
        :type name: str
        :param age: The age of the person.
        :type age: int
        :param email: The email of the person.
        :type email: str
        """
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Prints a brief introduction of the person.
        """
        print(f"Hello, I am {self.name}. I am {self.age} years old. My email is {self._email}.")



class Student(Person):
    """
    A class to represent a student, inheriting from Person.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student.
    :type age: int
    :param email: The email of the student.
    :type email: str
    :param student_id: The ID of the student.
    :type student_id: str
    """
    def __init__(self, name, age, email, student_id):
        """
        Constructs all the necessary attributes for the student object.

        :param name: The name of the student.
        :type name: str
        :param age: The age of the student.
        :type age: int
        :param email: The email of the student.
        :type email: str
        :param student_id: The ID of the student.
        :type student_id: str
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Registers the student for a course.

        :param course: The course to register the student in.
        :type course: Course
        """
        self.registered_courses.append(course)
        print(f"{self.name} registered for {course.course_name}.")


class Instructor(Person):
    """
    A class to represent an instructor, inheriting from Person.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor.
    :type age: int
    :param email: The email of the instructor.
    :type email: str
    :param instructor_id: The ID of the instructor.
    :type instructor_id: str
    """
    def __init__(self, name, age, email, instructor_id):
        """
        Constructs all the necessary attributes for the instructor object.

        :param name: The name of the instructor.
        :type name: str
        :param age: The age of the instructor.
        :type age: int
        :param email: The email of the instructor.
        :type email: str
        :param instructor_id: The ID of the instructor.
        :type instructor_id: str
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns the instructor to a course.

        :param course: The course to assign the instructor to.
        :type course: Course
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self
            print(f"{self.name} is assigned to {course.course_name}.")
        else:
            print("Already Assigned")


class Course:
    """
    A class to represent a course.

    :param course_id: The ID of the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor assigned to the course (default is None).
    :type instructor: Instructor, optional
    """
    def __init__(self, course_id, course_name, instructor=None):
        """
        Constructs all the necessary attributes for the course object.

        :param course_id: The ID of the course.
        :type course_id: str
        :param course_name: The name of the course.
        :type course_name: str
        :param instructor: The instructor assigned to the course (default is None).
        :type instructor: Instructor, optional
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_students(self, student):
        """
        Adds a student to the course.

        :param student: The student to add to the course.
        :type student: Student
        """
        student.register_course(self)
        self.enrolled_students.append(student)
        print(f"{student.name} added to {self.course_name}.")


def save_data(data, filename):
    """
    Saves data to a JSON file.

    :param data: The data to save.
    :type data: dict
    :param filename: The name of the file to save the data to.
    :type filename: str
    """
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_data(filename):
    """
    Loads data from a JSON file.

    :param filename: The name of the file to load the data from.
    :type filename: str
    :return: The loaded data.
    :rtype: dict
    """
    with open(filename, 'r') as file:
        return json.load(file)


def validate_email(email):
    """
    Validates an email address.

    :param email: The email address to validate.
    :type email: str
    :return: True if the email is valid, False otherwise.
    :rtype: bool
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


def validate_age(age):
    """
    Validates an age.

    :param age: The age to validate.
    :type age: int or str
    :return: True if the age is valid, False otherwise.
    :rtype: bool
    """
    if isinstance(age, int) or age.isnumeric():
        return age >= 0 and age <= 100
    else:
        return False


def export_to_csv(students, instructors, courses, filename):
    """
    Exports data to a CSV file.

    :param students: The list of students.
    :type students: list
    :param instructors: The list of instructors.
    :type instructors: list
    :param courses: The list of courses.
    :type courses: list
    :param filename: The name of the file to save the data to.
    :type filename: str
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Name", "ID", "Course"])

        for student in students:
            writer.writerow(["Student", student.name, student.student_id, "N/A"])
        for instructor in instructors:
            writer.writerow(["Instructor", instructor.name, instructor.instructor_id, "N/A"])
        for course in courses:
            writer.writerow(["Course", course.course_name, course.course_id, ", ".join(student.name for student in course.enrolled_students)])

class SchoolManagementSystemGUI(QMainWindow):
    """
    A class to represent the School Management System GUI.

    Inherits from QMainWindow to create the main window for the application.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the School Management System GUI.
        """
        super().__init__()
        self.setWindowTitle("School Management System")

        self.students = []
        self.instructors = []
        self.courses = []

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_professor_section()
        self.create_student_section()
        self.create_course_section()
        self.create_registration_section()
        self.create_instructor_assignment_section()
        self.create_display_section()
        self.create_search_section()
        self.create_edit_delete_section()
        self.create_save_load_section()
        self.create_export_csv_section()

    def create_professor_section(self):
        """
        Creates the professor section of the GUI.
        """
        professor_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.professor_name_entry = QLineEdit()
        self.professor_age_entry = QLineEdit()
        self.professor_email_entry = QLineEdit()
        self.professor_id_entry = QLineEdit()

        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.professor_name_entry)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.professor_age_entry)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.professor_email_entry)
        form_layout.addWidget(QLabel("Instructor ID:"))
        form_layout.addWidget(self.professor_id_entry)

        layout.addLayout(form_layout)

        professor_add_button = QPushButton("Add Professor")
        professor_add_button.clicked.connect(self.add_professor)
        layout.addWidget(professor_add_button)

        self.professor_message_label = QLabel("")
        layout.addWidget(self.professor_message_label)

        professor_widget.setLayout(layout)
        self.tabs.addTab(professor_widget, "Professor")

    def create_student_section(self):
        """
        Creates the student section of the GUI.
        """
        student_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.student_name_entry = QLineEdit()
        self.student_age_entry = QLineEdit()
        self.student_email_entry = QLineEdit()
        self.student_id_entry = QLineEdit()

        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.student_name_entry)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.student_age_entry)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.student_email_entry)
        form_layout.addWidget(QLabel("Student ID:"))
        form_layout.addWidget(self.student_id_entry)

        layout.addLayout(form_layout)

        student_add_button = QPushButton("Add Student")
        student_add_button.clicked.connect(self.add_student)
        layout.addWidget(student_add_button)

        self.student_message_label = QLabel("")
        layout.addWidget(self.student_message_label)

        student_widget.setLayout(layout)
        self.tabs.addTab(student_widget, "Student")

    def create_course_section(self):
        """
        Creates the course section of the GUI.
        """
        course_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.course_id_entry = QLineEdit()
        self.course_name_entry = QLineEdit()

        form_layout.addWidget(QLabel("Course ID:"))
        form_layout.addWidget(self.course_id_entry)
        form_layout.addWidget(QLabel("Course Name:"))
        form_layout.addWidget(self.course_name_entry)

        layout.addLayout(form_layout)

        course_add_button = QPushButton("Add Course")
        course_add_button.clicked.connect(self.add_course)
        layout.addWidget(course_add_button)

        self.course_message_label = QLabel("")
        layout.addWidget(self.course_message_label)

        course_widget.setLayout(layout)
        self.tabs.addTab(course_widget, "Course")

    def create_registration_section(self):
        """
        Creates the student course registration section of the GUI.
        """
        registration_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.student_combobox = QComboBox()
        self.course_combobox = QComboBox()

        form_layout.addWidget(QLabel("Select Student:"))
        form_layout.addWidget(self.student_combobox)
        form_layout.addWidget(QLabel("Select Course:"))
        form_layout.addWidget(self.course_combobox)

        layout.addLayout(form_layout)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_student_for_course)
        layout.addWidget(register_button)

        self.registration_message_label = QLabel("")
        layout.addWidget(self.registration_message_label)

        registration_widget.setLayout(layout)
        self.tabs.addTab(registration_widget, "Student Course Registration")

    def create_instructor_assignment_section(self):
        """
        Creates the instructor assignment section of the GUI.
        """
        instructor_assignment_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.instructor_combobox = QComboBox()
        self.course_combobox_instructor = QComboBox()

        form_layout.addWidget(QLabel("Select Instructor:"))
        form_layout.addWidget(self.instructor_combobox)
        form_layout.addWidget(QLabel("Select Course:"))
        form_layout.addWidget(self.course_combobox_instructor)

        layout.addLayout(form_layout)

        assign_instructor_button = QPushButton("Assign Instructor")
        assign_instructor_button.clicked.connect(self.assign_instructor_to_course)
        layout.addWidget(assign_instructor_button)

        self.instructor_assignment_message_label = QLabel("")
        layout.addWidget(self.instructor_assignment_message_label)

        instructor_assignment_widget.setLayout(layout)
        self.tabs.addTab(instructor_assignment_widget, "Instructor Assignment")

    def create_display_section(self):
        """
        Creates the display records section of the GUI.
        """
        display_widget = QWidget()
        layout = QVBoxLayout()

        self.treeview = QTableWidget()
        self.treeview.setColumnCount(4)
        self.treeview.setHorizontalHeaderLabels(["Type", "Name", "ID", "Course"])
        layout.addWidget(self.treeview)

        display_button = QPushButton("Display All Records")
        display_button.clicked.connect(self.display_records)
        layout.addWidget(display_button)

        display_widget.setLayout(layout)
        self.tabs.addTab(display_widget, "Display Records")

    def create_search_section(self):
        """
        Creates the search records section of the GUI.
        """
        search_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.search_entry = QLineEdit()

        form_layout.addWidget(QLabel("Search By Name or ID:"))
        form_layout.addWidget(self.search_entry)

        layout.addLayout(form_layout)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        layout.addWidget(search_button)

        self.search_result_treeview = QTableWidget()
        self.search_result_treeview.setColumnCount(4)
        self.search_result_treeview.setHorizontalHeaderLabels(["Type", "Name", "ID", "Course"])
        layout.addWidget(self.search_result_treeview)

        search_widget.setLayout(layout)
        self.tabs.addTab(search_widget, "Search Records")

    def create_edit_delete_section(self):
        """
        Creates the edit/delete records section of the GUI.
        """
        edit_delete_widget = QWidget()
        layout = QVBoxLayout()

        self.edit_delete_treeview = QTableWidget()
        self.edit_delete_treeview.setColumnCount(4)
        self.edit_delete_treeview.setHorizontalHeaderLabels(["Type", "Name", "ID", "Course"])
        layout.addWidget(self.edit_delete_treeview)

        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Records")
        load_button.clicked.connect(self.load_records)
        button_layout.addWidget(load_button)

        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        edit_delete_widget.setLayout(layout)
        self.tabs.addTab(edit_delete_widget, "Edit/Delete Records")

    def create_save_load_section(self):
        """
        Creates the save/load data section of the GUI.
        """
        save_load_widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        button_layout.addWidget(load_button)

        layout.addLayout(button_layout)

        save_load_widget.setLayout(layout)
        self.tabs.addTab(save_load_widget, "Save/Load Data")

    def create_export_csv_section(self):
        """
        Creates the export to CSV section of the GUI.
        """
        export_csv_widget = QWidget()
        layout = QVBoxLayout()

        export_csv_button = QPushButton("Export to CSV")
        export_csv_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_csv_button)

        export_csv_widget.setLayout(layout)
        self.tabs.addTab(export_csv_widget, "Export to CSV")

    def add_professor(self):
        """
        Adds a professor to the system.
        """
        name = self.professor_name_entry.text()
        age = self.professor_age_entry.text()
        if age.isnumeric():
            age = int(age)
        email = self.professor_email_entry.text()
        professor_id = self.professor_id_entry.text()

        if validate_email(email) and validate_age(age):
            professor = Instructor(name, age, email, professor_id)
            self.instructors.append(professor)
            self.update_instructor_combobox()
            self.professor_message_label.setText(f"Added Professor: {professor.name}")
            self.professor_message_label.setStyleSheet("color: green;")
            professor.introduce()
        else:
            self.professor_message_label.setText("Invalid professor data")
            self.professor_message_label.setStyleSheet("color: red;")

    def add_student(self):
        """
        Adds a student to the system.
        """
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        if age.isnumeric():
            age = int(age)
        email = self.student_email_entry.text()
        student_id = self.student_id_entry.text()

        if validate_email(email) and validate_age(age):
            student = Student(name, age, email, student_id)
            self.students.append(student)
            self.update_student_combobox()
            self.student_message_label.setText(f"Added Student: {student.name}")
            self.student_message_label.setStyleSheet("color: green;")
            student.introduce()
        else:
            self.student_message_label.setText("Invalid student data")
            self.student_message_label.setStyleSheet("color: red;")

    def add_course(self):
        """
        Adds a course to the system.
        """
        course_id = self.course_id_entry.text()
        course_name = self.course_name_entry.text()

        course = Course(course_id, course_name)
        self.courses.append(course)
        self.update_course_combobox()
        self.course_message_label.setText(f"Added Course: {course.course_name}")
        self.course_message_label.setStyleSheet("color: green;")

    def register_student_for_course(self):
        """
        Registers a student for a course.
        """
        selected_student = self.student_combobox.currentText()
        selected_course = self.course_combobox.currentText()

        student = next((s for s in self.students if s.name == selected_student), None)
        course = next((c for c in self.courses if c.course_name == selected_course), None)

        if student and course:
            course.add_students(student)
            self.registration_message_label.setText(f"Registered {student.name} for {course.course_name}")
            self.registration_message_label.setStyleSheet("color: green;")
        else:
            self.registration_message_label.setText("Invalid student or course")
            self.registration_message_label.setStyleSheet("color: red;")

    def assign_instructor_to_course(self):
        """
        Assigns an instructor to a course.
        """
        selected_course = self.course_combobox_instructor.currentText()
        selected_instructor = self.instructor_combobox.currentText()

        course = next((c for c in self.courses if c.course_name == selected_course), None)
        instructor = next((i for i in self.instructors if i.name == selected_instructor), None)

        if course and instructor:
            instructor.assign_course(course)
            self.instructor_assignment_message_label.setText(f"Assigned {instructor.name} to {course.course_name}")
            self.instructor_assignment_message_label.setStyleSheet("color: green;")
        else:
            self.instructor_assignment_message_label.setText("Invalid course or instructor")
            self.instructor_assignment_message_label.setStyleSheet("color: red;")

    def update_student_combobox(self):
        """
        Updates the student combobox with the current list of students.
        """
        self.student_combobox.clear()
        self.student_combobox.addItems([student.name for student in self.students])

    def update_course_combobox(self):
        """
        Updates the course combobox with the current list of courses.
        """
        self.course_combobox.clear()
        self.course_combobox.addItems([course.course_name for course in self.courses])
        self.course_combobox_instructor.clear()
        self.course_combobox_instructor.addItems([course.course_name for course in self.courses])

    def update_instructor_combobox(self):
        """
        Updates the instructor combobox with the current list of instructors.
        """
        self.instructor_combobox.clear()
        self.instructor_combobox.addItems([instructor.name for instructor in self.instructors])

    def display_records(self):
        """
        Displays all records in the system.
        """
        self.treeview.setRowCount(0)
        for student in self.students:
            row_position = self.treeview.rowCount()
            self.treeview.insertRow(row_position)
            self.treeview.setItem(row_position, 0, QTableWidgetItem("Student"))
            self.treeview.setItem(row_position, 1, QTableWidgetItem(student.name))
            self.treeview.setItem(row_position, 2, QTableWidgetItem(student.student_id))
            self.treeview.setItem(row_position, 3, QTableWidgetItem("N/A"))
        for instructor in self.instructors:
            row_position = self.treeview.rowCount()
            self.treeview.insertRow(row_position)
            self.treeview.setItem(row_position, 0, QTableWidgetItem("Instructor"))
            self.treeview.setItem(row_position, 1, QTableWidgetItem(instructor.name))
            self.treeview.setItem(row_position, 2, QTableWidgetItem(instructor.instructor_id))
            self.treeview.setItem(row_position, 3, QTableWidgetItem("N/A"))
        for course in self.courses:
            row_position = self.treeview.rowCount()
            self.treeview.insertRow(row_position)
            self.treeview.setItem(row_position, 0, QTableWidgetItem("Course"))
            self.treeview.setItem(row_position, 1, QTableWidgetItem(course.course_name))
            self.treeview.setItem(row_position, 2, QTableWidgetItem(course.course_id))
            self.treeview.setItem(row_position, 3, QTableWidgetItem(", ".join(student.name for student in course.enrolled_students)))

    def search_records(self):
        """
        Searches for records in the system based on the search query.
        """
        search_query = self.search_entry.text()
        self.search_result_model.clear()

        for student in self.students:
            if search_query in student.name or search_query in student.student_id:
                self.search_result_model.appendRow([QStandardItem("Student"), QStandardItem(student.name), QStandardItem(student.student_id), QStandardItem("N/A")])
        for instructor in self.instructors:
            if search_query in instructor.name or search_query in instructor.instructor_id:
                self.search_result_model.appendRow([QStandardItem("Instructor"), QStandardItem(instructor.name), QStandardItem(instructor.instructor_id), QStandardItem("N/A")])
        for course in self.courses:
            if search_query in course.course_name or search_query in course.course_id:
                self.search_result_model.appendRow([QStandardItem("Course"), QStandardItem(course.course_name), QStandardItem(course.course_id), QStandardItem(", ".join(student.name for student in course.enrolled_students))])

    def edit_record(self):
        """
        Edits a selected record in the system.
        """
        selected_item = self.edit_delete_treeview.selectedIndexes()
        if selected_item:
            item_values = [index.data() for index in selected_item]
            record_type, name, record_id, _ = item_values

            if record_type == "Student":
                student = next((s for s in self.students if str(s.student_id) == str(record_id)), None)
                if student:
                    new_name, ok = QInputDialog.getText(self, "Edit Student", "Enter new name:", text=student.name)
                    if ok and new_name:
                        student.name = new_name
                        self.display_records()
            elif record_type == "Instructor":
                instructor = next((i for i in self.instructors if str(i.instructor_id) == str(record_id)), None)
                if instructor:
                    new_name, ok = QInputDialog.getText(self, "Edit Instructor", "Enter new name:", text=instructor.name)
                    if ok and new_name:
                        instructor.name = new_name
                        self.display_records()
            elif record_type == "Course":
                course = next((c for c in self.courses if str(c.course_id) == str(record_id)), None)
                if course:
                    new_name, ok = QInputDialog.getText(self, "Edit Course", "Enter new course name:", text=course.course_name)
                    if ok and new_name:
                        course.course_name = new_name
                        self.display_records()

    def delete_record(self):
        """
        Deletes a selected record from the system.
        """
        selected_item = self.edit_delete_treeview.selectedIndexes()
        if selected_item:
            item_values = [index.data() for index in selected_item]
            record_type, name, record_id, _ = item_values

            if record_type == "Student":
                student = next((s for s in self.students if str(s.student_id) == str(record_id)), None)
                if student:
                    self.students.remove(student)
                    self.display_records()
                else:
                    QMessageBox.warning(self, "Delete Student", "Student not found.")
            elif record_type == "Instructor":
                instructor = next((i for i in self.instructors if str(i.instructor_id) == str(record_id)), None)
                if instructor:
                    self.instructors.remove(instructor)
                    self.display_records()
                else:
                    QMessageBox.warning(self, "Delete Instructor", "Instructor not found.")
            elif record_type == "Course":
                course = next((c for c in self.courses if str(c.course_id) == str(record_id)), None)
                if course:
                    self.courses.remove(course)
                    self.display_records()
                else:
                    QMessageBox.warning(self, "Delete Course", "Course not found.")
        else:
            QMessageBox.warning(self, "Delete Record", "No record selected.")

    def save_data(self):
        """
        Saves the current data to a JSON file.
        """
        data = {
            "students": [{"name": s.name, "age": s.age, "email": s._email, "student_id": s.student_id} for s in self.students],
            "instructors": [{"name": i.name, "age": i.age, "email": i._email, "instructor_id": i.instructor_id} for i in self.instructors],
            "courses": [{"course_id": c.course_id, "course_name": c.course_name, "instructor": c.instructor.name if c.instructor else None} for c in self.courses]
        }
        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON files (*.json)")
        if filename:
            with open(filename, 'w') as file:
                json.dump(data, file)
            QMessageBox.information(self, "Save Data", f"Data saved to {filename}")

    def load_data(self):
        """
        Loads data from a JSON file.
        """
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON files (*.json)")
        if filename:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.students = [Student(s['name'], s['age'], s['email'], s['student_id']) for s in data.get('students', [])]
            self.instructors = [Instructor(i['name'], i['age'], i['email'], i['instructor_id']) for i in data.get('instructors', [])]
            self.courses = [Course(c['course_id'], c['course_name'], next((i for i in self.instructors if i.name == c['instructor']), None)) for c in data.get('courses', [])]
            self.update_student_combobox()
            self.update_instructor_combobox()
            self.update_course_combobox()
            self.display_records()
            QMessageBox.information(self, "Load Data", f"Data loaded from {filename}")

    def export_to_csv(self):
        """
        Exports the current data to a CSV file.
        """
        filename, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV files (*.csv)")
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Type", "Name", "ID", "Details"])
                for student in self.students:
                    writer.writerow(["Student", student.name, student.student_id, "N/A"])
                for instructor in self.instructors:
                    writer.writerow(["Instructor", instructor.name, instructor.instructor_id, "N/A"])
                for course in self.courses:
                    writer.writerow(["Course", course.course_name, course.course_id, ", ".join(student.name for student in course.enrolled_students)])
            QMessageBox.information(self, "Export to CSV", f"Data exported to {filename}")

    def load_records(self):
        """
        Loads records into the edit/delete section.
        """
        self.edit_delete_model.clear()

        for student in self.students:
            self.edit_delete_model.appendRow([QStandardItem("Student"), QStandardItem(student.name), QStandardItem(student.student_id), QStandardItem("N/A")])
        for instructor in self.instructors:
            self.edit_delete_model.appendRow([QStandardItem("Instructor"), QStandardItem(instructor.name), QStandardItem(instructor.instructor_id), QStandardItem("N/A")])
        for course in self.courses:
            self.edit_delete_model.appendRow([QStandardItem("Course"), QStandardItem(course.course_name), QStandardItem(course.course_id), QStandardItem(", ".join(student.name for student in course.enrolled_students))])# Create the main window
app = QApplication([])
window = SchoolManagementSystemGUI()
window.show()
app.exec_()