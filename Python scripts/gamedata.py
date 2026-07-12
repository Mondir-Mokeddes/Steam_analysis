import csv
from requests_html import HTMLSession
import pandas as pd
from pathlib import Path

session=HTMLSession()
input_path = Path("data/processed/output.csv")
df = pd.read_csv(input_path)

cookies = {'lastagecheckage': '1-0-1900', 'birthtime':'-2211667760', 'wants_mature_content':'1'}

all_english_ratings = []
all_date =[]
all_total_reviews = []
all_publisher = []
all_genres = []

for row in df.itertuples():
    response = session.get('https://store.steampowered.com/app/' + str(row.Steam_id), cookies=cookies)

    try:
        all_english_ratings.append(response.html.find('span.game_review_summary[itemprop="description"]')[0].text)
    except:
        all_english_ratings.append('n/a')

    try:
        all_date.append(response.html.find('div.date')[0].text)
    except:
        all_date.append('n/a')

    try:
        all_total_reviews.append(response.html.find('span.review_summary_count')[0].text)
    except:
        try:
            all_total_reviews.append(response.html.find('span.app_reviews_count')[0].text)
        except:
            all_total_reviews.append('n/a')

    try:
        temp = response.html.find('div.dev_row')[1]
        all_publisher.append(temp.find('a')[0].text)
    except:
        all_publisher.append('n/a')

    try:
        genres = response.html.find('div.glance_tags.popular_tags')

        genres_list = genres[0].find('a')
        genres_text=[]
        for x in range(len(genres_list)):
            genres_text.append(genres_list[x].text)
        all_genres.append(genres_text)
    except:
        all_genres.append('n/a')


df['English_rating'] = all_english_ratings
df['Date_published'] = all_date
df['Total_number_of_reviews'] = all_total_reviews
df['Publisher'] = all_publisher
df['Genres'] = all_genres

output_path = Path("data/processed/thirdoutput.csv")
df.to_csv(output_path, index=False)




