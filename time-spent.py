import time
import os
import psutil

log_file = "programming_time.log"

# Initialize log file if it doesn't exist
if not os.path.exists(log_file):
    with open(log_file, "w") as file:
        file.write("Total programming time (in seconds): 0\n")

# Function to check if the Code process is running
def is_vscode_running():
    # Iterate over all procs
    for proc in psutil.process_iter(attrs=['name']):
        try:
            if "code" in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Function to convert seconds to hh:mm:ss format
def timeTransformer(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to get the total time from the log file
def get_total_time():
    with open(log_file, "r") as file:
        lines = file.readlines()
    total_time = float(lines[0].split(":")[1].strip())  # First line contains total time
    return total_time

# Function to update the log file with the new total time
def update_log(session_time):
    old_total = get_total_time()
    new_total = old_total + session_time

    with open(log_file, "w") as file:
        file.write(f"Total programming time (in seconds): {new_total}\n")


#Debugging
def debug():
    session = time.time() - start_timestamp
    update_log(session)
    print(f"Total Time: {timeTransformer(get_total_time())}")
    print(f"Running: {is_vscode_running()}")

start_timestamp = None
is_timing = False
has_debugged = False
# Update the log and print the total programming time
while (True) :
    running = is_vscode_running()



    if running and not is_timing:
        start_timestamp = time.time()
        is_timing = True
        print("[Started Timing]")

    if not running and is_timing:
        session = time.time() - start_timestamp
        update_log(session)
        print(f"[Session Ended] + {timeTransformer(session)}")
        is_timing = False

    if not running and not is_timing:
        print("[Waiting for VS Code to start]")

    if not has_debugged:
        input_message = input("Enter 'd' to debug or any other key to continue: ")
        if input_message.lower() == 'd':
            debug()
            has_debugged = True
        else:
            print("Debugging skipped.")
            has_debugged = True
        has_debugged = True
    time.sleep(1)


