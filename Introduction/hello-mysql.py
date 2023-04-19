import mysql.connector as mysql

HOST = "localhost"
USER_NAME = "zahed"
PASSWORD = "#####"


def main():
    print("MySQL Example")
    db = None
    cur = None

    try:
        db = mysql.connect(host=HOST, user=USER_NAME, password=PASSWORD,
                           database="scratch")
        cur = db.cursor(prepared=True)
        print("Connected...")

    except mysql.Error as error:
        print(f"could not connected: {error}")
        exit(1)

    try:
        sql_create = """
        CREATE TABLE IF NOT EXISTS hello (
        id SERIAL PRIMARY KEY,
        a VARCHAR(16),
        b VARCHAR(16),
        c VARCHAR(16)
        )
        """
        cur.execute(sql_create)
        print("table hello created")

    except mysql.Error as error:
        print(f"could not create table: {error}")
        exit(1)

    try:
        print("trying to insert rows")
        values = (
            ("one", "two", "three"),
            ("four", "five", "six"),
            ("seven", "eight", "nine"),
            ("one", "four", "six"),
            ("eight", "nine", "ten")
        )
        print("inserting rows...")
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?, ?, ?)", values)
        count = cur.rowcount
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?,?,?)", values)
        count += cur.rowcount
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?,?,?)", values)
        count += cur.rowcount
        print(f"{count} rows added")
        db.commit()

    except mysql.Error as error:
        print(f"could not insert rows: {error}")
        exit(1)

    try:
        cur.execute("SELECT COUNT(*) FROM hello")
        count = cur.fetchone()[0]
        print(f"there are {count} rows in the table")

        # get column names
        cur.execute("SELECT * FROM hello LIMIT 1")
        cur.fetchall()
        column_names = cur.column_names
        print(f"column names are: {column_names}")

        # fetch rows using iterator
        print("\nusing iterator")
        cur.execute("SELECT * FROM hello LIMIT 5")
        for row in cur:
            print(row)

        # fetch rows using dictionary
        print("\ndictionary workaround")
        cur.execute("SELECT * FROM hello LIMIT 5")
        for row in cur:
            rd = dict(zip(column_names, row))
            print(f"as tuple: {row}, as dict: "
                  f"id:{rd['id']} a:{rd['a']}, b:{rd['b']}, c:{rd['c']}")

        # fetch rows by group of 4
        print("\ngroups of 4 using fetchmany")
        cur.execute("SELECT * FROM hello")
        rows = cur.fetchmany(4)
        while rows:
            for row in rows:
                print(row)
            print("#######  #######  #######")
            rows = cur.fetchmany(4)

    except mysql.Error as error:
        print(f"could not fetch rows: {error}")

    print("\ndrop table and close connection")
    cur.execute("DROP TABLE IF EXISTS hello")
    print("table hello deleted")
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
