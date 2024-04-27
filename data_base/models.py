from sqlalchemy import Column, Integer, String, ForeignKey, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), unique=True, nullable=False)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(255), unique=True, nullable=False)
    group_name = Column(String, ForeignKey('groups.group_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    group = relationship("Group")

class Lecturer(Base):
    __tablename__ = 'lecturers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lecturer_name = Column(String(255), unique=True, nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(255), unique=True, nullable=False)
    lecturer_name = Column(String, ForeignKey('lecturers.lecturer_name', ondelete='CASCADE', onupdate='CASCADE'))
    lecturer = relationship("Lecturer")

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Integer, nullable=False)
    student_name = Column(String, ForeignKey('students.student_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    subject_name = Column(String, ForeignKey('subjects.subject_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date_of = Column(Date)

    student = relationship("Student")
    subject = relationship("Subject")
