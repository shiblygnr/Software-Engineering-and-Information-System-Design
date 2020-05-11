import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime

engine = create_engine("postgresql://postgres:hellobd66@localhost/postgres")
db = scoped_session(sessionmaker(bind=engine))

def main():
    email = "danny@gmail.com"
    user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
    sid = user.student_id

    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May" :
        semester = "Spring"
    elif  month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"

    next_semester = ""
    if semester == "Spring":
        next_semester = "Summer"
    elif semester == "Summer":
        next_semester = "Fall"
    else:
        next_semester = "Spring"
        year +=1
    
    registered_sections = db.execute("select * from takes, sections where takes.section_id = sections.id and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":next_semester, "year":year}).fetchall()
    print(registered_sections)

if __name__ == "__main__":
    main()