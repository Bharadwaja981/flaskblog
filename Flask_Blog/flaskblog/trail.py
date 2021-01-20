import sqlite3


conn=sqlite3.connect("site.db")

print("opened db")

conn.execute("CREATE TABLE students (name TEXT  , addr TEXT,city  TEXT, gender TEXT)")

print("table created")

conn.close()


CREATE TABLE "details" (
    "id"    INTEGER,
    "userloginid"    varchar(20),
    "gender"    varchar(60),
    "course"    varchar(60),
    "degree"    varchar(60),
    "country"    varchar(60),
    "intrest1"    varchar(60),
    "intrest2"    varchar(60),
    "intrest3"    varchar(60),
    "intrest4"    varchar(60),
    "intrest5"    varchar(60),
    "lnkdurl"    varchar(120),
    "ghuburl"    varchar(120)
)


CREATE TABLE "user" (
    "id"    INTEGER NOT NULL,
    "firstname"    VARCHAR(20) NOT NULL,
    "lastname"    VARCHAR(20) NOT NULL,
    "email"    VARCHAR(120) NOT NULL,
    "image_file"    VARCHAR(20) NOT NULL,
    "password"    VARCHAR(60) NOT NULL,
    "collegeid"    VARCHAR(20) NOT NULL,
    "profession"    VARCHAR(20) NOT NULL,
    "userloginid"    VARCHAR(10),
    PRIMARY KEY("id"),
    UNIQUE("email"),
    UNIQUE("collegeid"),
    UNIQUE("profession"),
    UNIQUE("firstname"),
    UNIQUE("lastname")
)
