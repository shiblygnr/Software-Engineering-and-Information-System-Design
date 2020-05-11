import os
import requests
from flask import Flask, render_template, request, session, g, redirect, url_for, jsonify, make_response
import pdfkit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json, datetime
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename






config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'shiblygnr@gmail.com'
app.config['MAIL_PASSWORD'] = 'iqjydjorbfabowwm'
app.config['MAIL_DEFAULT_SENDER'] = 'shiblygnr@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


app.secret_key = "hellobd66"
engine = create_engine("postgresql://postgres:hellobd66@localhost/postgres", pool_size = 20, max_overflow = 0)
db = scoped_session(sessionmaker(bind=engine))
socketio = SocketIO(app)

@app.route("/studentuser/grades")
def grades():
    email = session["email"]
    user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
    sid = user.student_id
    student_info = db.execute("SELECT * FROM students WHERE student_id= :sid", {"sid": sid}).fetchone()
    completed_courses = db.execute("SELECT * FROM completedcourses, courses WHERE completedcourses.course_code = courses.course_code and student_id= :sid", {"sid": sid}).fetchall()
    print(completed_courses)
    semesters = list()
    for course in completed_courses:
        sem = {"semester":course.semester, "year":course.year}
        if sem not in semesters:
            semesters.append(sem)
    #semesters = set(semesters)
    #print(semesters)
    courses_by_semester = []
    for semester in semesters:
        courses = []
        for course in completed_courses:
            sem = {"semester":course.semester, "year":course.year}
            if semester == sem:
                courses.append({"course_code":course.course_code, "grade":course.grade, "course_title":course.course_title, "course_credit":course.course_credit})
        courses_by_semester.append({"semester_year":semester, "courses":courses})
    """
    #print(courses_by_semester)
    #print()
    for semester1 in courses_by_semester:
        s = semester1["semester_year"]
        s1 = s["semester"]
        y1 = s["year"]
        #print(f"{s1}{y1}")
        courses = semester1["courses"]
        for course in courses:
            course_code = course["course_code"]
            grade = course["grade"]
            #print(f"{course_code} {grade}")
        #print()
    """
    return render_template("student_grades.html", info = student_info, completed = courses_by_semester)


@app.route("/studentuser/course_registration/send_mail")
def send_mail():
    email = session["email"]
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
    next_year = year
    if semester == "Spring":
        next_semester = "Summer"
        next_year = year
    elif semester == "Summer":
        next_semester = "Fall"
        next_year = year
    else:
        next_semester = "Spring"
        next_year = year + 1
    
    info = db.execute("select * from students where student_id = :sid",{"sid":sid}).fetchone()
    #jhamela
    registered_sections = db.execute("select * from takes, sections, courses, teaches where takes.section_id = sections.id and teaches.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":next_semester, "year":next_year}).fetchall()
    tot = 0
    for section in registered_sections:
        tot = tot + section.course_credit*4900

    rendered =  render_template("registration_slip.html", sections = registered_sections, info = info, semester = next_semester, year = next_year, total = tot)
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    msg = Message('Your course registration slip', recipients=[email])
    msg.attach("slip.pdf", "application/pdf", pdf)
    mail.send(msg)
    return "Mail has been sent!"

@socketio.on("add course")
def add_course(data):
    selection = data["selection"]
    email = session["email"]
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
    occupied = []
    schedule = []
    for section in registered_sections:
        occupied.append(section.course_code)
        schedule.append(section.days[0]+section.time_slot)
        schedule.append(section.days[1]+section.time_slot)

    section_details = db.execute("SELECT *  FROM sections WHERE id = :selection", {"selection":selection}).fetchone()
    course_code = section_details.course_code
    course = db.execute("SELECT *  FROM courses WHERE course_code = :cid", {"cid":course_code}).fetchone()
    capacity = section_details.capacity
    t1 = section_details.days[0] + section_details.time_slot
    t2 = section_details.days[1] + section_details.time_slot
    if capacity==0:
        message = {"situation":"bad", "error":"size"}
    elif course_code in occupied:
        message = {"situation":"bad", "error":"taken"}
    elif t1 in schedule or t2 in schedule:
        message = {"situation":"bad", "error":"conflict"}
    else:
        db.execute("INSERT into takes(student_id, section_id) values(:sid, :selection)", {"sid":sid, "selection":selection})
        capacity = capacity - 1
        db.execute("UPDATE sections set capacity = :capacity where id = :selection", {"capacity":capacity, "selection":selection})
        db.commit()
        message = {"situation":"good", "capacity":capacity, "section":str(section_details.id), "course_code":section_details.course_code, "course_title":course.course_title, "section_no":section_details.section_no,
                    "days":section_details.days, "time":section_details.time_slot}

    emit("course registered", message, broadcast=False)

@app.route("/studentuser/edit_registered_courses", methods=["POST"])
def remove_course():
    selection = request.form.get("selection")
    email = session["email"]
    user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
    sid = user.student_id
    db.execute("delete from takes where student_id = :sid and section_id= :selection", {"sid":sid, "selection":selection})
    section = db.execute("select * from sections where id = :selection", {"selection":selection}).fetchone()
    capacity = section.capacity
    capacity += 1
    db.execute("UPDATE sections set capacity = :capacity where id = :selection",{"capacity":capacity, "selection":selection})
    db.commit()
    message = {"success":True}

    return jsonify(message)
 
    


