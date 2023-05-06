from wdb import BWErr, BWDB

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
        menu = [
            "A) Add domain",
            "F) Find domain",
            "E) Edit domain",
            "L) List domains",
            "D) Delete domain",
            "X) Drop table and exit",
            "Q) Quit",
        ]
        print()
        for option in menu:
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
    db = GLOBASLS["db"]
    if db is None:
        raise BWErr("add_domain: no db object")
    domain = input("Domain name > ")
    description = input("Description > ")
    count = db.add_row([domain, description])
    if count < 1:
        raise BWErr("unable to add domain")
    row_id = db.lastrowid()
    row = db.get_row(row_id)
    print(f"frow added: {row}")


def find_domain(**kwargs):
    print("Find domain")
    if "noprompt" not in kwargs:
        print("Find domain")
    db = GLOBASLS["db"]
    if db is None:
        raise BWErr("find_domain: no db object")
    domain = input("Domain name > ")
    if len(domain) == 0:
        return
    row_id = db.find_row("domain", domain)
    if row_id:
        row = db.get_row(row_id)
        print(f"found: {row}")
        return row_id
    else:
        print("row not found.")
        return None


def edit_domain():
    print("Edit domain")
    db = GLOBASLS["db"]
    if db is None:
        raise BWErr("edit_domain: no db object")
    row_id = find_domain(noprompt=True)
    if row_id is None:
        return
    description = input("Description (leave blank to cancel) > ")
    if len(description) == 0:
        print("Canceled.")
        return
    else:
        db.update_row(row_id, {"description": description})
        row = db.get_row(row_id)
        print(f"Updated row is {row}")


def list_domain():
    print("List domain")


def delete_domain():
    print("Delete domain")


def drop_domain():
    print("Drop domain")
