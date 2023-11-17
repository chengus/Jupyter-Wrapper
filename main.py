import os
import sys
import argparse
import json

def run_initial_setup():
    # Check Python version
    if sys.version_info.major < 3:
        print("Python 3 is required. Please download and install it from https://www.python.org/downloads/")
        sys.exit(1)
    else:
        print("Python version:", sys.version)

    # Code to create virtual env and install dependencies
    print("Running initial setup...")
    # ... setup code ...

    # Create a flag file upon successful setup
    open('setup_complete.flag', 'a').close()

def check_first_run():
    return not os.path.exists('setup_complete.flag')

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process a folder containing a notebook and app.json.")
    parser.add_argument("directory", type=str, help="Directory of the folder")
    return parser.parse_args()

def find_notebook(directory):
    """Find a notebook file in the given directory. Raise an error if more than one notebook is found."""
    notebooks = [file for file in os.listdir(directory) if file.endswith(".ipynb")]

    if len(notebooks) > 1:
        raise ValueError("More than one notebook found in the directory.")
    elif len(notebooks) == 0:
        raise ValueError("No notebook found in the directory.")
    else:
        return notebooks[0]


def read_app_json(directory):
    """Read details from app.json and check for required items."""
    required_keys = ['Python Version', 'Dependencies', 'App Name']

    try:
        with open(os.path.join(directory, "app.json"), 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Check for required keys
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                raise ValueError(f"Missing required key(s) in app.json: {', '.join(missing_keys)}")

            # Check dependencies versions if dependencies are listed
            if 'Dependencies' in data and data['Dependencies']:
                for dep, version in data['Dependencies'].items():
                    if not version:
                        raise ValueError(f"Version number required for dependency: {dep}")

            return data

    except FileNotFoundError:
        print("Error: app.json not found.")
        return None
    except json.JSONDecodeError:
        print("Error: app.json is not a valid JSON file.")
        return None
    except ValueError as e:
        print(e)
        return None


def main():
    if check_first_run():
        run_initial_setup()

    args = parse_args()
    print(args)
    # Find notebook file
    notebook = find_notebook(args.directory)
    if notebook:
        print(f"Name of notebook: {notebook}")
    else:
        print("No notebook found in the directory.")

    # Read app.json details
    app_details = read_app_json(args.directory)
    if app_details:
        print("Details from app.json:")
        for key, value in app_details.items():
            print(f"{key}: {value}")
    else:
        print("app.json not found or is empty.")

if __name__ == "__main__":
    main()
