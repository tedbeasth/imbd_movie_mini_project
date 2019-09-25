# imbd_movie_mini_project

##### Instructions
All of the functions needed to solve the problem set can be found in tasks.py

##### Database Design:
- Persons model that can be either a director or an actor
- Genre model that only has a name attribute
- Movie model that contains all the other fields from the csv file

For the database design I decided to break it up into a few different models. Mainly because this is more like a real world application for a database design. Given more problems to solve and a more real world application, the models could be broken up further.

##### Assumptions:
- An actor’s facebook likes are the same across all movies
- A movie can only have one director
- Lot of assumptions with input types and trusting valid data from csv

##### Importing:
For importing the csv into the database, I thought about using Django’s bulk_create function for improved efficiency. But ultimately, decided to just create each object individually because bulk_create does not support many-to-many relationships.  After some research it looks like bulk_create might be feasible by using a through model to save the many to many relationships. However, since it is a one time file upload, I decided speed was not a major concern. Furthermore, if speed was a concern, it would be best to do the import directly with SQL. I saw some interesting solutions involving SQL, however I do not have experience with that particular case so I decided to keep this project simple and not dive into that at this time. I used @transaction.atomic to help with the speed in my local environment. Since I am using SQLite which is slow on writes, atomic helped save time calling many save() methods.

##### Libraries used:
Everything shown in requirements.txt

##### Steps taken:
1. Setup django project and app in github and cloned to local repository and virtual env
2. Set up models and admin to reflect movie database that will be imported
3. Wrote script to import csv file and populate local database
4. Built out query functions to solve the problems listed
5. Wrote unit tests, refactored, overall cleanup

##### Unit Testing:
Only wrote tests for some of the app, and only some of the cases. A lot of the functions were similar so I felt it was trivial to do a full 100% coverage. The way I as taught to unit test is isolate the purpose of the function and mock out any other calls. Sometimes, this even includes mocking out queries, because testing a complex query is an integration test. These could be improved on given more time.

##### Problems Solved:
In the tasks.py file there are a few different variations of finding profitability. The functions can be used to return any of the following:
- Top 10 genres in decreasing order
   - Profitability calculated by sum of ‘gross’ minus sum of ‘budget’
   - Profitability calculated by average of ‘gross’ minus average of ‘budget’
- Top 10 actors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
- Top 10 directors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
- Top 10 of either actors or directors in decreasing order calculated by sum of ‘gross’ minus sum of ‘budget’
