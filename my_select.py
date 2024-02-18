from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.conn import session


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    """
    SELECT students.fullname, ROUND(AVG(grades.grade), 1) AS average_grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    GROUP BY students.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """

    result = (session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 1)
        .label('avg_grade'))\
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
        .all())

    return result


# Знайти студента із найвищим середнім балом з певного предмета
def select_2():
    """
    SELECT students.fullname, round(AVG(grades.grade), 1) AS average_grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    WHERE grades.subject_id = 6
    GROUP BY students.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """

    result = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 1)
            .label('average_grade'))\
        .select_from(Grade)
        .join(Student)
        .filter(Grade.subject_id == 6)
        .group_by(Student.id)
        .order_by(desc('average_grade'))
        .limit(1)
        .all()
        )

    return result


# Знайти середній бал у групах з певного предмета
def select_3():
    """
    SELECT groups.name, round(AVG(grades.grade), 1) AS average_grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN groups ON groups.id = students.group_id
    WHERE grades.subject_id = 6
    GROUP BY groups.id;
    """

    result = (
        session.query(
            Group.name,
            func.round(func.avg(Grade.grade), 1)
            .label('average_grade'))\
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .filter(Grade.subject_id == 6)
        .group_by(Group.id)
        .all()
        )

    return result


# Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    """
    SELECT
    ROUND(AVG(grades.grade), 1) AS average_grade
    FROM grades;
    """

    result = (
        session.query(
            func.round(func.avg(Grade.grade), 1)
            .label('average_grade'))\
        .select_from(Grade)
        .all()
    )

    return result


# Знайти які курси читає певний викладач
def select_5():
    """
    SELECT teachers.id, teachers.fullname name, subjects.name
    FROM subjects
    JOIN teachers ON teachers.id = subjects.teacher_id
    WHERE teachers.id = 2;
    """

    result = (
        session.query(
            Teacher.id,
            Teacher.fullname,
            Subject.name)\
        .select_from(Subject)
        .join(Teacher)
        .filter(Teacher.id == 2)
        .all()
    )

    return result


# Знайти список студентів у певній групі
def select_6():
    """
    SELECT students.id, students.fullname, groups."name"
    FROM students
    JOIN groups ON groups.id = students.group_id
    WHERE groups.id = 3
    ORDER BY students.id;
    """

    result = (
        session.query(
            Student.id,
            Student.fullname,
            Group.name)\
        .select_from(Student)
        .join(Group)
        .filter(Group.id == 3)
        .order_by(Student.id)
        .all()
    )

    return result


# Знайти оцінки студентів у окремій групі з певного предмета
def select_7():
    """
    SELECT
    groups."name" AS "group",
    subjects."name" AS "subject",
    students.fullname AS "student",
    grades.grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN groups ON groups.id = students.group_id
    JOIN subjects ON subjects.id = grades.subject_id
    WHERE groups.id = 3
    AND grades.subject_id = 5
    ORDER BY students.fullname;
    """

    result = (
        session.query(
            Group.name,
            Subject.name,
            Student.fullname,
            Grade.grade)\
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(
            Group.id == 3,
            Grade.subject_id == 5
        )
        .order_by(Student.fullname)
        .all()
    )

    return result


# Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8():
    """
    SELECT
    teachers.id,
    teachers.fullname,
    subjects.name,
    ROUND(AVG(grades.grade), 1) AS average_grade
    FROM grades
    JOIN subjects ON subjects.id = grades.subject_id
    JOIN teachers ON teachers.id = subjects.teacher_id
    WHERE teachers.id = 3
    GROUP BY teachers.id, teachers.fullname, subjects.name;
    """

    result = (
        session.query(
            Teacher.id,
            Teacher.fullname,
            Subject.name,
            func.round(func.avg(Grade.grade), 1).label('average_grade'))\
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.id == 3)
        .group_by(
            Teacher.id,
            Teacher.fullname,
            Subject.name
        )
        .all()
    )

    return result


# Знайти список курсів, які відвідує студент
def select_9():
    """
    SELECT
    students.id,
    students.fullname,
    subjects.name
    FROM subjects
    JOIN grades ON grades.subject_id = subjects.id
    JOIN students ON students.id = grades.student_id
    JOIN groups ON groups.id = students.group_id
    WHERE students.id = 5
    ORDER BY subjects.name;
    """

    result = (
        session.query(
            Student.id,
            Student.fullname,
            Subject.name)\
        .select_from(Subject)
        .join(Grade)
        .join(Student)
        .join(Group)
        .filter(Student.id == 5)
        .order_by(Subject.name)
        .all()
    )

    return result

# Список курсів, які певному студенту читає певний викладач
def select_10():
    """
    SELECT
    teachers.fullname AS "teacher",
    students.fullname AS "student",
    subjects.name AS "subjects"
    FROM subjects
    JOIN teachers ON teachers.id = subjects.teacher_id
    JOIN grades ON grades.subject_id = subjects.id
    JOIN students ON students.id = grades.student_id
    WHERE students.id = 6
    AND teachers.id = 3;
    """

    result = (
        session.query(
            Teacher.fullname.label('teacher'),
            Student.fullname.label('student'),
            Subject.name.label('subjects'))\
        .select_from(Subject)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(
            Student.id == 6,
            Teacher.id == 3
        )
        .all()
    )

    return result


# Середній бал, який певний викладач ставить певному студентові
def select_11():
    """
    SELECT
      teachers.fullname AS "teacher",
      students.fullname AS "student",
    ROUND(AVG(grades.grade), 1) AS average_grade
    FROM grades
    JOIN subjects ON subjects.id = grades.subject_id
    JOIN teachers ON teachers.id = subjects.teacher_id
    JOIN students ON students.id = grades.student_id
    WHERE students.id = 5 AND teachers.id = 3
    GROUP BY students.fullname, teachers.fullname;
    """

    result = (
        session.query(
            Teacher.fullname.label('teacher'),
            Student.fullname.label('student'),
            func.round(func.avg(Grade.grade), 1).label('average_grade'))\
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .filter(
            Student.id == 5,
            Teacher.id == 3
        )
        .group_by(
            Student.fullname,
            Teacher.fullname
        )
        .all()
    )

    return result


# Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12():
    """
    SELECT
      grades.grade,
      students.fullname as "student",
      groups."name" as "group",
      subjects."name" as "subject",
      grades."date"
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN groups ON groups.id = students.group_id
    JOIN subjects ON subjects.id = grades.subject_id
    WHERE groups.id = 1
    AND subjects.id = 6
    ORDER BY grades.date DESC
    LIMIT 1;
    """
    result = (
        session.query(
            Grade.grade,
            Student.fullname.label("student"),
            Group.name.label("group"),
            Subject.name.label("subject"),
            Grade.date)\
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(
            Group.id == 1,
            Subject.id == 6
        )
        .order_by(desc(Grade.date))
        .limit(1)
        .all()
        )

    return result


if __name__ == '__main__':
    print('-' * 200)
    print(f"1) Знайти 5 студентів із найбільшим середнім балом з усіх предметів\n{select_1()}")
    print('-' * 200)
    print(f"2) Знайти студента із найвищим середнім балом з певного предмета\n{select_2()}")
    print('-' * 200)
    print(f"3) Знайти середній бал у групах з певного предмета\n{select_3()}")
    print('-' * 200)
    print(f"4) Знайти середній бал на потоці (по всій таблиці оцінок)\n{select_4()}")
    print('-' * 200)
    print(f"5) Знайти які курси читає певний викладач\n{select_5()}")
    print('-' * 200)
    print(f"6) Знайти список студентів у певній групі\n{select_6()}")
    print('-' * 200)
    print(f"7) Знайти оцінки студентів у окремій групі з певного предмета\n{select_7()}")
    print('-' * 200)
    print(f"8) Знайти середній бал, який ставить певний викладач зі своїх предметів\n{select_8()}")
    print('-' * 200)
    print(f"9) Знайти список курсів, які відвідує студент\n{select_9()}")
    print('-' * 200)
    print(f"10) Список курсів, які певному студенту читає певний викладач\n{select_10()}")
    print('-' * 200)
    print(f"11) Середній бал, який певний викладач ставить певному студентові\n{select_11()}")
    print('-' * 200)
    print(f"12) Оцінки студентів у певній групі з певного предмета на останньому занятті\n{select_12()}")
    print('-' * 200)
