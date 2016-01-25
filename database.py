import sqlite3
import utils
from time import time

# input: username, hash (hexstring) of user's password
# returns: true if the username is NOT in the database, and a user is created
# returns; false if the username has been taken
def newUser(username, passwordHash, zipcode, state,preference):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q="""
    SELECT *
    FROM users
    WHERE users.username = ?
    """
    usernames = []
    usernames = c.execute(q, (username,)).fetchall()
    if len(usernames) == 0:
        q="INSERT INTO users VALUES (?,?,?,?,?)"
        c.execute(q, (username, passwordHash, zipcode, state,preference))
        conn.commit()
        return True
    else:
        return False
    #TESTED, works right

# input: username-passwordHash pair
# output: true if the pair match, false if the pair does not
def authenticate(uName, passwordHash):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    print passwordHash
    q="""
    SELECT users.username, users.password
    FROM users
    WHERE users.username = ? and users.password = ?
    """
    result = c.execute(q, (uName, passwordHash)).fetchall() # gets it as a list
    if len(result) == 0:
        return False
    else:
        return True;
    #TESTED, works right


# return a list of favorite story ids
def getFavorites(username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    stories = []
    q = """SELECT users.preference
    FROM users
    WHERE users.username = '%s'""" % (username)
    result = c.execute(q).fetchall()
    return result

def changeFavorite(storyID, username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q = """SELECT *
           FROM favorites
           WHERE favorites.username = ? AND favorites.id = ?
           """
    result = c.execute(q, (username, storyID)).fetchall()
# newly favorited
    if len(result) == 0:
        q = """INSERT INTO favorites VALUES (?, ?)"""
        c.execute(q, (storyID, username))
# removes favorite
    else:
        q = """DELETE FROM favorites
               WHERE favorites.username = ? AND favorites.id = ?
            """
        c.execute(q, (username, storyID))
    conn.commit()

def changePass(uname,passw):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q="""UPDATE users SET password=? WHERE users.username=?"""
    c.execute(q,(passw,uname,))
    print passw + "1"
    conn.commit()

def changeZip(uname,zipc):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q="""UPDATE users SET zipcode=? WHERE users.username=?"""
    c.execute(q,(zipc,uname,))
    print zipc + "2"
    conn.commit()

def changeState(uname,state):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q="""UPDATE users SET state=? WHERE users.username='%s'"""
    c.execute(q,(state,uname,))
    print state + "3"
    conn.commit()

def changePref(uname,pref):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q="""UPDATE users SET preference=? WHERE users.username=?"""
    c.execute(q,(pref,uname,))
    print pref + "4"
    conn.commit()

def getInfo(uname):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q = """SELECT *
    FROM users
    WHERE users.username = '%s'""" % (uname)
    result = c.execute(q).fetchall()
    print 'AAAAAAAAAAAAAAAAAAAAAAAAA'
    print result
    return result[0]

#def getEditedFavorites(username):
#    conn = sqlite3.connect("infos.db")
#    c = conn.cursor()
#
#    result = getStoryIDsByTime()
#
#    stories = []
#    q = """SELECT favorites.id
#           FROM favorites
#           WHERE favorites.username = ?"""
#
#    idList = c.execute(q, (username,)).fetchall()
#    editedFaves = []
#    for el in idList:
#        lastEdit = getLastEditTime(el[0])
#        q = """SELECT stories.time
#               FROM stories
#               WHERE stories.author = ? AND stories.id = ?
#        myLastEdit = c.execute(q, (username, el[0])).fetchall()
#        if len(myLastEdit) > 0:
#            myLastEdit = myLastEdit[0][0]
#            if lastEdit > myLastEdit:
#                editedFaves.append(el)
#        else:
#            editedFaves.append(el)
#    return editedFaves
