from sqlalchemy.exc import SQLAlchemyError

from conf.conn import session
from conf.models import Teacher, Student, Group, Subject, Grade

import argparse
from datetime import datetime


def load_to_bd(obj):
    """
        Зберігає об'єкт в базі даних.

        Аргументи:
            obj: Об'єкт для збереження (Teacher, Group, Student, Subject, Grade).

        Винятки:
            SQLAlchemyError: Якщо виникає помилка під час взаємодії з базою даних.
    """

    try:
        session.add(obj)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def create_teacher(name):
    """
    Створює нового вчителя в базі даних.

    Аргументи:
        name: Ім'я вчителя.
    """

    teacher = Teacher(fullname=name)
    load_to_bd(teacher)
    print(f"Створено вчителя '{name}'")


def create_group(name):
    """
    Створює нову групу в базі даних.

    Аргументи:
        name: Назва групи.
    """

    group = Group(name=name)
    load_to_bd(group)
    print(f"Створено групу '{name}'")


def create_student(name, group_id):
    """
    Створює нового студента в базі даних.

    Аргументи:
        name: Ім'я студента.
        group_id: ID групи, до якої належить студент.
    """
    student = Student(fullname=name, group_id=group_id)
    load_to_bd(student)
    print(f"Створено студента '{name}'")


def create_subject(name, teacher_id):
    """
    Створює новий предмет в базі даних.

    Аргументи:
        name: Назва предмету.
        teacher_id: ID вчителя, який викладає предмет.
    """
    subject = Subject(name=name, teacher_id=teacher_id)
    load_to_bd(subject)
    print(f"Створено предмет '{name}'")


def create_grade(grade, subject_id, student_id):
    """
    Створює нову оцінку в базі даних.

    Аргументи:
        grade: Оцінка студента.
        subject_id: ID предмету, за яким виставлено оцінку.
        student_id: ID студента, який отримав оцінку.
    """
    gd = Grade(grade=grade, subject_id=subject_id, student_id=student_id, date=datetime.now().date())
    load_to_bd(gd)
    print(f"Створено оцінку '{grade}', ID предметe: {subject_id}, ID студента: {student_id}")


def list_teachers():
    """
    Виводить список всіх вчителів з бази даних.
    """

    teachers = session.query(Teacher).all()
    print("Список вчителів:")
    for teacher in teachers:
        print(f"ID: {teacher.id}, Ім'я: {teacher.fullname}")


def list_groups():
    """
    Виводить список всіх груп з бази даних.
    """

    groups = session.query(Group).all()
    print("Список груп:")
    for group in groups:
        print(f"ID: {group.id}, Назва: {group.name}")


def list_students():
    """
    Виводить список всіх studentів з бази даних.
    """

    students = session.query(Student).all()
    print("Список студентів:")
    for student in students:
        print(f"ID: {student.id}, Ім'я: {student.fullname}, група: {student.group_id}")


def list_subject():
    """
    Виводить список всіх предметів з бази даних.
    """

    subjects = session.query(Subject).all()
    print("Список предметів:")
    for subject in subjects:
        teacher = session.query(Teacher).filter_by(id=subject.teacher_id).first()
        print(f"ID: {subject.id}, Назва: {subject.name}, Викладач: {teacher.fullname}")


def list_grade():
    """
    Виводить список всіх оцінок з бази даних.
    """

    grades = session.query(Grade).all()
    print("Список оцінок:")
    for grade in grades:
        subject = session.query(Subject).filter_by(id=grade.subject_id).first()
        student = session.query(Student).filter_by(id=grade.student_id).first()
        print(f"ID: {grade.id}, Оцінка: {grade.grade}, Предмет: {subject.name}, Студент: {student.fullname}")


def update_teacher(id, name):
    """
    Оновлює дані вчителя в базі даних.

    Аргументи:
        id: ID вчителя.
        name: Оновлене ім'я вчителя.
    """

    teacher = session.query(Teacher).filter_by(id=id).first()
    if teacher:
        teacher.fullname = name
        session.commit()
        print(f"Оновлено дані вчителя з id={id}: нове ім'я - '{name}'")
    else:
        print(f"Вчителя з id={id} не знайдено.")


def update_group(id, name):
    """
    Оновлює дані групи в базі даних.

    Аргументи:
        id: ID групи.
        name: Оновлена назва групи.
    """

    group = session.query(Group).filter_by(id=id).first()
    if group:
        group.name = name
        session.commit()
        print(f"Оновлено дані групи з id={id}: нова назва - '{name}'")
    else:
        print(f"Групу з id={id} не знайдено.")


def update_student(id, name, group):
    """
    Оновлює дані студента в базі даних.

    Аргументи:
        id: ID студента.
        name: Оновлене ім'я студента.
        group: Оновлений ID групи студента.
    """

    student = session.query(Student).filter_by(id=id).first()
    if student:
        student.fullname = name
        student.group_id = group
        session.commit()
        print(f"Оновлено дані студента з id={id}: ім'я - '{name}', група - {group}")
    else:
        print(f"Студент з id={id} не знайдено.")


