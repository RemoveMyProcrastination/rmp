## Milestone3_Database ##

### CouchDB ###

For our project we are using CouchDB(NoSQL) as the database and are using python and flask to create the api that will interact with CouchDB and the android client. 
The database is located on an ubuntu server set up using Amazon Web Services. 

We currently have 6 documents in the database, which are titled by user name. Each user name has all of the apps that are used, with corresponding time that app has been used per day, per week, and total usage of all the apps per day and per week. As we are still working on the api to populate the database, the database has been populated using REST commands and test(fake) users. Each user has 4 applications that they have usage data for + 1 total usage section, all of which contain data for each day of the week. Also, a goals section has been added that will compare the daily and weekly usage with the corresponding set goal. We plan to expand this, and possibly include geolocation sections and more specfic data storage sections.

Below is a screenshot of all of the documents in our user_data database, as well as a close up of the data in some of the specific document users.


![ScreenShot of Database](DatabaseEx.png)
