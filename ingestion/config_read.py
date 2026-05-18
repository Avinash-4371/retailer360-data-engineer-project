
import os
import yaml
import pandas as pd
from pathlib import Path

# BEST PRACTICE: Use a relative path so your code works on any computer (or in the cloud),
# not just on your personal local C: drive.
CONFIG_PATH =  r"C:\Users\avi72\retailer360-data-engineer-project\ingestion\config.yml"

def yaml_load(path=CONFIG_PATH):
    if not os.path.exists(path):
        print(f"path = {path} not exist")

    with open(path,"r",encoding="utf-8") as file:
      return yaml.safe_load(file)
def read_csv_file(file_path : Path, config_file : dict):
    delimiter = config_file.get("delimiter",",")
    header = 0 if config_file.get("header",True) is True else None
    return pd.read_csv(file_path,delimiter=delimiter,header=header,index_col=0,dtype=str)
def read_json_files(file_path : Path,config_file : dict):
    try:
       return pd.read_json(file_path,dtype=str,lines=True,nrows=None)
    except ValueError:
     return pd.read_json(file_path, dtype=str,nrows=None)


if __name__ == "__main__":
    print("--- Starting Local Test ---")

    try:
       print("Loading config file")
       config=yaml_load(CONFIG_PATH)
       print(f"config file loaded: {config}........")

       sales_config=config["sources"]["sales"]
       sales_config_json=config["sources"]["customers"]
       file_path = Path(sales_config["source_path"])
       file_path_json = Path(sales_config_json["source_path"])
       target_file = r"C:\Users\avi72\retailer360-data-engineer-project\data\landing\sales\store_sales.csv"
       target_file_json = r"C:\Users\avi72\retailer360-data-engineer-project\data\landing\customers\customers.json"
       df = read_csv_file(target_file, sales_config)
       print("\n--- Success! Here is your data ---")
       print(df.head())
       df = read_json_files(target_file_json,file_path_json)
       print("\n--- Success! Here is your data ---")
       print(df.head())


    except Exception as e:
        print(f" Pipeline failed: {e}")


