def convert_all_colums_to_string(df):
    return df.astype(str)

def add_metadata_columns(df,source_file_path,checksum):
    df["source_file"] = source_file_path.name
    df["ingestion_timestamp"] = pd.Timestamp.now()
    df["checksum"] = checksum
    return df