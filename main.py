import requests
import random
from tkinter import *
from tkinter import simpledialog
import pickle

# Loading Tkinter
window = Tk()
window.title('Movie suggestions!')

# Dictionary to store ratings in. Variable to save the current suggestion.
ratings = pickle.load(open('ratings', 'rb'))
current_suggestion = ''
watched_movies = pickle.load(open('watched movies', 'rb'))
movies = pickle.load(open('movies', 'rb'))
# Helps reset information. When reset requested, reset will be set to True.
reset = False


# Functions for when you click the buttons

# Uses random module to select a random movie from the list. Checks if it has been watched.
def give_movie():
    output.delete(0.0, END)
    suggestion = random.choice(movies)
    global current_suggestion
    current_suggestion = suggestion
    if current_suggestion in watched_movies:
        give_movie()
    output.insert(END, suggestion)


# If user has watched the movie, they can rate it. The rate button saves the title and rating to a dictionary whilst
# removing the movie from the movies list and moves it to the watched_movies list.
def rate_movie():
    if output.get("1.0", 'end-1c') in movies:
        rating = int(simpledialog.askstring('Rate the movie!', 'Rate it out of 100!'))
        ratings[current_suggestion] = rating
        watched_movies.append(current_suggestion)
        movies.remove(current_suggestion)
    else:
        which_movie = int(
            simpledialog.askstring('Which film?', 'Please enter the index of the film you would like to add:'))
        film_choice = which_movie - 1
        print(requested_search[film_choice])
        rating = int(simpledialog.askstring('Rate the movie!', 'Rate it out of 100!'))
        ratings[requested_search[film_choice]] = rating


# Mainly helped with testing, removing the data for a fresh start. Sets reset to True, which clears the two-
# pickle files under watched_movies and ratings and refreshes the movie list with all previously removed titles.
def reset_data():
    answer = simpledialog.askstring('RESET DATA', "Are you sure? All data will be lost! Type 'yes' to continue")
    if answer == 'yes':
        global reset
        reset = True


def show_ratings():
    output.delete(0.0, END)

    for rating, score in ratings.items():
        output.insert(END, f'{rating} - {score}\n')


def search_film():
    output.delete(0.0, END)
    search_request = entry_box.get()
    search_film = requests.get(f'https://imdb-api.com/en/API/SearchMovie/k_u4c57gpn/{search_request}')
    film_r = search_film.json()
    # print(film_r['results'])
    global requested_search
    requested_search = []
    n = 1
    for result in film_r['results']:
        requested_search.append(result['title'] + ' ' + result['description'])
        # output.insert(END, requested_search) #result['title'] + ' ' + result['description'] + '\n'

    for film in requested_search:
        output.insert(END, f'{n}) {film} \n')
        n += 1  # n +  +  film + '\n'
    print(output.get("1.0", 'end-1c'))


# Create label
Label(window,
      text='Movie Manager',
      bg='black',
      fg='white',
      font='none 12 bold').grid(row=0, column=0, sticky=W)

entry_box = Entry(window, width=20)
entry_box.grid(row=2, column=0, sticky=W)
# Create the buttons
Button(window, text='Movie suggestion:', bg='black', fg='white', command=give_movie, width=15).grid(row=3, column=0,
                                                                                                    sticky=W)
Button(window, text='Watched it!', bg='black', fg='white', command=rate_movie, width=15).grid(row=4, column=0, sticky=W)
Button(window, text='Show my ratings!', bg='black', fg='white', command=show_ratings, width=15).grid(row=5, column=0,
                                                                                                     sticky=W)
Button(window, text='RESET', bg='red', fg='white', command=reset_data).grid(row=6, column=0, sticky=W)
Button(window, text='Search for a film:', bg='black', fg='white', command=search_film, width=16).grid(row=1, column=0,
                                                                                                      sticky=W)
# Output text box
output = Text(window, width=50, height=10, wrap=WORD, background='white')
output.grid(row=10, column=0, sticky=W)

window.mainloop()

# Confirms whether to save the data or reset it based off user interaction.
if not reset:
    pickle.dump(movies, open('movies', 'wb'))
    pickle.dump(watched_movies, open('watched movies', 'wb'))
    pickle.dump(ratings, open('ratings', 'wb'))
elif reset:
    ratings = {}
    watched_movies = []
    response = requests.get('https://imdb-api.com/en/API/Top250Movies/APIKEY')
    # Convert into JSON format
    r = response.json()
    items = r['items'][0:251]
    movies = []
    for item in items:
        movie = item['title']
        movies.append(movie)
    pickle.dump(movies, open('movies', 'wb'))
    pickle.dump(watched_movies, open('watched movies', 'wb'))
    pickle.dump(ratings, open('ratings', 'wb'))
print(ratings)

# Fix the GUI - Align and sort the output box
# SQL?
