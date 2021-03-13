# TripAdvisor_Hotels
# WebScaper
[![Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project is a part of research work carried out to analyze the behaviour of customers visiting hotels in Boston and Newyork .

  - Focussed crawler was developed using beautiful soup and selenium
  - Ensured that cralwer obeys the laws of robot.txt
  - Used AWS resources and proxy rotating ip's in order to reduce the wait time

# Tools used!

  - Pyspark - Analyze data
  - S3 and RDS  to load data
  - Proxy raotator service
  - Fake Agents
  - Word2Vec for machine learning
 
# Architecture:
Below is the architected pipeline devloped 

![alt text](https://github.com/harshavardhanm03/TripAdvisor_Hotels/blob/master/RAWork_pipeline.PNG)
 
# Scarping  and CRONOS jobs
Initially data is scraped using local setup. Then AWS resources are added in order to scale up.Proxy roatator and fake agents are used in order rotate the  ips and browsers.

~10 Million points were gathered  from trip advisor and loaded data into S3.
Cronos jobs were scheduled in order to scrap new reviews from all the hotels.

# Loading and Visulizations
Data is loaded into RDS after data cleaning  for developing dashboards on the raw data. Amazon quick sight is used for visualizations.

# Batch jobs
Spark runs batch jobs for every one year and stores the data back into s3.

# Machine learning - Amazon Sage Maker

Word2Vec and LDA models were developed to analzye the reviews and to recommends better hotels.

# This is a new line