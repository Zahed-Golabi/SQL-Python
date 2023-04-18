import sqlite3


def main():
    print("SQLite Example")
    db = None
    cur = None

    try:
        db = sqlite3.connect(":memory:")
        cur = db.cursor()
        print("connected...")

    except sqlite3.Error as e:
        print(f"could not open database: {e}")
        exit(1)

    try:
        sql_create = """ 
        CREATE TABLE IF NOT EXISTS hello (
        id INTEGER PRIMARY KEY,
        a TEXT,
        b TEXT,
        c TEXT)
        """
        cur.execute(sql_create)
        print("table created")

    except sqlite3.Error as e:
        print(f"could not create table: {e}")
        exit(1)

    try:
        print("trying to insert rows")
        values = (
            ("one", "two", "three"),
            ("four", "five", "six"),
            ("seven", "eight", "nine"),
            ("one", "three", "four"),
            ("six", "zero", "nine"),
        )
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?,?,?)", values)
        count = cur.rowcount
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?,?,?)", values)
        count += cur.rowcount
        cur.executemany("INSERT INTO hello (a,b,c) VALUES (?,?,?)", values)
        count += cur.rowcount
        print(f"{count} rows added")
        db.commit()

    except sqlite3.Error as e:
        print(f"could not insert rows: {e}")
        exit(1)

    try:
        cur.execute("SELECT COUNT(*) FROM hello")
        count = cur.fetchone()[0]
        print(f"there are {count} rows in the table")

        # get column names from SQLite meta-data table_info
        cur.execute("PRAGMA table_info(hello);")
        row = cur.fetchall()
        column_names = [r[1] for r in row]
        print(f"columns names are: {column_names}")

        # fetch rows using iterator
        print("\nusing iterator")
        cur.execute("SELECT * FROM hello LIMIT 5")
        for row in cur:
            print(row)

        # fetch rows using row_factory
        print("\nusing row_factory")
        cur.execute("SELECT * FROM hello LIMIT 5")
        cur.row_factory = sqlite3.Row
        for row in cur:
            print(f"as tuple: {tuple(row)}, as dict: id:{row['id']} a:{row['a']}, b:{row['b']}, c:{row['c']}")

        cur.row_factory = None  # reset row factory
        print("\ngroups of 5 using fetchmany")
        cur.execute("SELECT * FROM hello")
        rows = cur.fetchmany(5)
        while rows:
            for row in rows:
                print(row)
            print("#######  ######  ######")
            rows = cur.fetchmany(5)

    except sqlite3.Error as e:
        print(f"could not fetch rows: {e}")
        exit(1)

    # drop table and close the database
    print("\ndrop table and close connection")
    cur.execute("DROP TABLE IF EXISTS hello")  # cleanup if db is not :memory:
    print("memory cleaned:!")
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
