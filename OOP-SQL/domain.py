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

def do_menu():
    while True:
        menue = [
            "A) Add domain",
            "F) Find domain",
            "E) Edit domain",
            "L) List domains",
            "D) Delete domain",
            "X) Drop table and exit",
            "Q) Quit"
        ]I
        print()
        for option in menue:
            print(option)
        response = input("Select an action or Q to quit").upper()
        if len(response) != 1:
            print("\nInput too long or empty")
            continue
        elif response in "AFELDXQ":
            break
        else:
            print("\nInvalid response")
            continue
    return response

def jump(response):
    if response == "A":
        add_domain()
    elif response == "F":
        find_domain()
    elif response == "E":
        edit_domain()
    elif response == "L":
        list_domain()
    elif response == "D":
        delete_domain()
    elif response == "X":
        drop_domain()
    else:
        print("jump: invalid argument")
    return

def add_domain():
    print("Add domain")

def find_domain():
    print("Find domain")

def edit_domain():
    print("Edit domain")

def list_domain():
    print("List domain")

def delete_domain():
    print("Delete domain")

def drop_domain():
    print("Drop domain")



























