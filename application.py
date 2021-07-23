import os
import requests
import random
import time

from flask import Flask, session, render_template, request, jsonify, redirect, flash, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date
from random import randrange

from mollie.api.client import Client
from mollie.api.error import Error

app = Flask(__name__)

# Initializing mollie api
mollie_client = Client()
mollie_client.set_api_key('test_w4rQfuj6qypyatUz78zf2R5ynSzp2h')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    """ Load the index page. """
    return render_template("index.html")

@app.route('/quiz')
def quiz():
    """ Show the quiz. """
    # User must be logged in
    if session["username"] == "":
        return redirect("/login")

    # Get the genres from the database and choose 4 random genres per question
    genres = db.execute("SELECT * FROM genres").fetchall()
    genres_q1 = [random.choice(genres) for _ in range(4)]
    genres_q3 = [random.choice(genres) for _ in range(4)]

    information_posters = []
    information_posters_q3 = []

    # Get poster genres question 1 from api.
    for genre in genres_q1:
        res = requests.get(f" https://api.themoviedb.org/3/discover/movie?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={genre[0]}")
        if res.status_code !=200:
            raise Exception("ERROR: API request unsuccessful.")
        data = res.json()
        information_posters.append(data["results"][randrange(20)]["poster_path"])

    # Get poster genres question 3
    for genre in genres_q3:
        res = requests.get(f" https://api.themoviedb.org/3/discover/movie?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&sort_by=revenue.desc&include_adult=false&include_video=false&page=1&with_genres={genre[0]}")
        if res.status_code !=200:
            raise Exception("ERROR: API request unsuccessful.")
        data = res.json()
        information_posters_q3.append(data["results"][randrange(20)]["poster_path"])

    return render_template("quiz.html", information_posters_q3=information_posters_q3, information_posters=information_posters, genres_q1=genres_q1, genres_q3=genres_q3)

@app.route('/results', methods=["POST"])
def results():
    """ Show the results of the quiz. """
    # User must be logged in
    if session["username"] == "":
        return redirect("/login")

    # Get the data from the quiz
    genre_q1 = request.form.get("question1")
    decade = request.form.get("question2")
    genre_q2 = request.form.get("question3")
    personality = request.form.get("question4")
    language = request.form.get("question5")

    # Insert the results into the results table in database
    username = session["username"]
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    user_id = user[0]
    results = db.execute("INSERT INTO results (user_id, genre1, genre2, decade, language) VALUES (:user_id, :genre_q1, :genre_q2, :decade, :language)",
            {"user_id": user_id, "genre_q1": genre_q1, "genre_q2": genre_q2, "decade": decade, "language": language})
    db.commit()

    # Get already watched movies
    watchedmovies = db.execute("SELECT * FROM watchedmovies WHERE user_id= :user_id", {"user_id": user_id}).fetchall()
    
    # Get genres to use in the html page (on which the quiz is based)
    genres = db.execute("SELECT * FROM genres")

    # Get API information.
    res = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&sort_by={personality}&include_adult=false&include_video=false&page=1&{decade}&with_genres={genre_q1}%2C{genre_q2}&with_original_language={language}")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()

    # Get the results but remove the already watched movies
    information = []
    for movie in watchedmovies:
        for item in data["results"]:
            if int(item["id"]) != int(movie[1]):
                information.append(item)
            else:
                information.remove(item)
    
    # Genre1 and genre2 are the genres used for the results (displayed on html page)
    for genre in genres:
        if int(genre[0]) == int(genre_q1):
            genre1 = genre[1]
        if int(genre[0]) == int(genre_q2):
            genre2 = genre[1]

    return render_template("results.html", watchedmovies=watchedmovies, results=results, genres=genres, genre1=genre1, genre2=genre2, information=information)