@app.route("/studentuser/show_registered_courses", methods=["POST"])
def show_registered_courses():
    email = session["email"]
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
    
    registered_sections = db.execute("select * from takes, sections, courses where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":next_semester, "year":year}).fetchall()
    if not registered_sections:
        return jsonify({'situation': False})
    else:
        items = []
        for section in registered_sections:
            items.append({"course_code": section.course_code, "course_title":section.course_title, "section_no":section.section_no, "credit":section.course_credit, "days":section.days, "time":section.time_slot})
        return jsonify({'situation': True, 'details':items})

@app.route("/studentuser/edit_registration")
def edit_registration():
    email = session["email"]
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
    next_year = 0
    if semester == "Spring":
        next_semester = "Summer"
        next_year = year
    elif semester == "Summer":
        next_semester = "Fall"
        next_year = year
    else:
        next_semester = "Spring"
        next_year = year + 1
    
    info = db.execute("select * from students where student_id = :sid",{"sid":sid}).fetchone()
    #jhamela
    registered_sections = db.execute("select * from takes, sections, courses, teaches where takes.section_id = sections.id and teaches.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":next_semester, "year":next_year}).fetchall()
    if registered_sections is None:
        return render_template("error.html", message = "No course registered!")
    else:
        return render_template("edit_registration.html", sections = registered_sections, info = info, message = {"semester":next_semester.upper(), "year":next_year})

@app.route("/course_registration/print_slip")
def print_slip():
    email = session["email"]
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
    next_year = 0
    if semester == "Spring":
        next_semester = "Summer"
        next_year = year
    elif semester == "Summer":
        next_semester = "Fall"
        next_year = year
    else:
        next_semester = "Spring"
        next_year = year + 1
    
    info = db.execute("select * from students where student_id = :sid",{"sid":sid}).fetchone()
    #jhamela
    registered_sections = db.execute("select * from takes, sections, courses, teaches where takes.section_id = sections.id and teaches.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":next_semester, "year":next_year}).fetchall()
    tot = 0
    for section in registered_sections:
        tot = tot + section.course_credit*4900

    rendered =  render_template("registration_slip.html", sections = registered_sections, info = info, semester = next_semester, year = next_year, total = tot)
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=slip.pdf'
    return response

@app.route("/grades/print")
def print_gradesheet():
    email = session["email"]
    user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
    sid = user.student_id
    student_info = db.execute("SELECT * FROM students WHERE student_id= :sid", {"sid": sid}).fetchone()
    completed_courses = db.execute("SELECT * FROM completedcourses, courses WHERE completedcourses.course_code = courses.course_code and student_id= :sid", {"sid": sid}).fetchall()
    print(completed_courses)
    semesters = list()
    for course in completed_courses:
        sem = {"semester":course.semester, "year":course.year}
        if sem not in semesters:
            semesters.append(sem)
    #semesters = set(semesters)
    #print(semesters)
    courses_by_semester = []
    for semester in semesters:
        courses = []
        for course in completed_courses:
            sem = {"semester":course.semester, "year":course.year}
            if semester == sem:
                courses.append({"course_code":course.course_code, "grade":course.grade, "course_title":course.course_title, "course_credit":course.course_credit})
        courses_by_semester.append({"semester_year":semester, "courses":courses})
    """
    #print(courses_by_semester)
    #print()
    for semester1 in courses_by_semester:
        s = semester1["semester_year"]
        s1 = s["semester"]
        y1 = s["year"]
        #print(f"{s1}{y1}")
        courses = semester1["courses"]
        for course in courses:
            course_code = course["course_code"]
            grade = course["grade"]
            #print(f"{course_code} {grade}")
        #print()
    """
    rendered =  render_template("print_gradesheet.html", info = student_info, completed = courses_by_semester)
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=gradesheet.pdf'
    return response


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup/student_signup")
def student_signup():
    return render_template("student-signup.html")

@app.route("/hi")
def hi():
    return render_template("hi.html")

flag = 0
@app.route("/studentuser", methods=["POST", "GET"])
def studentuser():
    global flag
    if request.method == "POST":
        session.pop('email', None)
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
        # result = check_password_hash(user.password, password)
        if user is None:
            message = "username is not available!"
            return render_template("home.html", message = message)
        elif user.email==email and check_password_hash(user.password, password) is True:
            flag = 1
            session["email"] = email
            stud = db.execute("SELECT * from studentusers where email= :email", {"email": email}).fetchone()
            sid = stud.student_id
            info = db.execute("SELECT * FROM students WHERE student_id = :sid", {"sid": sid}).fetchone()
            return render_template("student_dashboard.html", info = info)
        else:
            message = "username password missmatched!"
            return render_template("home.html", message = message)
    else:
        if flag == 1:
            email = session["email"]
            stud = db.execute("SELECT * from studentusers where email= :email", {"email": email}).fetchone()
            sid = stud.student_id
            info = db.execute("SELECT * FROM students WHERE student_id = :sid", {"sid": sid}).fetchone()
            return render_template("student_dashboard.html", info = info)            
        else:
            return render_template("home.html")

@app.route("/studentuser/personal_details")
def personal_details():
    email = session["email"]
    stud = db.execute("SELECT * from studentusers where email = :email", {"email": email}).fetchone()
    sid = stud.student_id
    info = db.execute("SELECT * FROM students, studentusers WHERE students.student_id = studentusers.student_id and students.student_id = :sid", {"sid": sid}).fetchone()
    if info is None:
        return json.dumps({'success': False})
    else:
        return render_template("personal_details.html", info = info, image = f"images/{sid}.jpg")


