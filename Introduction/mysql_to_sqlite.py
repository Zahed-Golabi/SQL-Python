import sqlite3
import mysql.connector as mysql

# MySQL Database Connection
HOST = "127.0.0.1"
USER = "zahed"
PASSWORD = "94723115"
MYSQL_DATABASE = "university"

# SQLite Database Connection
SQLite_DATABASE = "../db/university.db"


def main():
    """
    connect to mysql and sqlite databases
    copy table data from mysql to sqlite table
    :return: sqlite database table
    """

    mysql_db = None
    mysql_cursor = None

    sqlite_db = None
    sqlite_cursor = None

    try:
        print("trying to connect to mysql database server....")
        mysql_db = mysql.connect(host=HOST, user=USER, password=PASSWORD, database=MYSQL_DATABASE)
        mysql_cursor = mysql_db.cursor(prepared=True)
        print("successfully connected to mysql server")

    except mysql.Error as error:
        print(f"could not connect to mysql server: {error}")
        exit(1)

    try:
        print("trying to connect to sqlite database....")
        sqlite_db = sqlite3.connect(SQLite_DATABASE)
        sqlite_cursor = sqlite_db.cursor()
        print("successfully connect to sqlite")

    except sqlite3.Error as error:
        print(f"could not connect to sqlite: {error}")
        exit(1)

    mysql_cursor.execute("DROP TABLE IF EXISTS student")
    sqlite_cursor.execute("DROP TABLE IF EXISTS student")

    create_query = """ CREATE TABLE IF NOT EXISTS student (
    stuid INTEGER PRIMARY KEY,
    first_name VARCHAR(9),
    last_name VARCHAR(9),
    major VARCHAR(9),
    faculty VARCHAR(12)
    )
    """
    insert_query = """ INSERT INTO student VALUES (?, ?, ?, ?, ?)
            """
    select_query = "SELECT * FROM student"

    try:
        print("trying to create a table on mysql server, university database....")
        mysql_cursor.execute(create_query)
        print("successfully created table student on university, mysql")

    except mysql.Error as error:
        print(f"could not create table student: {error}")
        exit(1)

    try:
        print("trying to create a table on sqlite, university database....")
        sqlite_cursor.execute(create_query)
        print("successfully created table student on university, sqlite")

    except sqlite3.Error as error:
        print(f"could not create table student: {error}")
        exit(1)

    try:
        print("trying to insert rows to table student on mysql....")
        row_values = [(947231, "Martian", "Amir", "AI", "Computer"),
                      (947232, "David", "Captain", "Network", "Computer"),
                      (947233, "Leonard", "Lizard", "Power", "Electrical")
                      ]
        mysql_cursor.executemany(insert_query, row_values)
        mysql_db.commit()
        print("successfully inserted values to student table")

    except mysql.Error as error:
        print(f"cold not insert values: {error}")
        exit(1)

    try:
        print("trying fetch rows from student on mysql")
        mysql_cursor.execute(select_query)
        print("successfully fetched")
        for row in mysql_cursor:
            print(row)
            sqlite_cursor.execute(insert_query, row)
        sqlite_db.commit()

    except mysql.Error as error:
        print(f"could not fetch rows from student: {error}")
        exit(1)

    try:
        print("rows in sqlite student table after copy")
        sqlite_cursor.execute(select_query)
        for row in sqlite_cursor:
            print(row)

    except sqlite3.Error as error:
        print(f"could not fetch rows in sqlite student after copy: {error}")
        exit(1)

    # close connections
    try:

        mysql_cursor.close()
        sqlite_cursor.close()
        mysql_db.close()
        sqlite_db.close()
        print("\nsuccessfully closed connections")
    except:
        print("could not close connections:")
        exit(1)




if __name__ == '__main__':
    main()


