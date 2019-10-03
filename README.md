# imbd_movie_mini_project

#### Instructions for webapp
&ensp; &ensp; &ensp; The app has been deployed on heroku at the following url: https://imbd-project.herokuapp.com/

&ensp; &ensp; &ensp; I did not spend much time with the styling and frontend design. Given time restraints, I just wanted to make a simple UI to be able to see the app in action. The webapp consists of two pages: one page that shows a table of all the movies (with pagination) and a second page to allow for the user to compute profitability. For the profitability page, just select one of the options in the drop down menu and you should see the results populate the page. As an additional feature, if you want, you can add a query string at the end of the url called "num_items". This will do the same profitability computation, but show however many results the user chooses. The default number of results is 10, as described in the project description. An example of the url to get the top 20 profitable actors is: https://imbd-project.herokuapp.com/profitability/?filter_type=actors&num_items=20 . Normally I would add an input field for the user to specify how many actors they want, but I felt that was unnecessary for this small project. Also, the size of the database exceeds Heroku's free tier plan, so there is a chance the app stops working on 10/9/2019.

#### Instructions for command line
&ensp; &ensp; &ensp; The instructions for running this on your local enviornment are a bit more cumbersome simply because you have to set up django, the database, etc. But here are some instructions if you prefer testing the app this way.
1. Clone the github repo, set up a virtualenv, and activate the enviornment.
2. add a 'dummy' SECRET_KEY to line 25 of the settings.py. Since this app is now deployed, the secret key isn't in the repository.
3. run <code>pip3 install -r requirements.txt</code> to download all the dependencies.
4. run <code>python manage.py migrate</code> to setup the database.

Once that is setup, you can run <code>python manage.py runserver</code> if you want to use the webapp in your localhost browser. You should also run <code>python manage.py collectstatic</code> to make sure the bootsrap css shows up and you will have to change line 24 in the settings.py file to make sure your localhost is allowed. Otherwise, follow these additional steps to run the tasks in the command line.

5. run <code>python manage.py shell</code> this will open up a shell through django.

Once the shell is running, you can run the following commands below inside of the shell.

6. <code>from imbadapp.tasks import *</code> you now have access to all the functions inside of imbdapp/tasks.py
7. <code>import_movies_csv()</code> this function will populate your local database from the csv file downloaded from kaggle. Should only be run once.

8. In the shell, you can now run any of the 5 funtions to compute profitability on your local database. These functions will not work if you did not correctly upload the data into your local database. There are five of these functions: get_top_profitable_genres_by_total(), get_top_profitable_genres_by_average(), get_top_profitable_actors_by_total(), get_top_profitable_directors_by_total, get_top_profitable_persons_by_total().

Please let me know if you run into any problems, bugs, or would like to see a specific area expanded on.


#### Problems Solved:
&ensp; &ensp; &ensp; In the tasks.py file there are a few different variations of finding profitability. The functions can be used to return any of the following:
- Top 10 genres in decreasing order
   - Profitability calculated by sum of ‘gross’ minus sum of ‘budget’
      - **RESULT:** [Comedy, Family, Adventure, Romance, Fantasy, Thriller, Action, Mystery, Music, Sport]
   - Profitability calculated by average of ‘gross’ minus average of ‘budget’
      - **RESULT:** [Family, Fantasy, Music, Musical, Sport, Adventure, Mystery, Romance, Comedy, Biography]
- Top 10 actors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
   - **RESULT:** [Peter Cushing, Kenny Baker, Catherine Dyer, Dee Wallace, Chirs Miller, Kathleen Freeman, Hattie McDaniel, George Reeves, Fiona Shaw, Adriana Caselotti]
- Top 10 directors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
   - **RESULT:** [Tim Miller, George Lucas, Richard Marquand, Kyle Balda, Colin Trevorrow, Chris Buck, Joss Whedon, Yarrow Cheney, Pierre Coffin, Lee Unkrich]
- Top 10 of either actors or directors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
   - **RESULT:** [Peter Cushing, Tim Miller, George Lucas, Richard Marquand, Kenny Baker, Kyle Balda, Colin Trevorow, Chris Buck, Joss Whedon, Yarrow Cheney]


#### Database Design:
- Persons model that can be either a director or an actor
- Genre model that only has a name attribute
- Movie model that contains all the other fields from the csv file

&ensp; &ensp; &ensp; For the database design I decided to break it up into a few different models. Mainly because this is more like a real world application for a database design. Given more problems to solve and a more real world application, the models could be broken up further.

#### Assumptions:
- An actor’s facebook likes are the same across all movies
- A movie can only have one director
- Lot of assumptions with input types and trusting valid data from csv

#### Importing:
&ensp; &ensp; &ensp; For importing the csv into the database, I thought about using Django’s bulk_create function for improved efficiency. But ultimately, decided to just create each object individually because bulk_create does not support many-to-many relationships.  After some research it looks like bulk_create might be feasible by using a through model to save the many to many relationships. However, since it is a one time file upload, I decided speed was not a major concern. Furthermore, if speed was a concern, it would be best to do the import directly with SQL. I saw some interesting solutions involving SQL, however I do not have experience with that particular case so I decided to keep this project simple and not dive into that at this time. I used @transaction.atomic to help with the speed in my local environment. Since I am using SQLite which is slow on writes, atomic helped save time.

#### Libraries used:
Everything shown in requirements.txt

#### Steps taken:
1. Setup django project and app in github and cloned to local repository and virtual env
2. Set up models and admin to reflect movie database that will be imported
3. Wrote script to import csv file and populate local database
4. Built out query functions to solve the problems listed
5. Wrote unit tests, refactored, overall cleanup

#### Unit Testing:
&ensp; &ensp; &ensp; Only wrote tests for some of the app, and only some of the cases. A lot of the functions were similar so I felt it was trivial to do a full 100% coverage. The way I as taught to unit test is isolate the purpose of the function and mock out any other calls. Sometimes, this even includes mocking out queries, because testing a complex query is an integration test. These could be improved on given more time.
