from pathlib import Path
import fnmatch


def list_matching_files(file_path : Path , file_pattern : str):
    return[ files for files in Path(file_path).iterdir() if files.is_file() and fnmatch.fnmatch(files.name, file_pattern)]

def validate_file_extension(file_path : Path, file_type: str):
    extension_required = {"csv":[".csv"],
                 "json":[".json"],
                 "excel":[".xls",".xlsx"],
                 "parquet":[".parquet"],
                 "api":[]
                 }
    recive = extension_required.get(file_type)
    for files in Path(file_path).iterdir():
        if files.is_file() and files.suffix.lower() not in recive:

           raise ValueError(f"Invalid extension {files.suffix} for file type {file_type} in file {files.name}")
    return True


#a=list_matching_files("C:/Users/avi72/retailer360-data-engineer-project/data/landing/sales/","sales_*.csv")
#print(a)
b=validate_file_extension("C:/Users/avi72/retailer360-data-engineer-project/data/landing/sales/","csv")
print(b)