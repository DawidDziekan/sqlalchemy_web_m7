from sqlalchemy import select, func, and_
from connect_db import session
from models import Student, Grade, Subject, Lecturer, Group


def select_1():
    # Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
    query = session.execute(
        select(Student.student_name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .group_by(Student.student_name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
    ).mappings().all()
    
    print("wynik select_1:")
    for row in query:
        print(row)

def select_2(subject_name):
    # Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu.
    query = session.execute(
        select(Student.student_name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .filter(Grade.subject.has(subject_name=subject_name))
        .group_by(Student.student_name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
    ).mappings().all()
    
    print("wynik select_2:")
    for row in query:
        print(row)

def select_3(subject_name):
    # Znajdź średni wynik w grupach dla określonego przedmiotu.
    query = session.execute(
        select(Student.group_name, func.avg(Grade.grade).label('average_grade'))
        .join(Grade, Student.student_name == Grade.student_name)
        .join(Subject, Grade.subject_name == Subject.subject_name)
        .filter(Subject.subject_name == subject_name)
        .group_by(Student.group_name)
        ).mappings().all()
    
    print("wynik select_3:")
    for row in query:
        print(row)

def select_4(group_name):
    # Znajdź średni wynik w grupie (w całej tabeli ocen).
    query = session.execute(
        select(func.avg(Grade.grade).label('avg_grade'))
        .join(Student)
        .filter(Student.group_name == group_name)
    ).scalar()

    print("wynik select_4:")
    print(query)

def select_5(lecturer_name):
    # Znajdź przedmioty, których uczy określony wykładowca.
    query = session.execute(
        select(Subject.subject_name)
        .filter(Subject.lecturer.has(lecturer_name=lecturer_name))
    ).mappings().all()
    
    print("wynik select_5:")
    for row in query:
        print(row)

def select_6(group_name):
    # Znajdź listę studentów w określonej grupie.
    query = session.execute(
        select(Student.student_name)
        .filter(Student.group.has(group_name=group_name))
    ).mappings().all()
    
    print("wynik select_6:")
    for row in query:
        print(row)

def select_7(group_name, subject_name):
    # Znajdź oceny studentów w określonej grupie z danego przedmiotu.
    query = session.execute(
        select(Student.student_name, Grade.grade)
        .join(Grade)
        .filter(and_(Student.group.has(group_name=group_name), Grade.subject.has(subject_name=subject_name)))
    ).mappings().all()
    
    print("wynik select_7:")
    for row in query:
        print(row)

def select_8(lecturer_name):
    # Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
    query = session.execute(
        select(func.avg(Grade.grade).label('avg_grade'))
        .join(Subject)
        .filter(Subject.lecturer.has(lecturer_name=lecturer_name))
    ).scalar()
    
    print("wynik select_8:")
    print(query)

def select_9(student_name):
    # Znajdź listę przedmiotów zaliczonych przez danego studenta.
    query = session.execute(
        select(Subject.subject_name)
        .join(Grade)
        .filter(and_(Grade.student.has(student_name=student_name), Grade.grade >= 3))
        .distinct()
    ).mappings().all()
    
    print("wynik select_9:")
    for row in query:
        print(row)

def select_10(student_name, lecturer_name):
    # Znajdź listę przedmiotów prowadzonych przez określonego wykładowcę dla określonego studenta.
    query = session.execute(
        select(Subject.subject_name)
        .join(Grade)
        .filter(and_(Subject.lecturer.has(lecturer_name=lecturer_name), Grade.student.has(student_name=student_name)))
        .distinct()
    ).mappings().all()
    
    print("wynik select_10:")
    for row in query:
        print(row)

if __name__ == "__main__":
    stu = "William Casey"
    sub = "history"
    lec = "Alexis Brown"
    gro = "Group knowledge"
    
    print(select_1())
    print(select_2(sub))
    print(select_3(sub))
    print(select_4(gro))
    print(select_5(lec))
    print(select_6(gro))
    print(select_7(gro, sub))
    print(select_8(lec))
    print(select_9(stu))
    print(select_10(stu, lec))