def update_subject(id, name, teacher_id):
    """
    Оновлює дані предмету в базі даних.

    Аргументи:
        id: ID предмета.
        name: Оновлена назва предмета.
        teacher_id: Оновлений ID викладача, який веде предмет.
    """

    subject = session.query(Subject).filter_by(id=id).first()
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if subject:
        subject.name = name
        subject.teacher_id = teacher_id
        session.commit()
        print(f"Оновлено дані предметів з id={id}: назва - '{name}', викладач - {teacher.fullname}")
    else:
        print(f"Предмет з id={id} не знайдено.")


def update_grade(id, grade):
    """
    Оновлює дані оцінки в базі даних.

    Аргументи:
        id: ID оцінки.
        grade: Оновлена оцінка студента.
    """

    gd = session.query(Grade).filter_by(id=id).first()
    subject = session.query(Subject).filter_by(id=gd.subject_id).first()
    student = session.query(Student).filter_by(id=gd.student_id).first()
    if gd:
        gd.grade = grade
        session.commit()
        print(f"Оновлено дані оцінок з id={id}: оцінка - '{grade}', предмет - {subject.name}, студент - {student.fullname}")
    else:
        print(f"Оцінок з id={id} не знайдено.")


def remove_teacher(id):
    """
    Видаляє вчителя з бази даних.

    Аргументи:
        id: ID вчителя.
    """

    teacher = session.query(Teacher).filter_by(id=id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Видалено вчителя з id={id}")
    else:
        print(f"Вчителя з id={id} не знайдено.")


def remove_group(id):
    """
    Видаляє групу з бази даних.

    Аргументи:
        id: ID групи.
    """

    group = session.query(Group).filter_by(id=id).first()
    if group:
        session.delete(group)
        session.commit()
        print(f"Видалено групу з id={id}")
    else:
        print(f"Групу з id={id} не знайдено.")


def remove_student(id):
    """
    Видаляє студента з бази даних.

    Аргументи:
        id: ID студента.
    """

    student = session.query(Student).filter_by(id=id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Видалено студента з id={id}")
    else:
        print(f"Студент з id={id} не знайдено.")


def remove_subject(id):
    """
    Видаляє предмет з бази даних.

    Аргументи:
        id: ID предмета.
    """

    subject = session.query(Subject).filter_by(id=id).first()
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Видалено предмет з id={id}")
    else:
        print(f"Предмет з id={id} не знайдено.")


def remove_grade(id):
    """
    Видаляє оцінку з бази даних.

    Аргументи:
        id: ID оцінки.
    """

    grade = session.query(Grade).filter_by(id=id).first()
    subject = session.query(Subject).filter_by(id=grade.subject_id).first()
    student = session.query(Student).filter_by(id=grade.student_id).first()
    if grade:
        session.delete(grade)
        session.commit()
        print(f"Видалено оцінок з id={id}: оцінка - '{grade.grade}', предмет - {subject.name}, студент - {student.fullname}")
    else:
        print(f"Оцінок з id={id} не знайдено.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI програма для CRUD операцій із базою даних")
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], help="Оберіть дію: create, list, update, remove")
    parser.add_argument("-m", "--model", choices=["Teacher", "Group", "Student", "Subject", "Grade"], help="Оберіть модель: Teacher, Group")
    parser.add_argument("-n", "--name", help="Ім'я об'єкту для створення або оновлення")
    parser.add_argument("-id", "--id", type=int, help="ID об'єкту для оновлення або видалення")
    parser.add_argument("-gp", "--group", type=int, help="ID групи для додавання студента")
    parser.add_argument("-th", "--teacher_id", type=int, help="ID викладача для додавання предмету")
    parser.add_argument("-sj", "--subject_id", type=int, help="ID предмету для додавання оцінки")
    parser.add_argument("-st", "--student_id", type=int, help="ID студента для додавання оцінки")
    parser.add_argument("-gd", "--grade", type=int, help="Оцінка для додавання оцінки")

    args = parser.parse_args()

    if args.action == "create":
        if args.model == "Teacher":
            create_teacher(args.name)
        elif args.model == "Group":
            create_group(args.name)
        elif args.model == "Student":
            create_student(args.name, args.group)
        elif args.model == "Subject":
            create_subject(args.name, args.teacher_id)
        elif args.model == "Grade":
            create_grade(args.grade, args.subject_id, args.student_id)

    elif args.action == "list":
        if args.model == "Teacher":
            list_teachers()
        elif args.model == "Group":
            list_groups()
        elif args.model == "Student":
            list_students()
        elif args.model == "Subject":
            list_subject()
        elif args.model == "Grade":
            list_grade()

    elif args.action == "update":
        if args.model == "Teacher":
            update_teacher(args.id, args.name)
        elif args.model == "Group":
            update_group(args.id, args.name)
        elif args.model == "Student":
            update_student(args.id, args.name, args.group)
        elif args.model == "Subject":
            update_subject(args.id, args.name, args.teacher_id)
        elif args.model == "Grade":
            update_grade(args.id, args.grade)

    elif args.action == "remove":
        if args.model == "Teacher":
            remove_teacher(args.id)
        elif args.model == "Group":
            remove_group(args.id)
        elif args.model == "Student":
            remove_student(args.id)
        elif args.model == "Subject":
            remove_subject(args.id)
        elif args.model == "Grade":
            remove_grade(args.id)
