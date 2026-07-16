
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os
import random
from pathlib import Path
from dotenv import load_dotenv

def load_local_variables():
    script_location = Path(__file__).absolute().parent.parent
    dotenv_path = script_location / ".env"
    load_dotenv(dotenv_path)
    steam_username = os.getenv("STEAM_USERNAME")
    return steam_username


def obtain_html(steam_username): #returns a dictionary of game titles and their associated urls on howlongtobeat.com
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://howlongtobeat.com/steam?userName='+str(steam_username),timeout = 30000, wait_until="networkidle")
        full_html = page.content()
        browser.close()
    return full_html

def obtain_urls(full_html):
    titles_clean = []
    links_clean = [] #clean as they had no html parts ie <p>

    soup = BeautifulSoup(full_html, 'html.parser')
    titles = soup.find_all('span', style="text-decoration: none;")

    for a in soup.find_all('a', class_=''): #howlongtobeat uses empty attributes for links
        links_clean.append(a.get('href'))

    for span in titles:
        titles_clean.append(span.get_text())

    data = dict(zip(titles_clean, links_clean))
    return data

def extract_data_from_table(table):
    if table is None:
        return {}

    data = {}

    for i,row in enumerate(table.find_all('tr')[1:]):
            columns = row.find_all('td')
            data[i] = [column.text for column in columns]

    return data

def obtain_game_html(page, url):
    page.goto('https://howlongtobeat.com'+ url, timeout = 30000, wait_until="networkidle")
    time.sleep(random.uniform(0.7,1.5))
    return page.content()

def extract_times(html, name):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_ = 'GameTimeTable-module__M5Fuva__game_main_table')

    a = extract_data_from_table(table)
    times = {row[0]: row[1:] for row in a.values()}

    main_story = times.get("Main Story", ["n/a", "n/a"])
    completionist = times.get("Completionist", ["n/a", "n/a"])
    return {
        "game_title": name,
        "count_main": main_story[0],
        "time_main": main_story[1],
        "count_complete": completionist[0],
        "time_complete": completionist[1]
    }


def time_to_beat(game_urls): #takes in a dictionary from above and searches the urls for time to beat and number noted
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for key in game_urls:
            full_html = obtain_game_html(page, str(game_urls[key]))
            results.append(extract_times(full_html,key))

        browser.close()
    return results

def export_data(data):
    df = pd.DataFrame(data)
    script_location = Path(__file__).absolute().parent.parent
    output_path = script_location / "data/processed/secondoutput.csv"
    df.to_csv(output_path, index=False)

def main():
    username = load_local_variables()
    html = obtain_html(username)
    urls = obtain_urls(html)
    data = time_to_beat(urls)
    export_data(data)

if __name__ == "__main__":
    main()








