from wdb import BWErr, BWDB


MY_HOST = "127.0.0.1"
MY_USER = "zahed"
MY_PASSWORD = "##########"

def main():
    try:
        db = BWDB(dbms="sqlite", database="../db/scratch.db")
        # db = BWDB(dbms="mysql", host=MY_HOST, user=MY_USER, password=MY_PASSWORD,database="scratch")
        print(f"BWDB version {db.version()}")
        print(f"dbms is: {db.dbms}\n")

        # start clean
        db.sql_do("DROP TABLE IF EXISTS temp")

        print("create a table")
        if db.dbms == "sqlite":
            create_table = """
            CREATE TABLE IF NOT EXISTS temp (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
            )
            """
        elif db.dbms == "mysql":
            create_table = """
            CREATE TABLE IF NOT EXISTS temp (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            description VARCHAR(128)
            ) 
            """
        else:
            raise BWErr("create table: unknown dbms")

        # create and set the table
        db.sql_do(create_table)
        db.table = "temp"
        print(f"table columns: {db.column_names()}\n")

        print("populate table")
        insert_rows = [
            ("Jimi Hendrix", "Guitar"),
            ("Miles Davis", "Trumpet"),
            ("Billy Cobham", "Drums"),
            ("Charlie Bird", "Saxophone"),
            ("Oscar Peterson", "Piano"),
            ("Marcus Miller", "Bass")
        ]

        for row in insert_rows:
            db.add_row_nocommit(row)
        db.commit()
        print(f"added {len(insert_rows)} rows")

        for row in db.get_rows():
            print(row)
        print()
        print("find more than one row (%s%)")
        row_ids = db.find_rows("name", "%s%")
        print(f"found {len(row_ids)} rows")
        for row_id in row_ids:
            print(db.get_row(row_id))
        print()
        print("search for %Bird%")
        if row_id > 0:
            print(f"found row {row_id}")
            print(db.get_row(row_id))

        print()
        print(f"update row {row_id}")
        numrows = db.update_row(row_id, {"name":"The Bird"})
        print(f"{numrows} row(s) modified")
        print(db.get_row(row_id))

        print()
        print("add a row")
        numrows = db.add_row(["Bob Dylan", "Harmonica"])
        row_id = db.lastrowid()
        print(f"{numrows} row added (row {row_id}")
        print(db.get_row(row_id))






