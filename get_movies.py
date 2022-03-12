import requests
import pickle

# Pull top 250 movies from IMBD
response = requests.get('https://imdb-api.com/en/API/Top250Movies/k_u4c57gpn')


# Convert into JSON format
r = response.json()


# Extract information we need from dictionary to list
items = r['items'][0:251]
movies = []
for item in items:
    movie = item['title']
    movies.append(movie)
pickle.dump(movies, open('movies', 'wb'))
movie_title = 'Shark Tale'
search_film = requests.get(f'https://imdb-api.com/en/API/SearchMovie/k_u4c57gpn/{movie_title}')
film_r = search_film.json()
# print(film_r['results'])
requested_search = []
for result in film_r['results']:
    print(result['title'] + ' ' + result['description'])
    requested_search.append(result['title']+ ' '  + result['description'])

