import sqlite3


"""THIS FILE IS USED TO CREATE THE BACKEND OF THE PROJECT, IT CREATES THE
DATABASE FILE AND CREATES ITS TABLES. ALL FUNCTIONS REGARDING CHANGING THE
DATABASE IS LOCATED AT database.py"""

conn = sqlite3.connect("infos.db")

c = conn.cursor()

q = "CREATE TABLE %s (%s)" # format string for creating tables,
                           # first formatter = name
                           # second formatter = arguments

c.execute(q % ("users", "username TEXT, password TEXT, zipcode TEXT, state TEXT, preference TEXT")) # NOTE: hex string will do fine for hash


c.execute(q % ("favorites", "id INTEGER, username TEXT"))



conn.commit()
