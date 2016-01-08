import requests
import datetime

headers = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}

'''
-list of current movies
list of showtimes for those movies
list of theaters for later finding location
ticket availability
-theaters now playing chosen movie
ordering tickets
'''

#returns list of dictionary entries of currently playing movies in format {name:wwmReleaseNumber}. format is temporary tho
def getNowPlaying():
    global headers
    r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",headers=headers)
    q=r.json()
    movieData=q['_embedded']['movies']
    movieList=[]
    for movie in movieData:
        movieList.append({movie['name']:movie['wwmReleaseNumber']})
    return movieList

#returns list of theatre ids of theatres currently playing movie of a specific wwmReleaseNumber
def getTheatresPlayingMovie(wwm):
    global headers
    link="https://api.amctheatres.com/v2/theatres/views/now-playing/wwm-release-number/"+str(wwm)
    r=requests.get(link, headers=headers)
    q=r.json()
    theatreData=q['_embedded']['theatres']
    theatreList=[]
    for theatre in theatreData:
        theatreList.append(theatre['id'])
    return theatreList

movieno=getNowPlaying()[0][getNowPlaying()[0].keys()[0]]
getTheatresPlayingMovie(movieno)