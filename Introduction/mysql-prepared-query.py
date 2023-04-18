# prepared statement query
import mysql.connector as mysql

HOST = "localhost"
USER = "zahed"
PASSWORD = "########"


def main():
    db = mysql.connect(host=HOST, user=USER, password=PASSWORD,
                       database="scratch")
    cur = db.cursor(prepared=True)

    cur.execute("CREATE TABLE IF NOT EXISTS temp1 (a TEXT, b TEXT, c TEXT)")

    values = (
        ('one', 'two', 'three'),
        ('two', 'three', 'four'),
        ('four', 'five', 'six'),
        ('six', 'seven', 'eight'),
        ('eight', 'nine', 'ten')
    )
    insert_statement = "INSERT INTO temp1 VALUES (?, ?, ?)"
    cur.executemany(insert_statement, values)
    db.commit()

    cur.execute("SELECT * FROM temp1")
    for row in cur:
        print(row)

    query = "SELECT * FROM temp1 WHERE a = ?"
    cur.execute(query, ("four",))

    for row in cur:
        print(f"result is: {row}")

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
