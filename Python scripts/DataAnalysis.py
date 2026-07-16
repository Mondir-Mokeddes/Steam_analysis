import pandas as pd
import re
import ast
from pathlib import Path



def set_integer(df,column):
    df[column] = df[column].astype("Int64")
    return df

def clean_titles(df, column):
    df[column] = df[column].str.lower()
    df[column] = df[column].str.replace(r'[^a-zA-Z0-9]+',' ', regex=True)
    df[column] = df[column].str.replace('™',' ')
    return df

def hours_and_minutes_to_minutes(df, column):
    parts = df[column].str.extract(r"(?:(\d+)h)?\s*(?:(\d+)m)?")
    mask = parts.notna().any(axis=1)
    parts = parts.fillna(0).astype(int)
    df[column] = (parts[0] * 60 + parts[1]).where(mask) #this just turns 1h 40m into 100, but also turns n/a in NaN
    return df

def thousands_K_to_integer(df, column):
    df[column] = (
        df[column]
        .replace("n/a", pd.NA)
        .str.replace(r"(\d\.\d)K", lambda x: str(round(float(x.group(1)) * 1000)), regex=True)
    )
    return df

def replace_issue_character(df, issue_character, column):
    df[column] = df[column].replace(issue_character, pd.NA)
    return df

def import_data():
    script_location = Path(__file__).absolute().parent.parent
    input_path_1 = script_location / "data/processed/secondoutput.csv"
    input_path_2 = script_location / "data/processed/thirdoutput.csv"
    df1 = pd.read_csv(input_path_1)
    df2 = pd.read_csv(input_path_2)
    return df1, df2


def merge_tables(df1,df2): #################first step: making everything alphanumeric and lowercase and merging
    df1 = clean_titles(df1,"game_titles")
    df2 = clean_titles(df2,"Title")

    main_df = pd.merge(df2, df1, left_on ="Title", right_on="game_titles", how ='left')
    return main_df

def add_decimal_0_before_K(df, column):
    mask = df[column].str.contains(r'^(\d)K$', regex=True, na=False)
    df.loc[mask,column] = (
        df.loc[mask,column]
        .str.replace("K", ".0K", regex=False)
    )
    return df

def export_data_including_exploded(df):
    exploded_df = df.explode("Genres")
    script_location = Path(__file__).absolute().parent.parent
    output_path_sanitised = script_location / "data/database/Sanitised_Data.csv"
    output_path_exploded = script_location / "data/database/Exploded_Data.csv"
    df.to_csv(output_path_sanitised, index=False)
    exploded_df.to_csv(output_path_exploded, index=False)

def create_main_dataframe():
    df1, df2 = import_data()
    main_df = merge_tables(df1, df2)

    main_df["Total_number_of_reviews"] = main_df["Total_number_of_reviews"].str.replace(r'[^0-9]','', regex=True)

    main_df["Genres"] = main_df.pop("Genres")
    main_df = main_df.drop("game_titles", axis=1)
    return main_df

def clean_formats(main_df):
    main_df = hours_and_minutes_to_minutes(main_df, "time_main")
    main_df = hours_and_minutes_to_minutes(main_df, "time_complete")

    main_df = add_decimal_0_before_K(main_df, "count_main")
    main_df = add_decimal_0_before_K(main_df, "count_complete")

    main_df = thousands_K_to_integer(main_df,"count_main")
    main_df = thousands_K_to_integer(main_df,"count_complete")

    main_df["Date_published"] = pd.to_datetime(
        main_df["Date_published"],
        format="%d %b, %Y",
        errors="coerce"
    )

    return main_df

def clean_missing_values(main_df):
    columns = [
        "English_rating",
        "Date_published",
        "Total_number_of_reviews",
        "Publisher",
        "Genres",
        ]
    for col in columns:
        main_df = replace_issue_character(main_df,"n/a",col)

    columns_2 = [
        "completed_achievements",
        "total_achievements"
        ]
    for col in columns_2:
        main_df = replace_issue_character(main_df,"",col)
    return main_df

def set_data_types(main_df):
    integer_columns = [
        "completed_achievements",
        "total_achievements",
        "time_main",
        "time_complete",
        "count_main",
        "count_complete",
        "Total_number_of_reviews"
        ]
    for col in integer_columns:
        main_df = set_integer(main_df,col)

    main_df["Date_published"] = main_df["Date_published"].astype("datetime64[ns]")

    main_df["Genres"] = main_df["Genres"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else x
    ) #makes everything in the list into a string

    main_df = main_df.dropna(subset=["Total_number_of_reviews", "Publisher", "Genres"], how="all")
    return main_df

def main():
    main_df = create_main_dataframe()
    main_df = clean_formats(main_df)
    main_df = clean_missing_values(main_df)
    main_df = set_data_types(main_df)
    export_data_including_exploded(main_df)

if __name__ == "__main__":
    main()

