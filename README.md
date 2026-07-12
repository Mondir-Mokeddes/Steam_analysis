# Analysing the Factors Affecting Video Game Completion Time

## Overview

This project analyses the completion times of games in my steam library, and the factors that correlate to time required to beat and 100% the game. I used Python to webscrape Steam and HowLongToBeat for information to form a database, which was cleaned in Python. I then moved to Excel to visualise results. Although this project focuses on player completion behaviour, it demostrates skills in collecting data and building structured datasests to be analysed.


## Questions

This project answers a few main questions:

1. Does the time to 100% a game increase with achievement count?
2. Does the time to beat a game increase with rating?
3. Are more people reviewing games overtime?
4. Which genres have the highest and lowest time to 100%

## Tools used

Python:
- Requests
- Playwright
- Pandas

Data:
- Web scraping
- Data cleaning
- Data transformation

Excel:
- Exploratory analysis
- Visualisation
- Reporting


## Methodology

This was intially a project when I had planned to create a list of games which would be quick to 100%. I first used requests and playwright (in python) to webscrape steam and howlongtobeat.com for information about the video game in my steam library. This resulted in two distinct databases, one with steam information and one with information on how long it took players to beat and 100% games.

I then used pandas (in python) to merge the databases, and then clean the data. Cleaning consisted of making sure all missing values were of the same <Na> format and all columns of the same data type, so values that looked like "3.2K" became "3200".

I then exported two csv file - one exploded on genres and one not - and used ExCel for exploratory analysis. After this, I decided on the main questions of the project as I thought these questions were the most interesting in the dataset.

## Key Findings

For the questions above, this project found that:
1. The time to 100% does increase with achievement, up until a certain point where it seems to correlate much less.
2. The time to beat a game does increase with rating.
3. No conclusions can be drawn on if more people are reviewing games over time.
4. Grand strategy games take the longest time to beat and 100%, while puzzle platformers and 2.5D games take the least. The exact numbers of how long each genre took:

![Genre Completion Time](images/data.png)

## Limitations

The primary limitation of the project was the dataset. It was unfortunately rather small for the questions I wished to ask. while some of the conclusions felt as if they had enough data to justify, some questions felt as if they couldn't be answer with this dataset (namely "Are more people reviewing games over time?").

Alongside this, howlongtobeat.com contains user submitted data, and thus cant be verified. When the data count is low, it is difficult to justifiably use the data from this website to draw conclusions. 

Finally, I was unable to find a good public source for total sales. Such a source does not really exist, as steamspy.com has a range to great to be useful.


## Data Privacy

The dataset has been sanitised before publication.
Personal Steam account identifiers and unnecessary user-specific information have been removed.
