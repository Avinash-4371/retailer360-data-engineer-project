import pandas as pd
from pathlib import Path

def read_gcs_file_to_dataframe(file_path: str, config_file: dict) -> pd.DataFrame:

    file_ext = config_file.get("file_type", "").lower()

    if file_ext == "csv":
        return read_csv_file(file_path, config_file)
    elif file_ext == ".json":
        return read_json_file(file_path, config_file)
    elif file_ext in [".xls", ".xlsx"]:
        return read_excel_file(file_path, config_file)
    elif file_ext == ".parquet":
        return read_parquet_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def read_csv_file(file_path: str, config_file: dict) -> pd.DataFrame:
    delimiter = config_file.get("delimiter", ",")
    header = 0 if config_file.get("header", True) else None
    return pd.read_csv(file_path, delimiter=delimiter, header=header, dtype=str)


def read_json_file(file_path: str, config_file: dict) -> pd.DataFrame:
    try:
        return pd.read_json(file_path, dtype=str, lines=True)
    except ValueError:
        return pd.read_json(file_path, dtype=str)


def read_excel_file(file_path: str, config_file: dict) -> pd.DataFrame:
    sheet_name = config_file.get("sheet_name")
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, engine="openpyxl")


def read_parquet_file(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)