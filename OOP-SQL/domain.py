from wdb import BWErr,BWDB


GLOBASLS = {}

def connect():
    try:
        db = BWDB(dbms="sqlite", database="../db/scratch.db", table="domains")
        print(f"BWDB version {db.version()}")
        print(f"dbms is {db.dbms}")
    except BWErr as error:
        db = None
        print(f"Error: {error}")
        exit(1)

    GLOBASLS["db"] = db
    return db

























