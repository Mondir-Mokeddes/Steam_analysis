
from requests_html import HTMLSession
import pandas as pd
from pathlib import Path

cookies = {'lastagecheckage': '1-0-1900', 'birthtime':'-2211667760', 'wants_mature_content':'1'}


def import_data():
    script_location = Path(__file__).absolute().parent.parent
    input_path = script_location / "data/processed/output.csv"
    df = pd.read_csv(input_path)
    df["Steam_id"] = df["Steam_id"].astype(str)

    return df

def extract_english_ratings(response):
    try:
        return response.html.find('span.game_review_summary[itemprop="description"]')[0].text
    except IndexError:
        return 'n/a'

def extract_date(response):
    try:
        return response.html.find('div.date')[0].text
    except IndexError:
        return 'n/a'

def extract_total_reviews(response):
    try:
        return response.html.find('span.review_summary_count')[0].text
    except IndexError:
        try:
            return response.html.find('span.app_reviews_count')[0].text
        except IndexError:
            return 'n/a'

def extract_publisher(response):
    try:
        temp = response.html.find('div.dev_row')[1]
        return temp.find('a')[0].text
    except IndexError:
        return 'n/a'
def extract_genres(response):
    try:
        genres = response.html.find('div.glance_tags.popular_tags')

        genres_list = genres[0].find('a')
        genres_text=[]
        for x in range(len(genres_list)):
            genres_text.append(genres_list[x].text)
        return genres_text
    except IndexError:
        return 'n/a'

def extract_game_data(session, steam_id):
    steam_id = str(steam_id)
    response = session.get('https://store.steampowered.com/app/'+ steam_id, cookies=cookies, timeout=15)
    return {
        'Steam_id': steam_id,
        'English_rating': extract_english_ratings(response),
        'Date_published': extract_date(response),
        'Total_number_of_reviews': extract_total_reviews(response),
        'Publisher': extract_publisher(response),
        'Genres': extract_genres(response)
        }

def extract_steam_data(df):
    session=HTMLSession()
    extracted_data = []

    for row in df.itertuples():
        data = extract_game_data(session, row.Steam_id)
        extracted_data.append(data)

    extracted_df = pd.DataFrame(extracted_data)
    session.close()

    return df.merge(extracted_df, on="Steam_id")

def export_data(df):
    script_location = Path(__file__).absolute().parent.parent
    output_path = script_location / "data/processed/thirdoutput3.csv"
    df.to_csv(output_path, index=False)

def main():
    df = import_data()
    df = extract_steam_data(df)
    export_data(df)


if __name__ == "__main__":
    main()








