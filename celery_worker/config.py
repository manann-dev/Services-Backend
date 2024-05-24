import os
import sys
from openai import OpenAI
from utils import read_config   # Assuming you have a utils module for test_open_config_file function

# Check and load CONFIG_FILE
CONFIG_FILE = os.environ.get("CONFIG_FILE")
if not CONFIG_FILE:
    print("Error: CONFIG_FILE environment variable is not set.")
    sys.exit(2)
    
# Check and load OPENAI_API_KEY
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

# Initialize and export the OpenAI client
client = OpenAI(api_key=api_key)
config = read_config(CONFIG_FILE)