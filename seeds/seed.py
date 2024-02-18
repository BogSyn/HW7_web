import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.conn import session
from conf.models import Teacher, Student, Group, Subject, Grade

fake = Faker('uk-Ua')


# Додавання викладачів
def create_teachers():
    for teacher in range(3):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)



# Додавання груп
def create_groups():
    for group in range(3):
        group = Group(name=fake.word().capitalize())
        session.add(group)


# Додавання предметів
def create_subjects():
    teadhers = session.query(Teacher).all()
    for subject in range(6):
        subject = Subject(name=fake.word().capitalize(), teacher_id=random.choice(teadhers).id)
        session.add(subject)



# Додавання студентів
def create_students():
     groups = session.query(Group).all()
     for group in groups:
        for student in range(10):
            student = Student(fullname=fake.name(), group_id=group.id)
            session.add(student)


# Додавання студентів
def create_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for student in students:
        for subject in subjects:
            grade = Grade(
                grade=random.randint(0, 100),
                subject_id=subject.id,
                student_id=student.id,
                date=fake.date_this_decade()
            )
            session.add(grade)


if __name__ == '__main__':
    try:
        create_teachers()
        create_groups()
        create_students()
        create_subjects()
        create_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
