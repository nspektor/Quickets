import sqlite3
import utils

#8b1eef7d82f877bf8e0482fa5aae709c - API TMDB                                  


'''
-display favorites
-delete from favorites
-add to favorites
-recommend one of the now playing movies
   call the now playing fxn from utils
'''

'''
display that user's favorites list
'''
#def display_favorites():

'''   
delete a movie from the user's favorite list
'''
#def delete():

'''
input: movie 
adds movie to user's favorite list
'''
#def add(movie):

'''
recommends one of the now playing movies based on the user's favorite genres
If the user clicks "nope" takes that movie out of the running for
the recommended movie. note: delete the maybe later button, its useless
If there are no more movies and the person rejected all of them, error message
'''
def recommend(favorites):
    listSize=len(favorites)
    uniqs=set(favorites)
    for el in uniqs:
        print el
    
'''
favorites database has to have movie name and genre
'''

favgens=['action', 'comedy', 'horror', 'horror']
recommend(favgens)
