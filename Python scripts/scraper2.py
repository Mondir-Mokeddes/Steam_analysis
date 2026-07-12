import pandas as pd
from requests_html import HTML
from pathlib import Path


a = open("data/raw/Steam~Games.html")
source = a.read()
html = HTML(html=source)

tablez = html.find('div.FbG-gxCxUQw-', first=True)
tableq = html.find('div.JeLbcWPaZDg-')


names=[]
temp=[]
ids=[]
has_achievments=[]
completed_achievements=[]
total_achievements=[]

for item in tableq:
    names.append(item.find('span.UpqjtP0-VK0-')[0].text)
    temp_id= item.find('a', first=True).attrs
    ids.append(temp_id.get('href').split("/")[4])
    try:
        temp.append(item.find('a.dSM5w2eZ5dA-')[0].text)
        has_achievments.append('Y')
        completed_achievements.append(item.find('span.FwfGO0sl0JA-')[0].text.split("/")[0])
        total_achievements.append(item.find('span.FwfGO0sl0JA-')[0].text.split("/")[1])
    except:
        has_achievments.append('N')
        completed_achievements.append('N/A')
        total_achievements.append('N/A')


data_new=[]

for i in range(len(names)):
    tempdict = dict(Title = names[i],Steam_id=ids[i], has_achievements = has_achievments[i], completed_achievements = completed_achievements[i], total_achievements = total_achievements[i])
    data_new.append(tempdict)

df = pd.DataFrame(data_new)
output_path = Path("data/processed/output.csv")
df.to_csv(output_path, index=False)













