import json
import csv
import pandas as pd

def read_csv(filepath):
    with open(filepath,mode="r",encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file) # reads each row and change into dictionaries (key value pairs)
        return list(reader)

def read_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file) # read JSON data from a file and convert it into a Python object.


def read_excel(filepath):
    df = pd.read_excel(filepath)  # Reads the first sheet by default, returns a DataFrame.
    return df.to_dict(orient="records")  # Convert to dataframe to dictionaries