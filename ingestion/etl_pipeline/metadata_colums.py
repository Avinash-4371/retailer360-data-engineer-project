from datetime import datetime

def add_metadata_columns(df, source_file_path: str):
    df["source_file_name"] = source_file_path.split("/")[-1]
    df["load_timestamp"] = datetime.now()
    df["load_date"] = datetime.now().date()
    return df

def convert_all_columns_to_string(df):
    return df.astype(str)