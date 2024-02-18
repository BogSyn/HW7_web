from sqlalchemy import ForeignKey, Date, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import Mapped, mapped_column


# Базова модель для всіх сутностей
Base = declarative_base()


# Клас, що описує вчителя
class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)


# Клас, що описує групу
class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


# Клас, що описує студента
class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))
    group: Mapped[Group] = relationship(backref='students')


# Клас, що описує предмет
class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher: Mapped[Teacher] = relationship(backref='subjects')


# Клас, що описує оцінку
class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete='CASCADE'))
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    subject: Mapped[Subject] = relationship(backref='grades')
    student: Mapped[Student] = relationship(backref='grades')
