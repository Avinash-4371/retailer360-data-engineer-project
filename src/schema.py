from datetime import datetime
import os

def add_metadata_columns(df, source_file_path: str):
    print(source_file_path)
    filename=os.path.splitext(os.path.basename(source_file_path))[0]
    date=datetime.now()
    df["load_date"] = date.strftime('%Y-%m-%d')
    df["load_timestamp"] = date
    df["source_file_name"] = f"{filename}_{date.strftime('%Y%m%d%H%M%S')}"
    return df

def convert_all_columns_to_string(df):
    return df.astype(str)