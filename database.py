import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:hellobd66@localhost/postgres")
db = scoped_session(sessionmaker(bind=engine))

def main():
    rows = db.execute("SELECT email, password FROM users WHERE email='shibly'").fetchall()
    for row in rows:
        print(f"{row.email} and {row.password}")

if __name__ == "__main__":
    main()