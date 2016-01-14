import requests
import datetime

headers = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}
stateTheatres=[] #list of nearby theatre wwm numbers
zipTheatres=[]
#nearbyZips=[]
'''
-list of current movies
list of showtimes for those movies
list of theaters for later finding location
ticket availability
-theaters now playing chosen movie
ordering tickets
'''

#returns list of dictionary entries of currently playing movies in format {name:name, wwmRN:wwmReleaseNumber, id: id}. format is temporary tho
def getNowPlaying():
    global headers
    r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",headers=headers)
    q=r.json()
    movieData=q['_embedded']['movies']
    print movieData[0].keys()
    movieList=[]
    for movie in movieData:
        movieList.append({'name':movie['name'], 'wwmRN':movie['wwmReleaseNumber'], 'id': movie['id']})
    return movieList

#returns list of theatre ids of theatres currently playing movie of a specific wwmReleaseNumber
def getTheatresPlayingMovie(wwm):
    global headers
    link="https://api.amctheatres.com/v2/theatres/views/now-playing/wwm-release-number/"+str(wwm)
    r=requests.get(link, headers=headers)
    print r
    q=r.json()
    theatreData=q['_embedded']['theatres']
    theatreList=[]
    for theatre in theatreData:
        theatreList.append(theatre['id'])
    return theatreList

def getZipTheatres(state, postalCode):
    link='https://api.amctheatres.com/v2/theatres?page-size=100&state=%s'
    link=link % (state)
    global headers
    r=requests.get(link, headers=headers)
    q=r.json()
    theatreData=q['_embedded']['theatres']
    #print theatreData[0].keys()
    global stateTheatres
    for theatre in theatreData:
        #print theatre['slug']
        try:
            #print theatre['name']
            stateTheatres.append(theatre)
            #print theatre['location']['state']
        except KeyError:
            print "This theatre is a butt"
   # print len(stateTheatres)
    nearbyZips=getNearbyZips(postalCode, 10)
    #print stateTheatres
    global zipTheatres
    for theatre in stateTheatres:
        tZip=theatre['location']['postalCode'].split('-')[0]
        #print tZip
        #print theatre['location']['postalCode']
        if tZip in nearbyZips:
            print theatre['name']
            print tZip
            #print theatre.keys()
            if 'westWorldMediaNumber' in theatre.keys():
                print 'nearbyZips contains '+theatre['location']['postalCode']
                zipTheatres.append(theatre['westWorldMediaNumber'])
            '''try:
                print 'nearbyZips contains '+theatre['location']['postalCode']
                zipTheatres.append(theatre['westWorldMediaNumber'])
                print zipTheatres
            except KeyError:
                print "This theatre is a butt again, at "+theatre['location']['postalCode']'''
    print zipTheatres

def getNearbyZips(postalCode, radius):
    link='https://www.zipcodeapi.com/rest/XhcSg7FLPZcNBWPWCEfwKhmDQMea9IL7ZXZg5F1UEeHfbxcOcrkWJHAAtPKDxvKw/radius.json/%d/%d/mile'
    link = link % (postalCode, radius)
    r=requests.get(link)
    q=r.json()
    #print q.keys()
    #print q['error_msg']
    zipData=q['zip_codes']
    zipList=[]
    for zipper in zipData:
        zipList.append(zipper['zip_code'])
    #global nearbyZips
    #nearbyZips=zipList
    return zipList
    #print nearbyZips
    
    
def getTheatreShowtimes(theatreNo, movieTitle):
    rn=datetime.datetime.now()
    date=str(rn.month)+'-'+str(rn.day)+'-'+str(rn.year)
    titleList=movieTitle.split(' ')
    name=titleList[-1]
    link='https://api.amctheatres.com/v2/theatres/%d/showtimes/%s/?movie=%s' % (theatreNo, date, name)
    global headers
    r=requests.get(link, headers=headers)
    q=r.json()
    showtimeData=q['_embedded']['showtimes']
    print showtimeData[0].keys()
    #print showtimeData[0].keys()
    #for i in showtimeData:
        #print i['showDateTimeLocal']

        
def getMovieAvailability(theatreNo, movieTitle):
    rn=datetime.datetime.now()
    date=str(rn.month)+'-'+str(rn.day)+'-'+str(rn.year)
    titleList=movieTitle.split(' ')
    name=titleList[-1]
    link='https://api.amctheatres.com/v2/theatres/%d/showtimes/%s/?movie=%s' % (theatreNo, date, name)
    global headers
    r=requests.get(link, headers=headers)
    q=r.json()
    print q.keys()
    
#movieno=getNowPlaying()[0][getNowPlaying()[0].keys()[0]]
#getTheatresPlayingMovie(movieno)
#getTheatreShowtimes(610, 'The Danish girl')

#getNearbyZips(10282, 5)
#getZipTheatres('new-york', 10011)
testMovie=getNowPlaying()[0]
print testMovie
theatresPM=getTheatresPlayingMovie(testMovie['wwmRN'])
print theatresPM
#getTheatreShowtimes(theatreNo[0], testMovie['title'])
