import pandas as pd
import re
import ast
from pathlib import Path


def Set_integer(df,column):
    df[column] = main_df[column].astype("Int64")

def Clean_titles(df, column):
    df[column] = df[column].str.lower()
    df[column] = df[column].str.replace(r'[^a-zA-Z0-9]+ ',' ', regex=True)
    df[column] = df[column].str.replace('™',' ')

def Hours_and_minutes_to_minutes(df, column):
    #incomprehensible nonsense written in part(mostly(entirely)) by stack overflow
    parts = df[column].str.extract(r"(?:(\d+)h)?\s*(?:(\d+)m)?")
    mask = parts.notna().any(axis=1)
    parts = parts.fillna(0).astype(int)
    df[column] = (parts[0] * 60 + parts[1]).where(mask) #this just turns 1h 40m into 100, but also turns n/a in NaN

def Thousands_K_to_integer(df, column):
    df[column] = (
        df[column]
        .replace("n/a", pd.NA)
        .str.replace(r"(\d\.\d)K", lambda x: str(round(float(x.group(1)) * 1000)), regex=True)
    )

def Replace_issue_character(df, issue_character, column):
    df[column] = df[column].replace(issue_character, pd.NA)

####################### program start here
input_path_1 = Path("data/processed/secondoutput.csv")
input_path_2 = Path("data/processed/thirdoutput.csv")
df1 = pd.read_csv(input_path_1)
df2 = pd.read_csv(input_path_2)

#################first step: making everything alphanumeric and lowercase and merging

Clean_titles(df1,"game_titles")
Clean_titles(df2,"Title")

main_df = pd.merge(df2, df1, left_on ="Title", right_on="game_titles", how ='left')
main_df["Total_number_of_reviews"] = main_df["Total_number_of_reviews"].str.replace(r'[^0-9]','', regex=True)

main_df["Genres"] = main_df.pop("Genres")
main_df = main_df.drop("game_titles", axis=1)

##################cleaning weird formats

Hours_and_minutes_to_minutes(main_df, "time_main")
Hours_and_minutes_to_minutes(main_df, "time_complete")


main_df.at[74, "count_main"]= "1.0K"
main_df.at[130, "count_complete"]= "2.0K"

Thousands_K_to_integer(main_df,"count_main")
Thousands_K_to_integer(main_df,"count_complete")

main_df["Date_published"] = pd.to_datetime(
    main_df["Date_published"],
    format="%d %b, %Y",
    errors="coerce"
)

##################setting default data type and replacing weird characters with pd.NA

Replace_issue_character(main_df,"n/a","English_rating")
Replace_issue_character(main_df,"n/a","Date_published")
Replace_issue_character(main_df,"n/a","Total_number_of_reviews")
Replace_issue_character(main_df,"n/a","Publisher")
Replace_issue_character(main_df,"n/a","Genres")
Replace_issue_character(main_df,"n/a","English_rating")

Replace_issue_character(main_df,"","completed_achievements")
Replace_issue_character(main_df,"","total_achievements")

Set_integer(main_df,"completed_achievements")
Set_integer(main_df,"total_achievements")
Set_integer(main_df,"time_main")
Set_integer(main_df,"time_complete")
Set_integer(main_df,"count_main")
Set_integer(main_df,"count_complete")
Set_integer(main_df,"Total_number_of_reviews")
main_df["Date_published"] = main_df["Date_published"].astype("datetime64[ns]")


main_df = main_df.dropna(subset=["Total_number_of_reviews", "Publisher", "Genres"], how="all")

main_df["Genres"] = main_df["Genres"].apply(ast.literal_eval)
exploded_df = main_df.explode("Genres")


output_path_sanitised = Path("data/database/Sanitised_Data.csv")
output_path_exploded = Path("data/database/Exploded_Data.csv")
main_df.to_csv('/home/spectre/Projects/python/steamachieve/databases/Sanitised_Data.csv', index=False)
exploded_df.to_csv('/home/spectre/Projects/python/steamachieve/databases/Exploded_Data.csv', index=False)

