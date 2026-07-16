import pandas as pd
from requests_html import HTML
from pathlib import Path

def load_data():
    script_location = Path(__file__).absolute().parent.parent
    input_path = script_location / 'data/raw/Steam~Games.html'

    with open(input_path, encoding="utf-8") as f:
        source = f.read()

    html = HTML(html=source)
    info_table = html.find('div.JeLbcWPaZDg-')
    return info_table

def find_data(table):
    data = []

    for item in table:
        name = item.find('span.UpqjtP0-VK0-')[0].text
        steam_id = (
            item.find('a', first=True)
            .attrs.get('href')
            .split("/")[4]
        )
        achievement_check = item.find('a.dSM5w2eZ5dA-')
        if len(achievement_check) > 0:
            achievements = item.find('span.FwfGO0sl0JA-')[0].text.split("/")
            row = {
                "Title": name,
                "Steam_id": steam_id,
                "has_achievements": "Y",
                "completed_achievements": achievements[0],
                "total_achievements": achievements[1]
                }
        else:
            row = {
                "Title": name,
                "Steam_id": steam_id,
                "has_achievements": "N",
                "completed_achievements": "N/A",
                "total_achievements": "N/A"
                }
        data.append(row)
    return data

def export_data(data):
    df = pd.DataFrame(data)
    script_location = Path(__file__).absolute().parent.parent
    output_path = script_location / "data/processed/output.csv"
    df.to_csv(output_path, index=False)

def main():
    table = load_data()
    data = find_data(table)
    export_data(data)

if __name__ == "__main__":
    main()














