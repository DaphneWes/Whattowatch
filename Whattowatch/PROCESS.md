Per day I will update this document on the following:
1. The choices I made
2. What I expect to happen as a result of those choices
3. Why I think those things will happen

Date: 13 - 05 - 2020

I finished the proposal + design and started with making the databases.

Date: 14 - 05 - 2020

I started with making all the different pages.
I changed the username from the reviews database to user_id because then you can use it as a Foreign key. It is then easier to see the connection. Also, I deleted the id in the genre database because it was redundant (because there is already a genre_id)

Date: 15 - 05 - 2020

I continued with the pages and implemented the sign up and login pages. In the quiz / results pages (minimal) are still bugs and are therefore not fully functional yet.

Date: 18 - 05 - 2020

The quiz (with 1 question) now runs smoothly and the result page shows the right information as well as links to the specific movie pages. All results now have a specific movie page with more information and reviews. The only thing that is not working yet are the trailers ("Firefox heeft voorkomen dat de pagina in deze context werd geladen, omdat de pagina een beleid voor X-Frame-Options heeft dat dit niet toestaat.")

I've also implemented a search function but it only works with the title. (the button is not responding correctly either but submitting through enter does work)

I have added a javascript function to go back one page in history so that you do not lose your result page. I did it with the help of: https://www.w3schools.com/jsref/met_his_back.asp

Date: 19 - 05 - 2020

I extended the quiz with 2 genres and decade option. The quiz is now more dynamic because the posters shown in the first question change everytime the page opens as well as the genres. The users can now also review movie and this will be displayed on the page. The personal page now shows how many reviews the user wrote and how many times they did the quiz.

No changes were made in respect to the design.md

Date: 20 - 05 - 2020

I applied some CSS to make the webapp look a little better. The pages popular and upcoming are also added and styled. The movie pages are also more elaborate (trailer and actors)

I think the quiz is not gonna have as many questions as I would have liked but the quiz page will be very dynamic through randomized poster pages as well as genres that are shown. If I have enough time I would like to implement the already watched button on the movie page so that we could exclude that from the result pages (after the quiz). This would make it even more dynamic.

Date: 21 - 05 - 2020

The movie pages now have a button that you can press if you've already seen that movie. This information is uploaded to the database and is also shown on your personal page. The quiz is also more elaborate and has now 4 questions.

I think there is not enough time to make the search page also handle actors because then you would have to make pages for those actors and I should now focus more on getting the functionality that I do have to work perfectly and to expand on the quiz because it has only 4 questions. Also I have the favourite genre of the user (on personal page based on previous results) but I'm not sure if it is possible to implement this in the quiz right now because otherwise you would get maybe 3 or 4 genres and if you would enter more than 2 genres into the api, you will get no movies (most movies have only 2 genres attached).

Furthermore, there is now a watchedmovies table in the database to track what movies the user has watched.

Date: 22 - 05 - 2020

Sorry forgot to update my process.md! I extended the quiz with a language selection and I cleaned up the code of the quiz because it was too repetitive. Also, the search function now handles title or year. The already watched movies are now also removed from the results of the quiz.

The one thing I found out is that because there is a button on the movie page that you can press when you have seen the movie, the movie page can only be seen if logged in (which is a pity). Also, I wanted to implement the login with flask-login but I didn't have enough time and I thought it would be better to concentrate on the app itself. 

Date: 25 - 05 - 2020

Today, I included a button on the movie page to rent the movie, you will then go to a checkout by mollie and when payed you go to a page where you can "watch" the movie (it's just a bigger version of the trailer ;)

Date: 26 - 05 - 2020

I worked on the layout (css) to make the quiz look a little better. I finished working on the payment for renting a movie. 


