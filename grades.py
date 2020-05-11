import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:hellobd66@localhost/postgres")
db = scoped_session(sessionmaker(bind=engine))

def main():
    email = "shiblygnr@gmail.com"
    user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
    sid = user.student_id
    student_info = db.execute("SELECT * FROM students WHERE student_id= :sid", {"sid": sid}).fetchone()
    completed_courses = db.execute("SELECT * FROM completedcourses WHERE student_id= :sid", {"sid": sid}).fetchall()
    print(completed_courses)
    semesters = list()
    for course in completed_courses:
        sem = {"semester":course.semester, "year":course.year}
        if sem not in semesters:
            semesters.append(sem)
    #semesters = set(semesters)
    print(semesters)
    courses_by_semester = []
    for semester in semesters:
        courses = []
        for course in completed_courses:
            sem = {"semester":course.semester, "year":course.year}
            if semester == sem:
                courses.append({"course_code":course.course_code, "grade":course.grade})
        courses_by_semester.append({"semester_year":semester, "courses":courses})
    
    print(courses_by_semester)
    print()
    for semester1 in courses_by_semester:
        s = semester1["semester_year"]
        s1 = s["semester"]
        y1 = s["year"]
        print(f"{s1}{y1}")
        courses = semester1["courses"]
        for course in courses:
            course_code = course["course_code"]
            grade = course["grade"]
            print(f"{course_code} {grade}")
        print()



if __name__ == "__main__":
    main()