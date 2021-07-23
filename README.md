# What to watch by Daphne Westerdijk

I watch a lot of netflix but sometimes it is really hard to find a good movie to watch. This application will give you a list of movies based on your interests/personality. You can then go over the list and see if there is one that sparks your interest. When you click on the movie, you can also watch a trailer to see if it really something you want to watch.

## The problem

Sometimes you want to watch a movie/tv show but you don't know what to watch. Then it would be very handy to get a customize selection of movies based on your interests. 

## The solution

When you open this web application, you will fill out a quick form. After you submit, a table with movies will come up that are related to your interests (based on genres) and have a high rating. When clicking on the movie, you will get more details and a trailer.

## Installation

To install what to watch:
```
$ export FLASK_APP=application.py

$ export FLASK_DEBUG=1

$ export DATABASE_URL=postgres://kxgcyrtctakpzh:a10d1be49564ba126670c0d3b5f378946c991e7a2039dce62c9774c7a6cd3694@ec2-54
-228-209-117.eu-west-1.compute.amazonaws.com:5432/d912pobek628sq
```
Now use `flask run` to run what to watch on your computer.

## The product
Quiz:

![The layout of the quiz.](doc/quiz.jpg) 

Movie page:

![The layout of the moviepage.](doc/movie.jpg)

On the webapp "What to watch" you can fill out a quiz and based on your answers (mood) a list of movies is generated. The quiz is designed to be dynamic, everytime someone opens the quiz they will get to see different posters and the result of the quiz only shows movies that you haven't watched so there is always something new. When you find an interesting movie to watch, you can also rent it through a mollie payment.

## Acknowledgements

1. What to watch uses the flask framework written in Python. (https://palletsprojects.com/p/flask/)
2. The movie information is gathered through the API by The Movie Database (https://www.themoviedb.org/)
3. When renting a movie on what to watch, we use the mollie payment system. (https://github.com/mollie/mollie-api-python)

## Screencast

[![Screencast of what to watch](http://img.youtube.com/vi/8eLmYVytrF4/0.jpg)](http://www.youtube.com/watch?v=8eLmYVytrF4)