@app.route("/studentuser/edit_student_details")
def edit_student_details():
    email = session["email"]
    stud = db.execute("SELECT * from studentusers where email = :email", {"email": email}).fetchone()
    sid = stud.student_id
    info = db.execute("SELECT * FROM students WHERE student_id = :sid", {"sid": sid}).fetchone()
    return render_template("edit_student_details.html", info = info, image = f"images/{sid}.jpg", user = stud)





@app.route("/studentuser/upload_photo_student", methods = ["POST"])
def upload_photo_student():
    email = session["email"]
    user = db.execute("select * from studentusers where email = :email", {"email":email}).fetchone()
    target = APP_ROOT + "/" + "static/" + "images/"
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files.get("filename")
    print(file)
    filename = file.filename
    destination = "/".join([target, f"{user.student_id}.jpg"])
    print(destination)
    file.save(destination)

    return redirect(url_for('personal_details'))
           

@app.route("/studentuser/enrolled_courses")
def enrolled_courses():
    email = session["email"]
    stud = db.execute("SELECT * from studentusers where email= :email", {"email": email}).fetchone()
    sid = stud.student_id
    courses_enrolled = db.execute("select * from takes, sections, courses where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid", {"sid":sid}).fetchone()
    if len(courses_enrolled) == 0:
        return render_template("error.html", message = "No course found!")
    else:
        return render_template("enrolled_courses.html", courses = courses_enrolled)



@app.route("/api/enrolled/<string:email>")
def enrolled_api(email):
    stud = db.execute("SELECT * from studentusers where email = :email", {"email": email}).fetchone()
    print(email)
    sid = stud.student_id
    items = []
    courses_enrolled = db.execute("select * from takes, sections, courses where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid", {"sid":sid}).fetchone()
    """
    if len(courses_enrolled) >= 1:
        for course in courses_enrolled:
            items.append({'course_code' : course[4], 'section': course[5] })
        return json.dumps(items)
    """
    item = {'course_code' : courses_enrolled.course_code, 'section': courses_enrolled.section_no }
    return json.dumps(item)

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/studentuser/enrolled_courses1")
def enrolled_courses1():
    """
    email = session["email"]
    stud = db.execute("SELECT * from studentusers where email= :email", {"email": email}).fetchone()
    sid = stud.student_id
    courses_enrolled = db.execute("select * from takes, sections, courses where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid", {"sid":sid}).fetchall()
    #courses = []
    #for course in courses_enrolled:
    #    courses.append({"course_code" : course[4], "section_no" : course[5]})
    #courses = json.dumps(courses)
    return jsonify({"success":True, "course_code" : courses_enrolled.course_code, "section" : courses_enrolled.section_no})
    """
    #email = request.form.get("email")
    email = session["email"]
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"
    stud = db.execute("SELECT * from studentusers where email = :email", {"email": email}).fetchone()
    sid = stud.student_id
    info = db.execute("SELECT * from students where student_id = :sid", {"sid": sid}).fetchone()
    courses_enrolled = db.execute("select * from takes, sections, teaches, courses where takes.section_id = sections.id and teaches.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester": semester, "year": year}).fetchall()
    #res = requests.get("localhost:5000/api/enrolled/shiblygnr@gmail.com")
    #if res.status_code != 200:
    #    return jsonify({"success": False})

    # Make sure currency is in response
    #data = res.json()
    """
    if courses_enrolled is None:
        return jsonify({"success": False})
    else:
        return jsonify({"success": True, "course_code": courses_enrolled.course_code, "section": courses_enrolled.section_no})
    
    items = []
    if len(courses_enrolled) >= 1:
        for course in courses_enrolled:
            items.append({'success': True, 'course_code' : course[4], 'section': course[5] })
        return json.dumps(items)
    else:
        return json.dumps({'success': False})
    """
    return render_template("enrolled_courses.html", courses_enrolled = courses_enrolled, info = info, semester = semester, year = year)


