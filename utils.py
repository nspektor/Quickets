import requests
import datetime

headers = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}
#stateTheatres=[] #list of nearby theatre wwm numbers
#zipTheatres=[]
#nearbyZips=[]
'''
-list of current movies
list of showtimes for those movies
list of theaters for later finding location
ticket availability
-theaters now playing chosen movie
ordering tickets
'''

def buyTickets():
    global headers
    rn=datetime.datetime.now()
    date=str(rn.month)+'-'+str(rn.day)+'-'+str(rn.year)
    link="https://api.amctheatres.com/v2/theatres/610/showtimes/%s"%(date)
    r=requests.get(link, headers=headers)
    q=r.json()
    #print q
    showtimeData=q['_embedded']['showtimes']
    #print showtimeData
    showtime=showtimeData[0]
    sku=showtime['ticketPrices'][0]['sku']
    p=requests.post('https://api.amctheatres.com/v2/orders', headers=headers,data={'email':'developers@amctheatres.com'})
    print p.reason
    #print sku
    
#buyTickets()

'''
returns list of movies currently playing in theatres, as a list of dictionaries
format:
   {'name': movie name, 'wwmRN': movie's wwmReleaseNumber, 'id': movie's id, 'poster': poster URL, 'genre': movie's genre, 'blurb': movie's synopsis}

'''
def getNowPlaying():
    global headers
    r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",headers=headers)
    q=r.json()
    movieData=q['_embedded']['movies']
    #print movieData[0].keys()
    #print movieData[0]['synopsis']
    movieList=[]
    for movie in movieData:
        movieList.append({'name':movie['name'], 'wwmRN':movie['wwmReleaseNumber'], 'id': movie['id'], 'poster': movie['media']['posterLarge'], 'genre': movie['genre'].lower(), 'blurb': movie['synopsis']})
    #print movieList[0]['name']
    #print movieList[0]['genre']
    #print movieList[0]['poster']
    return movieList

#getNowPlaying()

'''
takes movie's wwm number
returns list of theatre ids of theatres playing that movie
to be used with getZipTheatres to get theatres playing certain movie near person's location
also returns value for use by getTheatreShowtimes and getMovieAvailability
'''
def getTheatresPlayingMovie(wwm):
    global headers
    link="https://api.amctheatres.com/v2/theatres/views/now-playing/wwm-release-number/%d?page-size=100" % (wwm)
    r=requests.get(link, headers=headers)
    print r
    q=r.json()
    theatreData=q['_embedded']['theatres']
    theatreList=[]
    for theatre in theatreData:
        theatreList.append(theatre['id'])
    return theatreList

'''
takes state and postal code
returns list of wwm numbers for theatres within certain radius of zipcode in that state
uses state for initial api call to find all theatres in a state
uses postalcode for getNearbyZips
'''
def getZipTheatres(state, postalCode):
    zipTheatres=[]
    link='https://api.amctheatres.com/v2/theatres?page-size=100&state=%s'
    link=link % (state)
    global headers
    r=requests.get(link, headers=headers)
    q=r.json()
    theatreData=q['_embedded']['theatres']
    stateTheatres=[]
    '''for theatre in theatreData:
        try:
            stateTheatres.append(theatre)
        except KeyError:
            print "This theatre is a butt"'''
    for theatre in theatreData:
        stateTheatres.append(theatre)
    print len(stateTheatres)
    nearbyZips=getNearbyZips(postalCode, 100)
    #print nearbyZips
    for theatre in stateTheatres:
        tZip=theatre['location']['postalCode'].split('-')[0]
        #tZip=theatre['location']['postalCode']
        print tZip
        #print theatre['location']['postalCode']
        if tZip in nearbyZips:
            #print theatre['name']
            #print tZip
            #print theatre.keys()
            #if 'westWorldMediaNumber' in theatre.keys():
            #    print 'nearbyZips contains '+theatre['location']['postalCode']
            zipTheatres.append(theatre['id'])
    print zipTheatres
    return zipTheatres


'''
takes a postal code and radius
returns list of zipcodes in that radius
to be used to find nearby theatres in getZipTheatres
'''
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

#getZipTheatres('new-york', 11235)
    
def getTheatreShowtimes(theatreNo, ID):
    rn=datetime.datetime.now()
    date=str(rn.month)+'-'+str(rn.day)+'-'+str(rn.year)
    
    link0='https://api.amctheatres.com/v2/movies/%d' % (ID)
    r0=requests.get(link0, headers=headers)
    q0=r0.json()
    movieTitle=q0['name']
    titleList=movieTitle.split(' ')
    name=titleList[-1]
    link='https://api.amctheatres.com/v2/theatres/%d/showtimes/%s/?movie=%s' % (theatreNo, date, name)
    global headers
    r=requests.get(link, headers=headers)
    q=r.json()
    print q
    try:
        showtimeData=q['_embedded']['showtimes']
    #print showtimeData[0].keys()
    #print showtimeData[0].keys()
        showtimeList = []
        link2='https://api.amctheatres.com/v2/theatres/%d' % (theatreNo)
        r2=requests.get(link2, headers=headers)
        q2=r2.json()
        theatreName=q2['name']
        #print theatreName
        for show in showtimeData:
        #print i['showDateTimeLocal']
            showtimeList.append({'theatreName': theatreName, 'time': show['showDateTimeLocal'], 'avail': show['isSoldOut']})
    #print showtimeList
        return showtimeList
    except KeyError:
        print q['errors'][0]['message']

def idToWWM(ID):
    link0='https://api.amctheatres.com/v2/movies/%d' % (ID)
    r0=requests.get(link0, headers=headers)
    q0=r0.json()
    return q0['wwmReleaseNumber']

def getShowInfo(state, postalCode, ID):
    movieWWM=idToWWM(ID)
    nearbyTheatres=getZipTheatres(state, postalCode)
    print 'nearbyTheatres: '
    print nearbyTheatres
    theatresPlayingMovie=getTheatresPlayingMovie(movieWWM)
    print 'theatresPlayingMovie: '
    print theatresPlayingMovie
    finalTheatres=[]
    for theatre in nearbyTheatres:
        print theatre
        if theatre in theatresPlayingMovie:
            print 'its in!'
            finalTheatres.append(theatre)
    print 'finals'
    print finalTheatres
    showtimes=[]
    for theatre in finalTheatres:
        #print getTheatreShowtimes(theatre, ID)
        showtimes.append(getTheatreShowtimes(theatre, ID))
    print showtimes
    
    
#movieno=getNowPlaying()[0][getNowPlaying()[0].keys()[0]]
#getTheatresPlayingMovie(movieno)


#getNearbyZips(10282, 5)
#getZipTheatres('new-york', 10011)
testMovie=getNowPlaying()[0]
#idToWWM(testMovie['id'])
#print testMovie
theatresPM=getTheatresPlayingMovie(testMovie['wwmRN'])
#print theatresPM
#print 'theatreNo: '+str(theatresPM[0])
#print 'title: '+testMovie['name']
#getTheatreShowtimes(theatresPM[0], testMovie['id'])
getShowInfo('texas', 73301, testMovie['id'])
