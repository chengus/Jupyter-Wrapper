import os

def run_initial_setup():
    # Code to create virtual env and install dependencies
    print("Running initial setup...")
    # ... setup code ...

    # Create a flag file upon successful setup
    open('setup_complete.flag', 'a').close()

def check_first_run():
    return not os.path.exists('setup_complete.flag')

def main():
    if check_first_run():
        run_initial_setup()

    # Rest of your application code
    print("Running application...")

if __name__ == "__main__":
    main()
