# module version
__version__ = "3.1.2"

# import sqlite3
try:
    import sqlite3

    have_sqlite3 = True
except ImportError:
    sqlite3 = None
    have_sqlite3 = False

# import mysql
try:
    import mysql.connector as mysql

    have_mysql = True
except ImportError:
    mysql = None
    have_mysql = False


class BWerr(Exception):
    """Simple Error class for WDB"""

    def __init__(self, message):
        self.message = message
        super.__init__(self.message)


class WDB:
    def __init__(self, **kwargs):
        self._db = None
        self._cur = None
        self._dbms = None
        self._database = None

        # populate simple parameters first
        if "user" in kwargs:
            self._user = kwargs["user"]
        else:
            self._user = None
        if "password" in kwargs:
            self._password = kwargs["password"]
        else:
            self._password = None
        if "host" in kwargs:
            self._host = kwargs["host"]
        else:
            self._host = None

        # populate properties
        if "dbms" in kwargs:
            self.dbms = kwargs["dbms"]

        if "database" in kwargs:
            self._database = kwargs["database"]

    # property setters/getters
    def get_dbms(self):
        return self._dbms

    def set_dbms(self, dbms_str):
        if dbms_str == "mysql":
            if have_mysql:
                self._dbms = dbms_str
            else:
                raise BWerr("mysql not available")
        elif dbms_str == "sqlite":
            if have_sqlite3:
                self._dbms = dbms_str
            else:
                raise BWerr("sqlite not available")
        else:
            raise BWerr("set_dbms: invalid dbms_str specified")

    def get_database(self):
        return self._database

    def set_database(self, database):
        self._database = database
        if self._cur:
            self._cur.close()
        if self._db:
            self._db.close()

        self._database = database
        if self._dbms == "sqlite":
            self._db = sqlite3.connect(self._database)
            if self._db is None:
                raise BWerr("set_database: failed to open sqlite database")
            else:
                self._cur = self._db.cursor()
        elif self._dbms == "mysql":
            self._db = mysql.connect(user=self._user, password=self._password,
                                     host=self._host, database=self._database)
            if self._db is None:
                raise BWerr("set_database: failed to connect to mysql")
            else:
                self._cur = self._db.cursor(prepared=True)
        else:
            raise BWerr("set_database: unknown _dbms")

    def get_cursor(self):
        return self._cur

    # properties
    dbms = property(fget=get_dbms, fset=set_dbms)
    database = property(fget=get_database, fset=set_database)
    cursor = property(fget=get_cursor())

    # sql methods ========
    def sql_do_nocommit(self, sql, parms=()):
        """Execute an Sql statement"""
        self._cur.execute(sql, parms)
        return self._cur.rowcount

    def sql_do(self, sql, parms=()):
        """Execute an sql statement"""
        self.sql_do_nocommit(sql, parms)
        self.commit()
        return self._cur.rowcount

    def sql_do_many_nocommit(self, sql, parms=()):
        """Execute an Sql statement over set of data"""
        self._cur.executemany(sql, parms)
        return self._cur.rowcount

    def sql_do_many(self, sql, parms=()):
        self._cur.executemany(sql, parms)
        self.commit()
        return self._cur.rowcount

    def sql_query(self, sql, parms=()):
        self._cur.execute(sql, parms)
        for row in self._cur:
            yield row

    def sql_query_row(self, sql, parms=()):
        self._cur.execute(sql, parms)
        row = self._cur.fetchone()
        self._cur.fetchall()
        return row

    def sql_query_value(self, sql, parms=()):
        return self.sql_query_row(sql, parms)[0]

    # Utilities   ============
