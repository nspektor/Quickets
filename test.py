import requests


payload = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}
r = requests.get("https://api.amctheatres.com/v2/movies/views/now-playing",data=payload)
print r
