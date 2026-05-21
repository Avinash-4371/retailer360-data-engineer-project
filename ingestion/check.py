from pathlib import Path
import fnmatch


def list_matching_files(file_path : Path , file_pattern : str):
    return[ files for files in Path(file_path).iterdir() if files.is_file() and fnmatch.fnmatch(files.name, file_pattern)]


a=list_matching_files("C:/Users/avi72/retailer360-data-engineer-project/data/landing/sales/","sales_*.csv")
print(a)
