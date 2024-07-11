import os
from email.policy import default

import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


# Run and print your queries


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )
    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student_2.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )


def get_students_info():
    students = Student.objects.all()
    result = []
    for current_student in students:
        result.append(
            f'Student №{current_student.student_id}: {current_student.first_name} {current_student.last_name}; Email: {current_student.email}')
    return '\n'.join(result)


def update_students_emails():
    students = Student.objects.all()
    for _student in students:
        # _student.email = _student.email.split('@')[0] + '@uni-students.com'
        _student.email = _student.email.replace('university.com', 'uni-students.com')
    Student.objects.bulk_update(students, ['email'])


def truncate_students():
    Student.objects.all().delete()
    # [student.delete() for student in Student.objects.all()]