@app.route('/movie/<movie_id>')
def movie(movie_id):
    """ Shows information about the movie """
    # User must be logged in
    if session["username"] == "":
        return redirect("/login")

    # Make sure the movie exists and get data.
    res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()

    if data is None:
        return render_template("error.html", message="The book is not found.")

    # Get the reviews
    res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&page=1")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    datareviews = res.json()

    reviewsapi = []
    for item in datareviews["results"]:
        reviewsapi.append(item)

    # Get the trailers
    res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=718d65a1e9807be576db8d5a6a3f622a&append_to_response=videos")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    trailerdata = res.json()

    trailer = []
    for item in trailerdata["videos"]["results"]:
        trailer.append(item)
    key = trailer[0]['key']

    # Get the actors
    res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=718d65a1e9807be576db8d5a6a3f622a")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    actordata = res.json()

    actors = []
    for item in actordata["cast"]:
        actors.append(item["name"])

    reviews = db.execute("SELECT * FROM reviews WHERE movie_id= :movie_id", {"movie_id": movie_id}).fetchall()
    users = db.execute("SELECT * FROM users")

    # Watched movies     
    username = session["username"]
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    user_id = user[0]
    watched = db.execute("SELECT * FROM watchedmovies WHERE movie_id= :movie_id AND user_id= :user_id", {"movie_id": movie_id, "user_id": user_id}).fetchone()

    return render_template("movie.html", watched=watched, actors=actors, reviews=reviews, users=users, data=data, reviewsapi=reviewsapi, key=key, movie_id=movie_id)

