
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

def read_all_file_to_dataframe(source_path : Path, config_file : str):
   file_type = config_file["file_type"]
   if file_type == "csv":
      return read_csv_file(source_path,config_file)
   if file_type == "json":
      return read_json_file(source_path,config_file)
   if file_type == "excel":
      return read_excel_file(source_path,config_file)
   if file_type == "parquet":
      return read_parquet_file(source_path)


def read_csv_file(file_path : Path, config_file : dict):
    delimiter = config_file.get("delimiter",",")
    header = 0 if config_file.get("header",True) is True else None
    return pd.read_csv(file_path,delimiter=delimiter,header=header,index_col=0,dtype=str)
def read_json_file(file_path : Path,config_file : dict):
    try:
       return pd.read_json(file_path,dtype=str,lines=True,nrows=None)
    except ValueError:
     return pd.read_json(file_path, dtype=str,nrows=None)

def read_excel_file(file_path : Path, config_file: dict):
   sheet_name=  config_file.get("sheet_name")  
   return pd.read_excel(file_path,sheet_name=sheet_name,dtype=str,engine="openpyxl",index_col= False)

def read_parquet_file(file_path: Path):
   return pd.read_parquet(file_path)
   
   
    



if __name__ == "__main__":
    print("--- Starting Local Test ---")

    try:
        print("Loading config file")
        config = yaml_load(CONFIG_PATH)
        print("Config file loaded successfully")

        sources = config["sources"]

        for source_name, source_config in sources.items():
            if not source_config.get("enabled", False):
                print(f"Skipping {source_name} (disabled)")
                continue

            source_dir = Path(source_config["source_path"])
            pattern = source_config.get("file_pattern")

            print(f"\n--- Reading {source_name} from {source_dir} ({source_config['file_type']}) ---")

            if not source_dir.exists():
                print(f"❌ Path does not exist: {source_dir}")
                continue

            files = list(source_dir.glob(pattern))
            if not files:
                print(f"❌ No files found for {source_name} with pattern {pattern}")
                continue

            # Read and preview each matching file
            for f in files:
                try:
                    df = read_all_file_to_dataframe(f, source_config)
                    if df is None:
                        print(f"❌ Could not load {source_name} from {f}")
                        continue

                    print(f"{source_name} loaded successfully from {f} with {len(df)} rows")
                    print("\n--- Success! Here is your data ---")
                    print(df.head())
                except Exception as e:
                    print(f"Failed to load {source_name} from {f}: {e}")

    except Exception as e:
        print(f"Pipeline failed: {e}")










