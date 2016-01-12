import sqlite3
from time import time

# input: username, hash (hexstring) of user's password
# returns: true if the username is NOT in the database, and a user is created
# returns; false if the username has been taken
def newUser(username, passwordHash):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q="""
    SELECT users.username
    FROM users
    WHERE users.username = ?
    """
    usernames = c.execute(q, (username,)).fetchall()
    if len(usernames) == 0:
        q="INSERT INTO users VALUES (?,?)"
        c.execute(q, (username, passwordHash))
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

def getStory(storyID):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.sentence
           FROM stories
           WHERE stories.id = ?
           ORDER BY time"""
    result = c.execute(q, (storyID,)).fetchall()
    if len(result) == 0:
        return ""
    else:
        story = []
        for i in result:
            story.append(i[0])
        return story
    #TESTED: works

def addSentence(storyID, sentence, author):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """INSERT INTO stories VALUES (?, ?, ?, ?)"""
    c.execute(q, (storyID, sentence, author, int(time())))
    conn.commit()
    #TESTED Works

# return a list of favorite story ids
#def getFavorites(username):
#    conn = sqlite3.connect("infos.db")
#    c = conn.cursor()
#
#    stories = []
#    q = """SELECT favorites.id
#           FROM favorites
#           WHERE favorites.username = '%s'""" % (username)
#    result = c.execute(q).fetchall()
#    return result

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

def getUniqueUsers(storyID):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.author
           FROM stories
           WHERE stories.id = ?
           """
    result = c.execute(q, (storyID,)).fetchall()
    result = set(result)
    result = list(result)
    return result


def getNumStories():
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.id
           FROM stories
           """
    result = c.execute(q).fetchall()
    length=len(set(result))
    return length;

def getStoryIDsByTime():
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.id
           FROM stories
           ORDER BY stories.time DESC
           """
    result = c.execute(q).fetchall()
# unique-ify the result, but keep the order
    uqList = []
    for el in result:
        if el[0] not in uqList:
            uqList.append(el[0])
    return uqList

def getFavorites(username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()


    stories = []
    q = """SELECT favorites.id
           FROM favorites
           WHERE favorites.username = ?"""

    result = c.execute(q, (username,)).fetchall()
    return result

def getEditedFavorites(username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    result = getStoryIDsByTime()

    stories = []
    q = """SELECT favorites.id
           FROM favorites
           WHERE favorites.username = ?"""

    idList = c.execute(q, (username,)).fetchall()
    editedFaves = []
    for el in idList:
        lastEdit = getLastEditTime(el[0])
        q = """SELECT stories.time
               FROM stories
               WHERE stories.author = ? AND stories.id = ?
               ORDER BY stories.time DESC"""
        myLastEdit = c.execute(q, (username, el[0])).fetchall()
        if len(myLastEdit) > 0:
            myLastEdit = myLastEdit[0][0]
            if lastEdit > myLastEdit:
                editedFaves.append(el)
        else:
            editedFaves.append(el)
    return editedFaves
# input: author
# returns: a list of storyids that the author contributed to sorted in order of
# last time he edited them
def getStoriesByContributor(contributor):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.id
           FROM stories
           WHERE author=?
           ORDER BY stories.time DESC
           """

    result = c.execute(q, (contributor,)).fetchall()
    uqList = []
    for el in result:
        uqList.append(el[0])
    return uqList

def getLastEditTime(storyID):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.time
           FROM stories
           WHERE stories.id=?
           ORDER BY stories.time DESC"""

    result = c.execute(q, (storyID,)).fetchall()
    return result[0][0]

def getLastEditor(storyID):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.author
           FROM stories
           WHERE stories.id=?
           ORDER BY stories.time DESC"""

    result = c.execute(q, (storyID,)).fetchall()
    return result[0][0]
