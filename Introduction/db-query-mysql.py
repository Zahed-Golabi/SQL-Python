import mysql.connector as mysql

MY_HOST = "127.0.0.1"
USER_NAME = "zahed"
PASSWORD = "########"


def main():
    db = mysql.connect(host=MY_HOST, user=USER_NAME, password=PASSWORD,
                       database="scratch")
    cur = db.cursor(prepared=True)

    cur.execute("DROP TABLE IF EXISTS temp")
    cur.execute("CREATE TABLE IF NOT EXISTS temp (a TEXT, b TEXT, c TEXt)")
    cur.execute("INSERT INTO temp VALUES ('one', 'two', 'three')")
    cur.execute("INSERT INTO temp VALUES ('four', 'five', 'six')")
    cur.execute("INSERT INTO temp VALUES ('seven', 'eight', 'nine')")
    db.commit()

    cur.execute("SELECT * FROM temp")
    for row in cur:
        print(row)

    query = "SELECT * FROM temp where a = ?"
    cur.execute(query, (input("Please Enter the row: "),))

    for row in cur:
        print(f"result is: {row}")

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
