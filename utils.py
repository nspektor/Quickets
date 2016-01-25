import requests
import datetime
import database

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

def getNowPlaying2(username):
    global headers
    r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",headers=headers)
    q=r.json()
    movieData=q['_embedded']['movies']
    #print movieData[0].keys()
    #print movieData[0]['synopsis']
    temp = database.getFavorites(username);
    print temp
    temp = temp[0][0].split()
    temp2 = []
    for i in temp:
        if i == '1':
            temp2.append("adventure")
        elif i == '2':
            temp2.append("animation")
        elif i == '3':
            temp2.append("comedy")
        elif i == '4':
            temp2.append("western")
        elif i == '5':
            temp2.append("special event")
        elif i == '6':
            temp2.append("fantasy")
        elif i == '7':
            temp2.append("musical")
        elif i == '8':
            temp2.append("science fiction")
        elif i == '9':
            temp2.append("film festival")
        elif i == '10':
            temp2.append("suspense")
        elif i == '11':
            temp2.append("family")
        elif i == '12':
            temp2.append("romantic comedy")
        elif i == '13':
            temp2.append("action")
        elif i == '14':
            temp2.append("documentary")
        elif i == '15':
            temp2.append("horror")
        elif i == '16':
            temp2.append("drama")
    movieList=[]
    for movie in movieData:
        if movie['genre'].lower() in temp2:
            movieList.append({'name':movie['name'], 'wwmRN':movie['wwmReleaseNumber'], 'id': movie['id'], 'poster': movie['media']['posterLarge'], 'genre': movie['genre'].lower(), 'blurb': movie['synopsis']})
    for movie in movieData:
        if movie['genre'].lower() not in temp2:
            movieList.append({'name':movie['name'], 'wwmRN':movie['wwmReleaseNumber'], 'id': movie['id'], 'poster': movie['media']['posterLarge'], 'genre': movie['genre'].lower(), 'blurb': movie['synopsis']})
    #print movieList[0]['name']
    #print movieList[0]['genre']
    #print movieList[0]['poster']
    return movieList



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
    #print r
    q=r.json()
    theatreData=q['_embedded']['theatres']
    #print theatreData
    theatreList=[]
    for theatre in theatreData:
        try:
            theatreList.append(theatre['id'])
        except AttributeError:
            print 'doesnt exist'
        except TypeError:
            print 'doesnt exist'
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
    #print len(stateTheatres)
    nearbyZips=getNearbyZips(postalCode, 200)
    #print nearbyZips
    for theatre in stateTheatres:
        tZip=theatre['location']['postalCode'].split('-')[0]
        #tZip=theatre['location']['postalCode']
        #print tZip
        #print theatre['location']['postalCode']
        if tZip in nearbyZips:
            #print theatre['name']
            #print tZip
            #print theatre.keys()
            #if 'westWorldMediaNumber' in theatre.keys():
            #    print 'nearbyZips contains '+theatre['location']['postalCode']
            zipTheatres.append(theatre['id'])
    #print zipTheatres
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
    global headers
    link0='https://api.amctheatres.com/v2/movies/%d' % (int(ID))
    r0=requests.get(link0, headers=headers)
    q0=r0.json()
    movieTitle=q0['name']
    titleList=movieTitle.split(' ')
    name=titleList[-1]
    link='https://api.amctheatres.com/v2/theatres/%d/showtimes/%s/?movie=%s' % (theatreNo, date, name)
    r=requests.get(link, headers=headers)
    q=r.json()
    try:
        showtimeData=q['_embedded']['showtimes']
        #print showtimeData[0]['purchaseUrl']
    #printshowtimeData[0].keys()
        showtimeList = []
        link2='https://api.amctheatres.com/v2/theatres/%d' % (theatreNo)
        r2=requests.get(link2, headers=headers)
        q2=r2.json()
        address=q2['location']['addressLine1']
        theatreName=q2['name']
        #print theatreName
        for show in showtimeData:
            rawtime=show['showDateTimeLocal'].split('T')[1][:-3]
            #print rawtime
            shour=rawtime.split(':')[0]
            sminute=rawtime.split(':')[1]
            rn=datetime.datetime.now()
            chour=rn.hour
            cminute=rn.minute
            if int(shour)<10:
                shour=int(shour[-1])
            if int(sminute)<10:
                sminute=int(sminute[-1])
            #print shour
            #print sminute
            if shour>=chour:
                if sminute>=cminute:
                    showtimeList.append({'theatreName': theatreName, 'time': rawtime, 'avail': str(show['isSoldOut']), 'address': address, 'buy': show['purchaseUrl']})
    #print showtimeList
        return showtimeList
    except KeyError:
        print q['errors'][0]['message']

def idToWWM(ID):
    link0='https://api.amctheatres.com/v2/movies/%d' % (int(ID))
    r0=requests.get(link0, headers=headers)
    q0=r0.json()
    return q0['wwmReleaseNumber']

'''
essentially combines all the other functions: takes a state, postal code, and movie ID to find the showtimes for that movie in nearby theatres
returns list of dictionaries, in the format:
   {'theatreName': name of theatre, 'time': the showtime, 'avail': True/False about ticket availability, 'address': the theatre's address, 'buy': purchase url}
'''
def getShowInfo(state, postalCode, ID):
    movieWWM=idToWWM(ID)
    nearbyTheatres=getZipTheatres(state, postalCode)
    print 'got nearby theatres, here they are'
    print nearbyTheatres
    theatresPlayingMovie=getTheatresPlayingMovie(movieWWM)
    print 'got theatres playing movie, here they are'
    print theatresPlayingMovie
    finalTheatres=[]
    for theatre in nearbyTheatres:
        if theatre in theatresPlayingMovie:
            finalTheatres.append(theatre)
    showtimes=[]
    for theatre in finalTheatres:
        showtimes.append(getTheatreShowtimes(theatre, ID))
    return showtimes

rn=datetime.datetime.now()
#print rn.hour
#print rn.minute
#print (time.strftime("%H:%M:%S"))

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
getTheatreShowtimes(theatresPM[0], testMovie['id'])
#getShowInfo('texas', 73301, testMovie['id'])
