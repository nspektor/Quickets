import requests


headers = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}
r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",headers=headers)
q=r.json()
#print q.keys()
#print q['_embedded']
embed=q['_embedded']
movies=embed['movies']
#print movies[0]['name']

movielist=q['_embedded']['movies']
for movie in movielist:
    print movie['name']
#print movielist
#print r
