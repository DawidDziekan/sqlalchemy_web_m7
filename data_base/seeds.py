import datetime
import faker
import random
from connect_db import session
from models import Student, Group, Lecturer, Subject, Grade

NUMBER_STUDENTS = random.randint(40, 50)
NUMBER_GROUPS = 3
NUMBER_LECTURERS = random.randint(3, 5)
SUBJECTS = [
    ("english",), ("math",), ("art",), ("science",), ("history",), ("music",), 
    ("P.E",), ("drama",), ("biology",), ("chemistry",), ("physics",), 
    ("I.T",), ("social studies",), ("technology",), ("philosophy",), 
    ("graphic design",), ("literature",), ("algebra",), ("geometry",)
]
NUMBER_GRADES = random.randint(2, 20)

fake_data = faker.Faker()

def generate_fake_data(number_students, number_groups, number_lecturers, subjects, number_grades) -> tuple:
    fake_students = []
    fake_groups = []
    fake_lecturers = []
    fake_subjects = []

    for _ in range(1, number_students + 1):
        fake_students.append(fake_data.name())

    for _ in range(1, number_groups + 1):
        fake_groups.append(f"Group {fake_data.word()}")

    for _ in range(1, number_lecturers + 1):
        fake_lecturers.append(fake_data.name())
        
    chosen_subjects = random.sample(subjects, random.randint(5, 8))
    for sub in chosen_subjects:
        fake_subjects.append(sub)
    
    return fake_students, fake_groups, fake_lecturers, fake_subjects, number_grades

def prepare_data(students, groups, lecturers, subjects, grades) -> tuple:
    for_students = []
    
    for student in students:
        chosen_group = random.choice(groups)
        for_students.append((student, chosen_group))

    for_groups = []
     
    for group in groups:    
        for_groups.append((group,))

    for_lecturers = []

    for lecturer in lecturers:
        for_lecturers.append((lecturer,))
    
    for_subjects = []
    
    for subject in subjects:
        chosen_lecturer = random.choice(lecturers)
        for_subjects.append((subject[0], chosen_lecturer))

    for_grades = []
    
    for student_id in for_students:
        for subject_id in subjects:
            for _ in range(1, grades):
                grade = round(random.randint(2, 5), 2)
                today = datetime.date.today()
                one_year_ago = today - datetime.timedelta(days=365)
                random_date = one_year_ago + datetime.timedelta(days=random.randint(0, 365))
                for_grades.append((student_id[0], subject_id[0], grade, random_date))

    return for_students, for_groups, for_lecturers, for_subjects, for_grades

def insert_data_to_db(students, groups, lecturers, subjects, grades):
    for group_name in groups:
        group = Group(group_name=group_name[0])
        session.add(group)

    for student_name, group_name in students:
        group = session.query(Group).filter_by(group_name=group_name).first()
        if group:
            student = Student(student_name=student_name, group=group)
            session.add(student)

    for lecturer_name in lecturers:
        lecturer = Lecturer(lecturer_name=lecturer_name)
        session.add(lecturer)

    for subject_name, lecturer_name in subjects:
        lecturer = session.query(Lecturer).filter_by(lecturer_name=lecturer_name).first()
        if lecturer:
            subject = Subject(subject_name=subject_name, lecturer=lecturer)
            session.add(subject)

    for student_id, subject_id, grade, date_of in grades:
        grade_entry = Grade(student_name=student_id, subject_name=subject_id, grade=grade, date_of=date_of)
        session.add(grade_entry)

    session.commit()


if __name__ == "__main__":
    students, groups, lecturers, subjects, grades = prepare_data(
        *generate_fake_data(NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_LECTURERS, SUBJECTS, NUMBER_GRADES)
    )
    insert_data_to_db(students, groups, lecturers, subjects, grades)