import sys
import ctypes
import subprocess
import time
import logging
import schedule as sc

# Create the log file if it doesn't already exist
LOG_FILE = "wifi_status_log.txt"
PING_HOST = "www.google.com"

try:
    with open(LOG_FILE, 'x') as file:
        file.write("Logs:\n")
    print(f"File '{LOG_FILE}' created successfully.")
except FileExistsError:
    print(f"File '{LOG_FILE}' already exists.")

# Set up logging to log to a file with timestamps
logging.basicConfig(filename=LOG_FILE, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s', 
                    filemode='a')  # Append mode

def enable():
    try:
        if sys.platform.startswith("win"):
            subprocess.call("netsh interface set interface Wi-Fi enabled", shell=True)
            print("Turning On the laptop WiFi")
            logging.info("WiFi enabled")
        else:
            # Linux/Mac alternative (optional: using nmcli if available)
            subprocess.call("nmcli radio wifi on", shell=True)
            print("Turning On the laptop WiFi (Linux/Mac)")
            logging.info("WiFi enabled (Linux/Mac)")
    except Exception as e:
        print(f"Failed to enable WiFi: {e}")
        logging.error(f"Failed to enable WiFi: {e}")

def disable():
    try:
        if sys.platform.startswith("win"):
            subprocess.call("netsh interface set interface Wi-Fi disabled", shell=True)
            print("Turning Off the laptop WiFi")
            logging.info("WiFi disabled")
        else:
            # Linux/Mac alternative (optional: using nmcli if available)
            subprocess.call("nmcli radio wifi off", shell=True)
            print("Turning Off the laptop WiFi (Linux/Mac)")
            logging.info("WiFi disabled (Linux/Mac)")
    except Exception as e:
        print(f"Failed to disable WiFi: {e}")
        logging.error(f"Failed to disable WiFi: {e}")

def job():
    try:
        if sys.platform.startswith("win"):
            subprocess.call("netsh interface set interface Wi-Fi enabled", shell=True)
        else:
            subprocess.call("nmcli radio wifi on", shell=True)
        print("WiFi is enabled and connected to internet")
        logging.info("WiFi is enabled and connected to the internet.")
        
        response = subprocess.call(f"ping -n 1 {PING_HOST}" if sys.platform.startswith("win") else f"ping -c 1 {PING_HOST}", shell=True)
        
        if response != 0:
            print("Your Connection is not working")
            logging.warning("WiFi connection not working, ping failed.")

            attempt_counter = 0
            max_attempts = 3

            while attempt_counter < max_attempts:
                print(f"Attempt {attempt_counter + 1} to reconnect...")
                logging.info(f"Attempt {attempt_counter + 1} to reconnect...")
                
                disable()
                time.sleep(1)
                enable()

                time.sleep(5)

                response = subprocess.call(f"ping -n 1 {PING_HOST}" if sys.platform.startswith("win") else f"ping -c 1 {PING_HOST}", shell=True)
                if response == 0:
                    print("Reconnection successful!")
                    logging.info("Reconnection successful!")
                    break
                else:
                    print(f"Reconnection attempt {attempt_counter + 1} failed.")
                    logging.warning(f"Reconnection attempt {attempt_counter + 1} failed.")
                
                attempt_counter += 1

            if attempt_counter == max_attempts and response != 0:
                print(f"Failed to reconnect after {max_attempts} attempts.")
                logging.error(f"Failed to reconnect after {max_attempts} attempts.")
    except Exception as e:
        print(f"Error during WiFi check: {e}")
        logging.error(f"Error during WiFi check: {e}")

def is_admin():
    try:
        if sys.platform.startswith("win"):
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            # On Linux/Mac, assume admin privileges (or implement an alternative check)
            return True
    except Exception as e:
        logging.error(f"Admin check failed: {e}")
        return False

# Schedule the job based on the operating system:
if sys.platform.startswith("win"):
    if is_admin():
        sc.every(50).seconds.do(job)
    else:
        # Only attempt elevation on Windows
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    # Linux/Mac: schedule the job without elevation
    sc.every(50).seconds.do(job)

# For testing in Jenkins, run the scheduler for a fixed number of iterations and then exit.
iterations = 5  # adjust the number of iterations as needed
for _ in range(iterations):
    sc.run_pending()
    time.sleep(1)

print("Job finished after fixed iterations.")
