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
    rating = int(simpledialog.askstring('Rate the movie!', 'Rate it out of 100!'))
    ratings[current_suggestion] = rating
    watched_movies.append(current_suggestion)
    movies.remove(current_suggestion)

# Mainly helped with testing, removing the data for a fresh start. Sets reset to True, which clears the two-
# pickle files under watched_movies and ratings and refreshes the movie list with all previously removed titles.
def reset_data():
    answer = simpledialog.askstring('RESET DATA', "Are you sure? All data will be lost! Type 'yes' to continue")
    if answer == 'yes':
        global reset
        reset = True


# Create label
Label(window,
      text='Click the button for a random movie suggestion!',
      bg='black',
      fg='white',
      font='none 12 bold').grid(row=0, column=0, sticky=W)

# Create the buttons
Button(window, text='Click here!', bg='black', fg='white', command=give_movie).grid(row=0, column=1, sticky=E)
Button(window, text='Watched it!', bg='black', fg='white', command=rate_movie).grid(row=1, column=1, sticky=N)
Button(window, text='RESET', bg='red', fg='white', command=reset_data).grid(row=2, column=1, sticky=N)
# Output text box
output = Text(window, width=50, height=10, wrap=WORD, background='white')
output.grid(row=1, column=0, sticky=E)


window.mainloop()

# Confirms whether to save the data or reset it based off user interaction.
if reset == False:
    pickle.dump(movies, open('movies', 'wb'))
    pickle.dump(watched_movies, open('watched movies', 'wb'))
    pickle.dump(ratings, open('ratings', 'wb'))
elif reset == True:
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
