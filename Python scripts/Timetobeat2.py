import requests
from bs4 import BeautifulSoup #using
import pandas as pd
from playwright.sync_api import sync_playwright #using
import time #using
import os
from pathlib import Path


def games_url_codes(): #returns a dictionary of game titles and their associated urls on howlongtobeat.com
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        steam_username = os.getenv("STEAM_USERNAME")
        page.goto('https://howlongtobeat.com/steam?userName={steam_username}')
        time.sleep(4)
        full_html = page.content()
        browser.close()

    titles_clean = []
    links_clean = [] #clean as they had no html parts ie <p>

    soup = BeautifulSoup(full_html, 'html.parser')
    titles = soup.find_all('span', style="text-decoration: none;")


    for a in soup.find_all('a', class_=''):
        links_clean.append(a.get('href'))

    for span in titles:
        titles_clean.append(span.get_text())

    data = dict(zip(titles_clean, links_clean))
    return(data)


def time_to_beat(diction): #takes in a dictionary from above and searches the urls for time to beat and number noted
    time_main=[]
    count_main=[]
    time_complete=[]
    count_complete=[]
    final_dict ={}

    for key in diction:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://howlongtobeat.com'+str(diction[key]))
            full_html = page.content()
            browser.close()

        soup = BeautifulSoup(full_html, 'html.parser')
        tablez = soup.find('table', class_ = 'GameTimeTable-module__M5Fuva__game_main_table')
        a={}
        i=0
        try:
            for row in tablez.find_all('tr')[1:]:
                columns = row.find_all('td')
                key = i
                value = [column.text for column in columns]
                a[key] = value
                i = i+1
        except:
            a['hi'] = 'yo'


        try:
            if a[0][0] == 'Main Story':
                count_main.append(a[0][1])
                time_main.append(a[0][2])
            else:
                count_main.append('n/a')
                time_main.append('n/a')
            try:
                if a[0][0] == 'Completionist':
                    count_complete.append(a[1][1])
                    time_complete.append(a[1][2])
                elif a[1][0] == 'Completionist':
                    count_complete.append(a[1][1])
                    time_complete.append(a[1][2])
                elif a[2][0] == 'Completionist':
                    count_complete.append(a[2][1])
                    time_complete.append(a[2][2])
                else:
                    count_complete.append('n/a')
                    time_complete.append('n/a')
            except:
                count_complete.append('n/a')
                time_complete.append('n/a')

        except:
            count_main.append('n/a')
            time_main.append('n/a')
            count_complete.append('n/a')
            time_complete.append('n/a')


    game_titles = list(diction.keys())
    keys=[]
    for i in range(len(game_titles)):
        keys.append(i)

    final_dict["keys"] = keys
    final_dict["game_titles"] = game_titles
    final_dict["count_main"] = count_main
    final_dict["time_main"] = time_main
    final_dict["count_complete"] = count_complete
    final_dict["time_complete"] = time_complete

    return final_dict


data = time_to_beat(games_url_codes())

df = pd.DataFrame(data)
output_path = Path("data/processed/secondoutput.csv")
df.to_csv(output_path, index=False)









