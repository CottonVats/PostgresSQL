import psycopg2 as pg


def create_db():
    with pg.connect("dbname=homework_db") as connection:
        with connection.cursor() as cur:
            cur.execute("""CREATE TABLE students (id serial PRIMARY KEY,
            name varchar(100),
            gpa numeric(10, 2),
            birth timestamp with timezone);""")
            cur.execute("""CREATE TABLE courses (id serial PRIMARY KEY,
            name varchar(100)); """)
            cur.execute("""CREATE TABLE registration (id serial PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            course_id INTEGER REFERENCES courses(id));""")


def get_students(course_id):
    with pg.connect("dbname=homework_db") as connection:
        with connection.cursor() as cur:
            names = cur.execute("""select students.name from registration join students on students.id = registration.student_id
            where course_id = (%s)""", (course_id))
    return names






def add_students(course_id, students):
    for stname, bdate in students.items():
        with pg.connect("dbname=homework_db") as connection:
            with connection.cursor() as cur:
                cur.execute("insert into students (name, birth) values (%s, %s) RETURNING id", (stname, bdate))
                id = cur.fetchone
                cur.execute("insert into registration (student_id, course_id) values (%s, %s)", (id, course_id))




def add_student(student):
    for stname, bdate in student.items():
        with pg.connect("dbname=homework_db") as connection:
            with connection.cursor() as cur:
                cur.execute("insert into students (name, birth) values (%s, %s)",(stname, bdate))


def get_student(student_id):
    with pg.connect("dbname=homework_db") as connection:
        with connection.cursor() as cur:
            cur.execute("select * from students where id = (%s)", (student_id))
