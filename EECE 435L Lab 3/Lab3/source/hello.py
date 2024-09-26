import tkinter as tk
from tkinter import ttk
import re
import csv

class Validator:
    """
    A utility class for validating inputs.

    Methods:
        validate_email(email): Validates if an email is in the correct format.
        validate_age(age): Validates if the age is a positive integer.
    """

    @staticmethod
    def validate_email(email):
        """
        Validate an email address.
        
        :param email: The email to validate.
        :type email: str
        :raises ValueError: If the email is invalid.
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            raise ValueError("Invalid email!")

    @staticmethod
    def validate_age(age):
        """
        Validate an age value.
        
        :param age: The age to validate.
        :type age: int
        :raises ValueError: If the age is negative.
        """
        if int(age) < 0:
            raise ValueError("Age cannot be negative")


class Person:
    """
    A class representing a generic person.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person.
    :type age: int
    :param email: The email address of the person.
    :type email: str

    Methods:
        introduce(): Print the introduction of the person.
        to_dict(): Convert the object to a dictionary.
        from_dict(data): Create a Person object from a dictionary.
    """

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """Introduce the person with their name and age."""
        print(f"Hello, my name is {self.name} and I am {self.age} years old")

    def to_dict(self):
        """Convert the person object into a dictionary."""
        return {'name': self.name, 'age': self.age, 'email': self._email}

    @staticmethod
    def from_dict(data):
        """Create a Person object from a dictionary."""
        return Person(data['name'], int(data['age']), data['email'])


class Student(Person):
    """
    A class representing a student, inheriting from Person.

    :param student_id: The ID of the student.
    :type student_id: str

    Methods:
        register_course(course): Add a course to the student's list of registered courses.
        to_dict(): Convert the object to a dictionary.
        from_dict(data): Create a Student object from a dictionary.
    """

    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """Register a course for the student."""
        self.registered_courses.append(course)

    def to_dict(self):
        """Convert the student object into a dictionary."""
        return {
            **super().to_dict(),
            'student_id': self.student_id,
            'registered_courses': [course.to_dict() for course in self.registered_courses]
        }

    @staticmethod
    def from_dict(data):
        """Create a Student object from a dictionary."""
        return Student(data['name'], int(data['age']), data['email'], data['student_id'])


class Instructor(Person):
    """
    A class representing an instructor, inheriting from Person.

    :param instructor_id: The ID of the instructor.
    :type instructor_id: str

    Methods:
        assign_course(course): Assign a course to the instructor.
        to_dict(): Convert the object to a dictionary.
        from_dict(data): Create an Instructor object from a dictionary.
    """

    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """Assign a course to the instructor."""
        self.assigned_courses.append(course)

    def to_dict(self):
        """Convert the instructor object into a dictionary."""
        return {
            **super().to_dict(),
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.to_dict() for course in self.assigned_courses]
        }

    @staticmethod
    def from_dict(data):
        """Create an Instructor object from a dictionary."""
        return Instructor(data['name'], int(data['age']), data['email'], data['instructor_id'])


class Course:
    """
    A class representing a course.

    :param course_id: The ID of the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor teaching the course.
    :type instructor: Instructor

    Methods:
        add_student(student): Enroll a student in the course.
        to_dict(): Convert the object to a dictionary.
        from_dict(data): Create a Course object from a dictionary.
    """

    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """Add a student to the course."""
        self.enrolled_students.append(student)

    def to_dict(self):
        """Convert the course object into a dictionary."""
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.to_dict(),
            'enrolled_students': [student.to_dict() for student in self.enrolled_students]
        }

    @staticmethod
    def from_dict(data):
        """Create a Course object from a dictionary."""
        instructor = Instructor.from_dict(data['instructor'])
        course = Course(data['course_id'], data['course_name'], instructor)

        for student_data in data['enrolled_students']:
            student = Student.from_dict(student_data)
            course.add_student(student)

        return course



import csv

class DataManager:
    """
    A class responsible for managing file I/O operations for students, instructors, and courses.
    
    Methods:
        save_to_file(data, filename): Saves a list of objects to a CSV file.
        load_from_file(filename, obj_class): Loads data from a CSV file and creates objects of the given class.
    """

    @staticmethod
    def save_to_file(data, filename):
        """
        Saves a list of objects to a CSV file.

        :param data: A list of objects to be saved. Each object must have a `to_dict` method.
        :type data: list
        :param filename: The name of the CSV file to save the data in.
        :type filename: str
        """
        with open(filename, 'w', newline='') as file:
            if data:
                headers = data[0].to_dict().keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for obj in data:
                    writer.writerow(obj.to_dict())

    @staticmethod
    def load_from_file(filename, obj_class):
        """
        Loads data from a CSV file and creates a list of objects of the given class.

        :param filename: The name of the CSV file to load the data from.
        :type filename: str
        :param obj_class: The class to instantiate objects from the loaded data.
        :type obj_class: class
        :return: A list of objects created from the data in the file.
        :rtype: list
        """
        data_list = []
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_list.append(obj_class.from_dict(row))
        except FileNotFoundError:
            print(f"No file named {filename} found, starting with an empty list.")
        return data_list


import tkinter as tk
from tkinter import ttk

def run_gui(student_list, instructor_list, course_list):
    """
    Launches the graphical user interface (GUI) for managing students, instructors, and courses.
    
    :param student_list: A list of Student objects.
    :type student_list: list
    :param instructor_list: A list of Instructor objects.
    :type instructor_list: list
    :param course_list: A list of Course objects.
    :type course_list: list
    """
    # Create main window
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("800x600")  # Set the window size

    # Function to add a new student to the system
    def add_student():
        """
        Adds a new student based on user input and saves the student to the file.
        """
        name = student_name_var.get()
        age = student_age_var.get()
        email = student_email_var.get()
        student_id = student_id_var.get()

        try:
            new_student = Student(name, age, email, student_id)
            student_list.append(new_student)
            DataManager.save_to_file(student_list, 'students.csv')
            student_name_var.set("")
            student_age_var.set("")
            student_email_var.set("")
            student_id_var.set("")
        except ValueError as e:
            print(f"Error: {e}")

    # Function to add a new instructor to the system
    def add_instructor():
        """
        Adds a new instructor based on user input and saves the instructor to the file.
        """
        name = instructor_name_var.get()
        age = instructor_age_var.get()
        email = instructor_email_var.get()
        instructor_id = instructor_id_var.get()

        try:
            new_instructor = Instructor(name, age, email, instructor_id)
            instructor_list.append(new_instructor)
            DataManager.save_to_file(instructor_list, 'instructors.csv')
            update_instructor_dropdown()
            instructor_name_var.set("")
            instructor_age_var.set("")
            instructor_email_var.set("")
            instructor_id_var.set("")
        except ValueError as e:
            print(f"Error: {e}")

    # Function to add a new course to the system
    def add_course():
        """
        Adds a new course based on user input and assigns it to an instructor.
        """
        course_id = course_id_var.get()
        course_name = course_name_var.get()
        instructor_name = selected_instructor_var.get()

        # Find the instructor by name
        instructor = next((inst for inst in instructor_list if inst.name == instructor_name), None)
        
        if instructor:
            new_course = Course(course_id, course_name, instructor)
            course_list.append(new_course)
            DataManager.save_to_file(course_list, 'courses.csv')
            course_id_var.set("")
            course_name_var.set("")
            selected_instructor_var.set("")
        else:
            print("Instructor not found.")

    # Update the dropdown menu with instructor names
    def update_instructor_dropdown():
        """
        Updates the instructor dropdown list with the names of available instructors.
        """
        instructors = [instructor.name for instructor in instructor_list]
        instructor_menu['values'] = instructors

    # Define form fields for the student section
    student_name_var = tk.StringVar()
    student_age_var = tk.StringVar()
    student_email_var = tk.StringVar()
    student_id_var = tk.StringVar()

    tk.Label(root, text="Student Name").pack()
    tk.Entry(root, textvariable=student_name_var).pack()

    tk.Label(root, text="Student Age").pack()
    tk.Entry(root, textvariable=student_age_var).pack()

    tk.Label(root, text="Student Email").pack()
    tk.Entry(root, textvariable=student_email_var).pack()

    tk.Label(root, text="Student ID").pack()
    tk.Entry(root, textvariable=student_id_var).pack()

    tk.Button(root, text="Add Student", command=add_student).pack()

    # Define form fields for the instructor section
    instructor_name_var = tk.StringVar()
    instructor_age_var = tk.StringVar()
    instructor_email_var = tk.StringVar()
    instructor_id_var = tk.StringVar()

    tk.Label(root, text="Instructor Name").pack()
    tk.Entry(root, textvariable=instructor_name_var).pack()

    tk.Label(root, text="Instructor Age").pack()
    tk.Entry(root, textvariable=instructor_age_var).pack()

    tk.Label(root, text="Instructor Email").pack()
    tk.Entry(root, textvariable=instructor_email_var).pack()

    tk.Label(root, text="Instructor ID").pack()
    tk.Entry(root, textvariable=instructor_id_var).pack()

    tk.Button(root, text="Add Instructor", command=add_instructor).pack()

    # Define form fields for the course section
    course_id_var = tk.StringVar()
    course_name_var = tk.StringVar()
    selected_instructor_var = tk.StringVar()

    tk.Label(root, text="Course ID").pack()
    tk.Entry(root, textvariable=course_id_var).pack()

    tk.Label(root, text="Course Name").pack()
    tk.Entry(root, textvariable=course_name_var).pack()

    tk.Label(root, text="Instructor").pack()
    instructor_menu = ttk.Combobox(root, textvariable=selected_instructor_var)
    instructor_menu.pack()

    tk.Button(root, text="Add Course", command=add_course).pack()

    # Initial call to populate the instructor dropdown
    update_instructor_dropdown()

    # Start the GUI event loop
    root.mainloop()


# Load data at the beginning of the program
student_list = DataManager.load_from_file('students.csv', Student)
instructor_list = DataManager.load_from_file('instructors.csv', Instructor)
course_list = DataManager.load_from_file('courses.csv', Course)

# Main entry point
if __name__ == "__main__":
    """
    Entry point for running the graphical user interface (GUI).
    Loads the student, instructor, and course lists and launches the GUI.
    """
    run_gui(student_list, instructor_list, course_list)
