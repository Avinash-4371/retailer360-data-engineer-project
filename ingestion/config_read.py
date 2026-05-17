
import os
import yaml

# BEST PRACTICE: Use a relative path so your code works on any computer (or in the cloud),
# not just on your personal local C: drive.
CONFIG_PATH =  r"C:\Users\avi72\retailer360-data-engineer-project\ingestion\config.yml"

def yaml_load(path=CONFIG_PATH):
    if not os.path.exists(path):
        print(f"path = {path} not exist")

    with open(path,"r",encoding="utf-8") as file:
      return yaml.safe_load(file)
if __name__ == "__main__":
    try:
        config_data = yaml_load()
        print("✅ YAML loaded successfully!")
        print(config_data)
    except Exception as e:
        print(f"❌ Error: {e}")