import requests
import pickle

####
# Pull top 250 movies from IMBD
response = requests.get('https://imdb-api.com/en/API/Top250Movies/APIKEY')


# Convert into JSON format
r = response.json()


# Extract information we need from dictionary to list
items = r['items'][0:251]
movies = []
for item in items:
    movie = item['title']
    movies.append(movie)
pickle.dump(movies, open('movies', 'wb'))
