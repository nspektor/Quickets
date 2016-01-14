import sqlite3

#8b1eef7d82f877bf8e0482fa5aae709c - API TMDB                                  


'''
-display favorites
-delete from favorites
-add to favorites
-recommend one of the now playing movies
   call the now playing fxn from utils
'''

def display_favorites():
'''
display that user's favorites list
'''

def delete():
'''   
delete a movie from the user's favorite list
'''

def add(movie):
'''
input: movie 
adds movie to user's favorite list
'''

def recommend(favorites):
'''
recommends one of the now playing movies based on the genres of the user's 
favorites.
   recommends random playing movie of the genre of whichever genre is most
   common in the users favorites list 
If the user clicks "nope" takes that movie out of the running for
the recommended movie. note: delete the maybe later button, its useless
If there are no more movies and the person rejected all of them, error message
'''

'''
favorites database has to have movie name and genre
'''