@app.route("/studentuser/enrolled_courses/instructor_details/<string:instructor_id>")
def see_instructor_details(instructor_id):
    email = session["email"]
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"
    
    fac1 = db.execute("select * from instructorusers where instructor_id = :instructor_id", {"instructor_id":instructor_id}).fetchone()
    user = db.execute("select * from studentusers where email = :email", {"email":email}).fetchone()
    info = db.execute("select * from students where student_id = :sid", {"sid":user.student_id}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :instructor_id", {"instructor_id":instructor_id}).fetchone()
    officehours = db.execute("Select * from officehours where instructor_id = :fid and semester = :semester and year = :year", {"fid":instructor_id, "semester":semester, "year":year}).fetchall()
    return render_template("see_instructor_details.html", info = info, instructorinfo = fac, image = f"images/{instructor_id}.jpg", officehours = officehours, user = fac1)



@app.route("/studentuser/course_registration")
def course_registration():
    email = session["email"]
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month=="May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"

    next_semester = ""
    next_year = year
    if semester == "Spring":
        next_semester = "Summer"
    elif semester == "Summer":
        next_semester = "Fall"
    else:
        next_semester = "Spring"
        next_year +=1
    
    stud = db.execute("SELECT * from studentusers where email= :email", {"email": email}).fetchone()
    sid = stud.student_id
    student = db.execute("SELECT * FROM students WHERE student_id = :sid", {"sid": sid}).fetchone()
    credit_completed = student.student_tot_credit
    current = db.execute("select * from takes, sections, courses where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = :sid and semester = :semester and year = :year", {"sid":sid, "semester":semester, "year":year}).fetchall()
    sections = db.execute("select * from teaches, sections, courses where teaches.section_id = sections.id and sections.course_code = courses.course_code and course_min_credit <= :credit_completed and course_max_credit >= :credit_completed and semester = :next_semester and year = :next_year order by sections.course_code, section_no asc", {"credit_completed":credit_completed, "next_semester":next_semester, "next_year":next_year}).fetchall()
    completed = db.execute("select course_code from completedcourses where student_id = :sid", {"sid":sid}).fetchall()
    
    course_completed = ['N/A']
    for c in completed:
        course_completed.append(c.course_code)
    current_courses = []
    for c in current:
        current_courses.append(c.course_code)
    #print(current_courses)
    #print(course_completed)
    #print(sections)
    #q1 = db.execute("select * from prereqs where course_to_take = :cd", {"cd":"CSE435"}).fetchone()

    section_info = []
    for section in sections:
        #print(section.course_code)
        q1 = db.execute("select * from prereqs where course_to_take = :cd", {"cd":section.course_code}).fetchone()
        prereq = q1.course_prereq
        #print(prereq)
        if (prereq in course_completed or prereq in current_courses) and (section.course_code not in current_courses):
            section_info.append(section)

    return render_template("course_registration.html", section_info = section_info, info = student, message = {"semester":next_semester.upper(), "year":next_year})

@app.route("/studentuser/enrolled_courses/<int:section>")
def course_details(section):
    email = session["email"]
    user = db.execute("select * from studentusers where email = :email", {"email":email}).fetchone()
    sid = user.student_id
    student = db.execute("select * from students where student_id = :sid", {"sid":sid}).fetchone()
    attendances = db.execute("select * from attendances, students where students.student_id = attendances.student_id and section_id = :section and attendances.student_id = :sid", {"section":section, "sid":sid}).fetchall()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    total_classes = len(attendances)
    attended = 0
    for a in attendances:
        if a.status == "P":
            attended +=1
    attentivity = (attended/total_classes)*100.0
    summary = {"total_classes":total_classes, "attended":attended, "attentivity":float("{:.2f}".format(attentivity))}
    return render_template("student_progress.html", info = student, attendances = attendances, summary = summary, sec = sec)



@app.route("/studentlogout")
def studentlogout():
    global flag
    session.pop('email', None)
    flag = 0
    return redirect(url_for("index"))

flag1 = 0
@app.route("/instructoruser", methods=["POST", "GET"])
def instructoruser():
    global flag1
    if request.method == "POST":
        session.pop('email', None)
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.execute("SELECT * FROM instructorusers WHERE email= :email", {"email": email}).fetchone()
        # result = check_password_hash(user.password, password)
        if user is None:
            message = "username is not available!"
            return render_template("faculty_login.html", message = message)
        elif user.email==email and check_password_hash(user.password, password) is True:
            flag1 = 1
            session["email"] = email
            fac = db.execute("SELECT * from instructorusers where email= :email", {"email": email}).fetchone()
            fid = fac.instructor_id
            info = db.execute("SELECT * FROM instructors WHERE instructor_id = :fid", {"fid": fid}).fetchone()
            return render_template("instructor_dashboard.html", info = info)
        else:
            message = "username password missmatched!"
            return render_template("faculty_login.html", message = message)
    else:
        if flag1 == 1:
            email = session["email"]
            fac = db.execute("SELECT * from instructorusers where email= :email", {"email": email}).fetchone()
            fid = fac.instructor_id
            info = db.execute("SELECT * FROM instructors WHERE instructor_id = :fid", {"fid": fid}).fetchone()
            return render_template("instructor_dashboard.html", info = info)            
        else:
            return render_template("faculty_login.html")

@app.route("/instructoruser/personal_details")
def faculty_personal_details():
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"
    email = session["email"]
    fac = db.execute("SELECT * from instructorusers where email = :email", {"email": email}).fetchone()
    fid = fac.instructor_id
    info = db.execute("SELECT * FROM instructors WHERE instructor_id = :fid", {"fid": fid}).fetchone()
    officehours = db.execute("Select * from officehours where instructor_id = :fid and semester = :semester and year = :year", {"fid":fid, "semester":semester, "year":year}).fetchall()
    if info is None:
        return json.dumps({'success': False})
    else:
        return render_template("faculty_personal_details.html", info = info, image = f"images/{fid}.jpg", officehours = officehours,  user = fac)

@app.route("/instructoruser/edit_instructor_details")
def edit_instructor_details():
    email = session["email"]
    fac = db.execute("SELECT * from instructorusers where email = :email", {"email": email}).fetchone()
    fid = fac.instructor_id
    info = db.execute("SELECT * FROM instructors WHERE instructor_id = :fid", {"fid": fid}).fetchone()
    return render_template("edit_instructor_details.html", info = info, image = f"images/{fid}.jpg", user = fac)





@app.route("/instructouser/upload_photo", methods = ["POST"])
def upload_photo():
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    target = APP_ROOT + "/" + "static/" + "images/"
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files.get("filename")
    print(file)
    filename = file.filename
    destination = "/".join([target, f"{user.instructor_id}.jpg"])
    print(destination)
    file.save(destination)

    return redirect(url_for('faculty_personal_details'))
           

@app.route("/instructoruser/assigned_courses")
def assigned_courses():
    email = session["email"]
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"
    fac = db.execute("SELECT * from instructorusers where email = :email", {"email": email}).fetchone()
    fid = fac.instructor_id
    info = db.execute("SELECT * from instructors where instructor_id = :fid", {"fid": fid}).fetchone()
    courses_assigned = db.execute("select * from teaches, sections, courses where teaches.section_id = sections.id and sections.course_code = courses.course_code and teaches.instructor_id = :fid and semester = :semester and year = :year", {"fid":fid, "semester": semester, "year": year}).fetchall()
    #res = requests.get("localhost:5000/api/enrolled/shiblygnr@gmail.com")
    #if res.status_code != 200:
    #    return jsonify({"success": False})

    # Make sure currency is in response
    #data = res.json()
    """
    if courses_enrolled is None:
        return jsonify({"success": False})
    else:
        return jsonify({"success": True, "course_code": courses_enrolled.course_code, "section": courses_enrolled.section_no})
    
    items = []
    if len(courses_enrolled) >= 1:
        for course in courses_enrolled:
            items.append({'success': True, 'course_code' : course[4], 'section': course[5] })
        return json.dumps(items)
    else:
        return json.dumps({'success': False})
    """
    return render_template("assigned_courses.html", courses_assigned = courses_assigned, info = info, semester = semester, year = year)

@app.route("/instructoruser/assigned_courses/details/<int:section>")
def section_details(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    # student_list = db.execute("SELECT * from sections, takes, students where sections.id = takes.section_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    return render_template("section_details.html" , info = fac, section = section, sec = sec)

@app.route("/instructoruser/assigned_courses/attendance/<int:section>")
def attendance(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    student_list = db.execute("SELECT * from sections, takes, students where sections.id = takes.section_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    return render_template("attendance.html", info=fac, student_list = student_list, sec=sec)

@app.route("/instructoruser/assigned_courses/check_details/<int:section>")
def check_details(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    attendances = db.execute("select * from attendances where section_id = :section", {"section":section}).fetchall()
    dates = []
    for a in attendances:
        if a.date not in dates:
            dates.append(a.date)
    total_classes = len(dates)
    student_list = db.execute("SELECT * from sections, takes, students where sections.id = takes.section_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    report = []
    
    for student in student_list:
        attended = db.execute("select * from attendances where student_id = :sid and section_id = :section and status = :status", {"sid":student.student_id, "section":section, "status":"P"}).fetchall()
        a = len(attended)
        attentivity = (a/total_classes)*100
        report.append({"student_id":student.student_id, "student_first_name":student.student_first_name, "student_last_name":student.student_last_name, "attended":a, "attentivity":"{:.2f}".format(attentivity)})
    try:
        grade_report = []
        for student in student_list:
            grade = db.execute("select * from marks where student_id = :sid and section_id = :section ", {"sid":student.student_id, "section":section}).fetchone()
            total = grade.total
            grade = 0
            if total >= 90:
                grade = 4
            elif total >=87:
                grade = 3.7
            elif total >= 83:
                grade = 3.3
            elif total >= 80:
                grade = 3
            elif total >= 77:
                grade = 2.7
            elif total >= 73:
                grade = 2.3
            elif total >= 70:
                grade = 2
            elif total >= 67:
                grade = 1.7
            elif total >= 63:
                grade = 1.3
            elif total >= 60:
                grade = 1
            else:
                grade = 0
            grade_report.append({"student_id":student.student_id, "student_first_name":student.student_first_name, "student_last_name":student.student_last_name, "grade":grade})
        return render_template("check_details.html", info = fac, report = report, total_classes = total_classes, sec = sec, grade_report = grade_report, g = True)
    except:
        return render_template("check_details.html", info = fac, report = report, total_classes = total_classes, sec = sec, g = False)

@app.route("/instructoruser/assigned_courses/check_student_list/<int:section>")
def check_student_list(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section" :section}).fetchone()
    student_list = db.execute("SELECT * from sections, takes, students, studentusers where sections.id = takes.section_id and students.student_id = studentusers.student_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    return render_template("check_student_list.html", info = fac, students = student_list, sec = sec)
        
@app.route("/instructoruser/assigned_courses/check_student_list/<string:student_id>")
def see_student_details(student_id):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    studentinfo = db.execute("select * from students, studentusers where students.student_id = studentusers.student_id and students.student_id = :student_id", {"student_id":student_id}).fetchone()
    return render_template("see_student_details.html", info = fac, studentinfo = studentinfo, image = f"images/{student_id}.jpg")

@app.route("/instructoruser/assigned_courses/check_student_list/<string:student_id>/gradesheet")
def see_gradesheet(student_id):
    email = session["email"]
    user = db.execute("SELECT * FROM instructorusers WHERE email= :email", {"email": email}).fetchone()
    fac = db.execute("SELECT * FROM instructors WHERE instructor_id= :fid", {"fid": user.instructor_id}).fetchone()
    sid = student_id
    student_info = db.execute("SELECT * FROM students WHERE student_id= :sid", {"sid": sid}).fetchone()
    completed_courses = db.execute("SELECT * FROM completedcourses, courses WHERE completedcourses.course_code = courses.course_code and student_id= :sid", {"sid": sid}).fetchall()
    print(completed_courses)
    semesters = list()
    for course in completed_courses:
        sem = {"semester":course.semester, "year":course.year}
        if sem not in semesters:
            semesters.append(sem)
    #semesters = set(semesters)
    #print(semesters)
    courses_by_semester = []
    for semester in semesters:
        courses = []
        for course in completed_courses:
            sem = {"semester":course.semester, "year":course.year}
            if semester == sem:
                courses.append({"course_code":course.course_code, "grade":course.grade, "course_title":course.course_title, "course_credit":course.course_credit})
        courses_by_semester.append({"semester_year":semester, "courses":courses})
    """
    #print(courses_by_semester)
    #print()
    for semester1 in courses_by_semester:
        s = semester1["semester_year"]
        s1 = s["semester"]
        y1 = s["year"]
        #print(f"{s1}{y1}")
        courses = semester1["courses"]
        for course in courses:
            course_code = course["course_code"]
            grade = course["grade"]
            #print(f"{course_code} {grade}")
        #print()
    """
    return render_template("see_gradesheet.html", info = fac, studentinfo = student_info ,completed = courses_by_semester)

@socketio.on("record attendance")
def record_attendance(data):
    
    date = data["date"]
    sid = data["sid"]
    student = db.execute("SELECT * from students where student_id = :sid", {"sid":sid}).fetchone()
    attendance = data["attendance"]
    section = data["section"]
    name = student.student_first_name
    att = db.execute("SELECT * from attendances where student_id = :sid and section_id = :section and date = :date", {"sid":sid, "section":section, "date":date}).fetchone()
    if att is None:
        db.execute("INSERT into attendances(student_id, section_id, date, status) values(:sid, :section, :date, :attendance)",{"sid":sid, "section":section, "date":date, "attendance":attendance})
        db.commit()
        message = {"situation":"added", "id":sid, "name":name}
    else:
        db.execute("UPDATE attendances set status = :attendance where student_id = :sid and section_id = :section and date = :date",{"sid":sid, "section":section, "date":date, "attendance":attendance})
        db.commit()
        message = {"situation":"changed", "id":sid, "name":name}

    emit('attendance recorded', message, broadcast=False)

@app.route('/instructoruser/show_attendance', methods = ["POST"])
def show_attendance():
    section = request.form.get("section")
    date = request.form.get("date")
    records = db.execute("select * from attendances, students where attendances.student_id = students.student_id and attendances.section_id = :section and attendances.date = :date", {"section":section, "date":date}).fetchall()
    if not records:
        return jsonify({'situation':False})
    else:
        items = []
        for record in records:
            items.append({'student_id':record.student_id, 'student_name':record.student_first_name, 'attendance':record.status})
        return jsonify({'situation':True, 'details':items})

@app.route('/instructoruser/asigned_courses/marks/<int:section>')
def marks(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    student_list = db.execute("SELECT * from sections, takes, students where sections.id = takes.section_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    details = []
    for student in student_list:
        total = db.execute("select * from attendances where student_id = :sid and section_id = :section", {"sid":student.student_id, "section":section}).fetchall()
        attended = db.execute("select * from attendances where student_id = :sid and section_id = :section and status = :status", {"sid":student.student_id, "section":section, "status":"P"}).fetchall()
        attentivity = len(attended)/len(total)
        attendance_mark = attentivity*5
        details.append({"student_id":student.student_id, "student_first_name":student.student_first_name, "student_last_name":student.student_last_name, "attendance_mark": float("{:.2f}".format(attendance_mark))})
    return render_template("marks.html", students = details, info = fac, sec = sec)

@socketio.on("add mark")
def record_mark(data):
    section = int(data['section'])
    sid = data['sid']
    mid1 = float(data['mid1'])
    mid2 = float(data['mid2'])
    final = float(data['final'])
    quiz = float(data['quiz'])
    project = float(data['project'])
    attendance = float(data['attendance'])
    tot = mid1 + mid2 + final + quiz + project + attendance
    available = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    if available is None:
        db.execute("insert into marks(student_id, section_id, mid1, mid2, final, quiz, project, attendance, total) values(:sid, :section, :m1, :m2, :f, :q, :p, :a, :t)", {"sid": sid, "section":section, "m1":mid1, "m2":mid2, "f":final, "q":quiz,"p":project, "a":attendance, "t":tot})
        db.commit()
        message = {'success':True}
    else:
        message = {'success':False}
    emit('mark added', message , broadcast=False)

@app.route("/instructoruser/add_marks", methods = ["POST"])
def add_marks():
    try:
        section = int(request.form.get("section"))
        sid = request.form.get("sid")
        mid1 = float(request.form.get("mid1"))
        mid2 = float(request.form.get("mid2"))
        final = float(request.form.get("final"))
        quiz = float(request.form.get("quiz"))
        project = float(request.form.get("project"))
        attendance = float(request.form.get("attendance"))
        tot = mid1 + mid2 + final + quiz + project + attendance
        available = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        if available is None:
            db.execute("insert into marks(student_id, section_id, mid1, mid2, final, quiz, project, attendance, total) values(:sid, :section, :m1, :m2, :f, :q, :p, :a, :t)", {"sid": sid, "section":section, "m1":mid1, "m2":mid2, "f":final, "q":quiz,"p":project, "a":attendance, "t":tot})
            db.commit()
            return jsonify({'success':"good"})
        else:
            return jsonify({'success':"bad"})

    except:
        return jsonify({'success':"exception"})

@app.route("/instructoruser/assesments/<string:student_id>/<int:section>")
def assesments(student_id, section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fid = user.instructor_id
    fac =  db.execute("select * from instructors where instructor_id = :fid", {"fid":fid}).fetchone()
    student = db.execute("select * from students where student_id = :student_id", {"student_id":student_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    attendances = db.execute("select * from attendances, students where students.student_id = attendances.student_id and section_id = :section and attendances.student_id = :sid", {"section":section, "sid":student_id}).fetchall()
    total_classes = len(attendances)
    attended = 0
    for a in attendances:
        if a.status == "P":
            attended +=1
    attentivity = (attended/total_classes)*5
    return render_template("assesment.html", info = fac, student = student, sec = sec, attentivity = attentivity)

@app.route("/instructoruser/attendance_check", methods = ["POST"])
def attendance_check():
    sid = request.form.get("sid")
    section = request.form.get("section")
    # student = db.execute("select * from students where student_id = :sid", {"sid":sid}).fetchone()
    attendances = db.execute("select * from attendances, students where students.student_id = attendances.student_id and section_id = :section and attendances.student_id = :sid", {"section":section, "sid":sid}).fetchall()
    sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
    total_classes = len(attendances)
    attended = 0
    for a in attendances:
        if a.status == "P":
            attended +=1
    attentivity = (attended/total_classes)*100.0
    summary = jsonify({"total_classes":total_classes, "attended":attended, "attentivity":float("{:.2f}".format(attentivity))})
 
    return summary

@app.route("/instructoruser/get_grades", methods = ["POST"])
def get_grades():
    sid = request.form.get("sid")
    student_info = db.execute("SELECT * FROM students WHERE student_id= :sid", {"sid": sid}).fetchone()
    completed_courses = db.execute("SELECT * FROM completedcourses, courses WHERE completedcourses.course_code = courses.course_code and student_id= :sid", {"sid": sid}).fetchall()
    print(completed_courses)
    if completed_courses is not None:
        details = []
        for course in completed_courses:
            details.append({"course_code": course.course_code, "grade":course.grade})
        print(details)
        return jsonify({'success':True, 'details':details})
    else:
        return jsonify({'success':False})

    # semesters = list()
    # for course in completed_courses:
    #     sem = {"semester":course.semester, "year":course.year}
    #     if sem not in semesters:
    #         semesters.append(sem)
    # #semesters = set(semesters)
    # #print(semesters)
    # courses_by_semester = []
    # for semester in semesters:
    #     courses = []
    #     for course in completed_courses:
    #         sem = {"semester":course.semester, "year":course.year}
    #         if semester == sem:
    #             courses.append({"course_code":course.course_code, "grade":course.grade, "course_title":course.course_title, "course_credit":course.course_credit})
    #     courses_by_semester.append({"semester_year":semester, "courses":courses})


@app.route("/instructoruser/is_added", methods = ["POST"])
def is_added():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    added = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    if added is None:
        return jsonify({'success':True})
    else:
        return jsonify({'success':False})

@app.route("/instructoruser/get_mid1_marks", methods = ["POST"])
def get_mid1_marks():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    return jsonify({"mid1":mark.mid1})


@app.route("/instructoruser/update_mid1", methods = ["POST"])
def update_mid1():
    try:
        to_mid1 = float(request.form.get("mid1"))
        sid = request.form.get("sid")
        section = int(request.form.get("section"))
        mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        tot = mark.total
        mid1_before = mark.mid1
        dif = to_mid1 - mid1_before
        new_total = tot + dif
        db.execute("update marks set mid1 = :to_mid1, total = :new_total where student_id = :sid and section_id = :section", {"to_mid1":to_mid1, "new_total":new_total, "sid":sid, "section":section})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})

@app.route("/instructoruser/get_mid2_marks", methods = ["POST"])
def get_mid2_marks():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    return jsonify({"mid2":mark.mid2})


@app.route("/instructoruser/update_mid2", methods = ["POST"])
def update_mid2():
    try:
        to_mid2 = float(request.form.get("mid2"))
        sid = request.form.get("sid")
        section = int(request.form.get("section"))
        mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        tot = mark.total
        mid2_before = mark.mid2
        dif = to_mid2 - mid2_before
        new_total = tot + dif
        db.execute("update marks set mid2 = :to_mid2, total = :new_total where student_id = :sid and section_id = :section", {"to_mid2":to_mid2, "new_total":new_total, "sid":sid, "section":section})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})  

@app.route("/instructoruser/get_final_marks", methods = ["POST"])
def get_final_marks():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    return jsonify({"final":mark.final})


@app.route("/instructoruser/update_final", methods = ["POST"])
def update_final():
    try:
        to_final = float(request.form.get("final"))
        sid = request.form.get("sid")
        section = int(request.form.get("section"))
        mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        tot = mark.total
        final_before = mark.final
        dif = to_final - final_before
        new_total = tot + dif
        db.execute("update marks set final = :to_final, total = :new_total where student_id = :sid and section_id = :section", {"to_final":to_final, "new_total":new_total, "sid":sid, "section":section})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})   

@app.route("/instructoruser/get_quiz_marks", methods = ["POST"])
def get_quiz_marks():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    return jsonify({"quiz":mark.quiz})


@app.route("/instructoruser/update_quiz", methods = ["POST"])
def update_quiz():
    try:
        to_quiz = float(request.form.get("quiz"))
        sid = request.form.get("sid")
        section = int(request.form.get("section"))
        mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        tot = mark.total
        quiz_before = mark.quiz
        dif = to_quiz - quiz_before
        new_total = tot + dif
        db.execute("update marks set quiz = :to_quiz, total = :new_total where student_id = :sid and section_id = :section", {"to_quiz":to_quiz, "new_total":new_total, "sid":sid, "section":section})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False}) 

@app.route("/instructoruser/get_project_marks", methods = ["POST"])
def get_project_marks():
    sid = request.form.get("sid")
    section = int(request.form.get("section"))
    mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
    return jsonify({"project":mark.project})


@app.route("/instructoruser/update_project", methods = ["POST"])
def update_project():
    try:
        to_project = float(request.form.get("project"))
        sid = request.form.get("sid")
        section = int(request.form.get("section"))
        mark = db.execute("select * from marks where student_id = :sid and section_id = :section", {"sid":sid, "section":section}).fetchone()
        tot = mark.total
        project_before = mark.project
        dif = to_project - project_before
        new_total = tot + dif
        db.execute("update marks set project = :to_project, total = :new_total where student_id = :sid and section_id = :section", {"to_project":to_project, "new_total":new_total, "sid":sid, "section":section})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})   

@app.route("/instructoruser/grade_submission")
def grade_submission():
    email = session["email"]
    d = datetime.datetime.now()
    month = d.strftime("%B")
    semester = ""
    year = d.strftime("%Y")
    if month == "January" or month == "February" or month == "March" or month == "April" or month == "May":
        semester = "Spring"
    elif month == "June" or month == "July" or month == "August":
        semester = "Summer"
    else:
        semester = "Fall"
    fac = db.execute("SELECT * from instructorusers where email = :email", {"email": email}).fetchone()
    fid = fac.instructor_id
    info = db.execute("SELECT * from instructors where instructor_id = :fid", {"fid": fid}).fetchone()
    courses_assigned = db.execute("select * from teaches, sections, courses where teaches.section_id = sections.id and sections.course_code = courses.course_code and teaches.instructor_id = :fid and semester = :semester and year = :year", {"fid":fid, "semester": semester, "year": year}).fetchall()
    return render_template("grade_submission.html", courses_assigned = courses_assigned, info = info)

@app.route("/instructoruser/grade_submission/<int:section>")
def submit_grade(section):
    email = session["email"]
    user = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
    fac = db.execute("select * from instructors where instructor_id = :fid", {"fid":user.instructor_id}).fetchone()
    sec = db.execute("select * from sections where id = :section", {"section" :section}).fetchone()
    student_list = db.execute("SELECT * from sections, takes, students where sections.id = takes.section_id and takes.student_id = students.student_id and takes.section_id = :section", {"section":section}).fetchall()
    return render_template("submit_grade.html", info = fac, students = student_list, sec = sec)

@app.route("/instructoruser/add_grade", methods=["POST"])
def add_grade():
    try:
        email = session["email"]
        fac = db.execute("select * from instructorusers where email = :email", {"email":email}).fetchone()
        fid = fac.instructor_id
        section = int(request.form.get("section"))
        sid = request.form.get("sid")
        grade = float(request.form.get("grade"))
        sec = db.execute("select * from sections where id = :section", {"section":section}).fetchone()
        semester = sec.semester
        year = sec.year
        course_code = sec.course_code
        course = db.execute("select * from courses where course_code = :code", {"code":course_code}).fetchone()
        student = db.execute("select * from students where student_id = :sid", {"sid":sid}).fetchone()
        credit = course.course_credit
        credit_completed = student.student_tot_credit
        cgpa = student.student_cgpa
        updated_cgpa = (credit_completed*cgpa + credit*grade)/(credit_completed+credit)
        updated_tot_credit = credit_completed + credit
        db.execute("Insert into completedcourses(student_id, course_code, instructor_id, course_section, semester, year, grade) values(:student_id, :course_code, :instructor_id, :course_section, :semester, :year, :grade)", {"student_id": sid, "course_code": course_code, "instructor_id": fid, "course_section": section, "semester": semester, "year": year, "grade": grade})
        db.execute("update students set student_tot_credit = :credit, student_cgpa = :cgpa where student_id = :sid", {"credit":updated_tot_credit, "cgpa":updated_cgpa, "sid":sid})
        db.commit()
        return jsonify({'success':True})
    except:
        return jsonify({'success':False})

@app.route("/instructorlogout")
def instructorlogout():
    global flag1
    session.pop('email', None)
    flag1 = 0
    return redirect(url_for("faculty_login"))

@app.route("/signup/student_signup_confirm", methods=["POST"])
def student_signup_confirm():
    email = request.form.get("email")
    phone = request.form.get("phone")
    student_id = request.form.get("sid")
    password = request.form.get("password")
    if email =="" or phone =="" or student_id == "" or password == "":
        message = "Every field is mandatory to fill up, try again!"
        return render_template("student-signup.html", message=message)
    else:
        password_hashed = generate_password_hash(password)
        q = db.execute("SELECT * FROM studentusers WHERE email= :email", {"email": email}).fetchone()
        if q is None:
            db.execute("INSERT INTO studentusers (email, phone_no, student_id, password) VALUES (:email, :phone, :student_id, :password)",{"email": email, "phone": phone, "student_id" : student_id, "password": password_hashed})
            db.commit()
            message = "Account created! You can log in now."
            return render_template("home.html", message=message)
        else:
            message = "Email already exists!"
            return render_template("student-signup.html", message=message)
    
@app.route("/admin_faculty_login")
def admin_faculty_login():
    return render_template("admin_faculty_login.html")

@app.route("/faculty_login")
def faculty_login():
    return render_template("faculty_login.html")

@app.route("/signup/faculty_signup")
def faculty_signup():
    return render_template("faculty_signup.html")

@app.route("/signup/faculty_signup_confirm", methods=["POST"])
def faculty_signup_confirm():
    email = request.form.get("email")
    phone = request.form.get("phone")
    instructor_id = request.form.get("fid")
    password = request.form.get("password")
    if email =="" or phone =="" or instructor_id == "" or password == "":
        message = "Every field is mandatory to fill up, try again!"
        return render_template("faculty_signup.html", message=message)
    else:
        password_hashed = generate_password_hash(password)
        q = db.execute("SELECT * FROM instructorusers WHERE email= :email", {"email": email}).fetchone()
        if q is None:
            db.execute("INSERT INTO instructorusers (email, phone_no, instructor_id, password) VALUES (:email, :phone, :instructor_id, :password)",{"email": email, "phone": phone, "instructor_id" : instructor_id, "password": password_hashed})
            db.commit()
            return redirect(url_for('faculty_login'))
        else:
            message = "Email already exists, try again!"
            return render_template("faculty_signup.html", message=message)
