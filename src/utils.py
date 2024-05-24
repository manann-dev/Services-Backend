import sys
import yaml

# Function to read configuration from the config file
def read_config(config_file):
    try:
        test_open_config_file(config_file)
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
        return {}

def test_open_config_file(file_path):
    try:
        print(file_path)
        # Attempt to open the file for reading
        with open(file_path, 'r') as config_file:
            # If the file opens successfully, you can perform further operations here
            print(f"Successfully opened the configuration file: {file_path}")
            # You can read, parse, or process the file content as needed
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Failed to open the file '{file_path}'.")
        print(f"Error Details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