@app.route('/movie/alreadywatched/<movie_id>', methods=["POST"])
def alreadywatched(movie_id):
    """ Get information if already watched the movie. """
    # Insert the movie into alreadywatched database
    username = session["username"]
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    user_id = user[0]

    # Get the poster
    res = requests.get(f" https://api.themoviedb.org/3/movie/{movie_id}?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    poster = data["poster_path"]

    # Insert the movie into the watchedmovies table in the database
    db.execute("INSERT INTO watchedmovies (movie_id, user_id, poster) VALUES (:movie_id, :user_id, :poster)",
            {"movie_id": movie_id, "user_id": user_id, "poster": poster})
    db.commit()

    return redirect(f'/movie/{movie_id}')

@app.route('/movie/<movie_id>', methods=["POST"])
def submit(movie_id):
    """Submit a review."""
    # User must be logged in
    if session["username"] == "":
        return redirect("/login")

    # Get form information
    review = request.form.get("review")
    rating = request.form.get("star")
    
    username = session["username"]
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    user_id = user[0]

    # Users should not be able to review twice
    if db.execute("SELECT * FROM reviews WHERE movie_id= :movie_id AND user_id= :user_id", {"movie_id": movie_id, "user_id": user_id}).rowcount != 0:
        return render_template("error.html", message="You cannot review this movie twice.")
    
    # Insert the review into the database
    db.execute("INSERT INTO reviews (review, movie_id, user_id, rating) VALUES (:review, :movie_id, :user_id, :rating)",
            {"review": review, "movie_id": movie_id, "user_id": user_id, "rating": rating})
    db.commit()

    return redirect(f'/movie/{movie_id}')

@app.route('/search')
def search():
    """ Show the search page. """
    return render_template("search.html")

@app.route('/search/results', methods=["POST", "GET"])
def searchresults():
    """ Show the results of the search. """
    # Get information from the form
    search = request.form.get("movie_info")
    detail = request.form.get("detail")
    information = []

    # Search the movie database based on title
    if detail == "title":
        res = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&query={search}&page=1&include_adult=false")
        if res.status_code !=200:
                raise Exception("ERROR: API request unsuccessful.")
        data = res.json()
    
    # Search the movie database based on year
    if detail == "year":
        res = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&primary_release_year={search}")
        if res.status_code !=200:
                raise Exception("ERROR: API request unsuccessful.")
        data = res.json()

    # Get the right information from the JSON
    for item in data["results"]:
            information.append(item)
    
    return render_template("searchresults.html", information=information)

@app.route('/personal')
def personal():
    """ Show the personal information of the user. """

    # Get personal information from database
    username = session["username"]
    users = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    user_id = users[0]
    resultsquiz = db.execute("SELECT COUNT(*) FROM results WHERE user_id= :user_id",{"user_id": user_id}).fetchone()
    amountreviews = db.execute("SELECT COUNT(*) FROM reviews WHERE user_id= :user_id",{"user_id": user_id}).fetchone()
    
    # Get the favourite genre of the user based on past results of the quiz
    genres = db.execute("SELECT * FROM genres")
    favouritegenre1 = db.execute("SELECT genre1, COUNT(*) as Total FROM results WHERE user_id= :user_id GROUP BY genre1 ORDER BY Total DESC", {"user_id": user_id}).fetchall()
    favouritegenre2 = db.execute("SELECT genre2, COUNT(*) as Total FROM results WHERE user_id= :user_id GROUP BY genre2 ORDER BY Total DESC", {"user_id": user_id}).fetchall()

    if favouritegenre1 == [] or favouritegenre2 == []:
        favouritegenre = "Not yet determined"
    else:
        if favouritegenre1[0][1] >= favouritegenre2[0][1]:
            favouritegenre = favouritegenre1[0][0]
        else:
            favouritegenre = favouritegenre2[0][0]

    # Get already watched movies
    watchedmovies = db.execute("SELECT * FROM watchedmovies WHERE user_id= :user_id", {"user_id": user_id}).fetchall()

    return render_template("personal.html", genres=genres, favouritegenre=favouritegenre, watchedmovies=watchedmovies, users=users, resultsquiz=resultsquiz, amountreviews=amountreviews)

@app.route('/upcoming')
def upcoming():
    """ Show the information of upcoming movies. """
    # Get the infromation of upcoming movies from API
    res = requests.get("https://api.themoviedb.org/3/movie/upcoming?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&page=1")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()

    information = []
    for item in data["results"]:
        information.append(item)

    return render_template("upcoming.html", information=information)

@app.route('/popular')
def popular():
    """ Show the information of popular movies. """
    # Get the infromation of popular movies from API
    res = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=718d65a1e9807be576db8d5a6a3f622a&language=en-US&page=1")
    if res.status_code !=200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()

    information = []
    for item in data["results"]:
        information.append(item)

    return render_template("popular.html", information=information)

@app.route('/login')
def login():
    """Show login page."""
    return render_template("login.html")

@app.route("/login/success", methods=["POST"])
def logincheck():
    """Check if login was a success."""
    # Get form information
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if the username and password are the same as in database
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount != 1:
        flash("Username does not exist and/or wrong password")
        return redirect(url_for('login'))
    
    # Change the session of the user to true (logged in)
    session["username"] = username
    return redirect(url_for('quiz'))

@app.route('/signup')
def signup():
    """Show signup page."""
    return render_template("signup.html")

@app.route("/signup/success", methods=["POST"])
def signupcheck():
    """Check if registration was a success."""

    # Get form information
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    date_of_birth = request.form.get("date_of_birth")
    created_at = date.today()

    # Check if the username is not already taken and then commit
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
        flash('Username already exists')
        return redirect(url_for('signup'))
    db.execute("INSERT INTO users (username, password, email, date_of_birth, created_at) VALUES (:username, :password, :email, :date_of_birth, :created_at)",
            {"username": username, "password": password, "email": email, "date_of_birth": date_of_birth, "created_at": created_at})
    db.commit()

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Logout of the user."""
    session["username"] = ""
    return redirect(url_for('index'))

@app.route('/mollie/<movie_id>', methods=["POST"])
def mollie(movie_id):
    """Make the payment for renting the movie."""

    # Create the mollie payment
    payment = mollie_client.payments.create({
    'amount': {
        'currency': 'EUR',
        'value': '10.00' 
    },
    'description': f'Renting movie with id={movie_id}',
    'redirectUrl': f'http://127.0.0.1:5000/movie/rent/{movie_id}',
    'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
})
    # Store the payment id in sessions and go to checkouturl
    paymentid = payment.id
    session['payment'] = paymentid
    return redirect(payment.checkout_url)

@app.route('/movie/rent/<movie_id>')
def rent(movie_id):
    """Show the movie."""

    # Get the payment id from session and check the status
    paymentid = session.get('payment', None)
    status = mollie_client.payments.get(payment_id=paymentid).status

    # If payment is paid, return the movie (actually trailer)
    if status == "paid":

        # Get the trailers
        res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=718d65a1e9807be576db8d5a6a3f622a&append_to_response=videos")
        if res.status_code !=200:
            raise Exception("ERROR: API request unsuccessful.")
        trailerdata = res.json()

        trailer = []
        for item in trailerdata["videos"]["results"]:
            trailer.append(item)
        key = trailer[0]['key']

        return render_template("rent.html", movie_id=movie_id, key=key)
    
    # If payment was not paid, return an error message
    return render_template("error.html", message="Something went wrong with the payment.")