## Brief comments on Engineering Analytics Exercise.

- How did you handle Twitter's rate limiting, and what are some options for improving this in the next iteration of this project?

   *I never reached the limit of allowed requests which is 1500 requests per 15 minutes for the user timeline endpoint. To optimize the number of requests I am requesting 200 tweets per request (max amount) as well as I am checking if I reached the end of the timeline.*
   
- How extendible is the software you wrote? How would you make it more reusable?

   *Make the Twitter hooks configurable. For example allow any Twitter account to be used in the analysis.*

- What's the most flawed piece of the analysis, and how would you improve it if you had
   more time?

	- *I am analyzing Twitter activity looking at time of day (i.e. 1pm). The analysis would be more complete if I record day of week (i.e. Monday) as well.*
	- *I collected all the tweets that the Twitter API allow but did not take under consideration the time period the tweets weere sent. Looking at the db I can see the recently harrys has been the most active and SchickHydro tweets the least. See below the dates of the earliest and latest record for each account.*

```
         min         |         max         | count |     account
---------------------+---------------------+-------+-----------------
 2014-09-15 12:30:35 | 2016-11-19 11:00:38 |  3227 | DollarShaveClub
 2016-04-18 11:36:00 | 2016-11-18 17:25:00 |  3198 | harrys
 2016-02-09 08:33:33 | 2016-11-20 17:01:00 |  3157 | Gillette
 2011-08-01 11:43:23 | 2016-09-16 10:04:22 |  2603 | SchickHydro
(4 rows)
``` 

- What would it take to make this a production system used everyday by our marketing team?

   *Automate the process of creating the plots from the API calls.*
