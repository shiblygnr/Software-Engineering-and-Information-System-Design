from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    dept_id = db.Column(db.String, unique=True, nullable=False)
    dept_name = db.Column(db.String, nullable = False)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, unique=True, nullable=False)
    student_first_name = db.Column(db.String, nullable=False)
    student_last_name = db.Column(db.String, nullable=False)
    student_dept = db.Column(db.String, db.ForeignKey(Department.dept_id), nullable=False)
    student_cgpa = db.Column(db.FLOAT, nullable=False)
    student_tot_credit = db.Column(db.FLOAT, nullable=False)
    student_dob = db.Column(db.DATE, nullable=False)

class Instructor(db.Model):
    __tablename__ = "instructors"
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.String, unique=True, nullable=False)
    instructor_first_name = db.Column(db.String, nullable=False)
    instructor_last_name = db.Column(db.String, nullable=False)
    instructor_dept = db.Column(db.String, db.ForeignKey(Department.dept_id), nullable=False)
    instructor_rank = db.Column(db.String, nullable=False)
    instructor_dob = db.Column(db.DATE, nullable=False)

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_title = db.Column(db.String, nullable=False)
    course_credit = db.Column(db.FLOAT, nullable = False)
    course_min_credit = db.Column(db.FLOAT, nullable = False)
    course_max_credit = db.Column(db.FLOAT, nullable = False)
    course_dept = db.Column(db.String, db.ForeignKey(Department.dept_id), nullable=False)

class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, db.ForeignKey(Course.course_code), nullable = False)
    section_no = db.Column(db.Integer, nullable = False)
    semester = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer,  nullable = False)
    time_slot = db.Column(db.String, nullable=False)
    days = db.Column(db.String, nullable = False)
    capacity = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('course_code', 'section_no', 'semester', 'year', name='section_pk'),)

class Takes(db.Model):
    __tablename__ = "takes"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey(Student.student_id), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey(Section.id),  nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'section_id',  name='takes_pk'),)

class Teaches(db.Model):
    __tablename__="teaches"
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.String, db.ForeignKey(Instructor.instructor_id), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey(Section.id), nullable=False)
    __table_args__ = (db.UniqueConstraint('instructor_id', 'section_id',  name='teaches_pk'),)

class PreReq(db.Model):
    __tablename__ = "prereqs"
    id = db.Column(db.Integer, primary_key=True)
    course_to_take = db.Column(db.String, db.ForeignKey(Course.course_code), nullable = False, unique = True)
    course_prereq = db.Column(db.String, db.ForeignKey(Course.course_code), nullable = False)

class CourseCompleted(db.Model):
    __tablename__ = "completedcourses"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey(Student.student_id), nullable=False)
    course_code = db.Column(db.String, db.ForeignKey(Course.course_code), nullable = False)
    instructor_id = db.Column(db.String, db.ForeignKey(Instructor.instructor_id), nullable = False)
    course_section = db.Column(db.Integer, db.ForeignKey(Section.id), nullable=False)
    semester = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    grade = db.Column(db.FLOAT, nullable = False)
    __table_args__ = (db.UniqueConstraint('student_id', 'course_code',  name='coursecompleted_pk'),)

class StudentUser(db.Model):
    __tablename__ = "studentusers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique = True, nullable = False)
    phone_no = db.Column(db.String, unique = True, nullable = False)
    student_id = db.Column(db.String, db.ForeignKey(Student.student_id), unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)

class InstructorUser(db.Model):
    __tablename__ = "instructorusers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique = True, nullable = False)
    phone_no = db.Column(db.String, unique = True, nullable = False)
    instructor_id = db.Column(db.String, db.ForeignKey(Instructor.instructor_id), unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Attendance(db.Model):
    __tablename__ = "attendances"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey(Student.student_id), nullable = False)
    section_id = db.Column(db.Integer,  db.ForeignKey(Section.id), nullable = False)
    date = db.Column(db.DATE, nullable=False)
    status = db.Column(db.String, nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'section_id', 'date', name='attendance_pk'),)

class Mark(db.Model):
    __tablename__ = "marks"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey(Student.student_id), nullable = False)
    section_id = db.Column(db.Integer,  db.ForeignKey(Section.id), nullable = False)
    mid1 = db.Column(db.FLOAT, nullable = False)
    mid2 = db.Column(db.FLOAT, nullable = False)
    final = db.Column(db.FLOAT, nullable = False)
    quiz = db.Column(db.FLOAT, nullable = False)
    project = db.Column(db.FLOAT, nullable = False)
    attendance = db.Column(db.FLOAT, nullable = False)
    total = db.Column(db.FLOAT)
    __table_args__ = (db.UniqueConstraint('student_id', 'section_id', name='mark_pk'),)

class OfficeHour(db.Model):
    __tablename__ = "officehours"
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.String, db.ForeignKey(Instructor.instructor_id))
    slot = db.Column(db.String)
    semester = db.Column(db.String)
    year = db.Column(db.Integer)

