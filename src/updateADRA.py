### 2024 Alex Poulin
import os
import subprocess
import sys
import time

# Path to the Git repository (the directory containing this script)
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# Interval in seconds to check for updates
CHECK_INTERVAL = 300  # e.g., 5 minutes

def check_for_updates():
    """
    Pull the latest changes from the remote Git repository.
    Returns True if updates were pulled, False otherwise.
    """
    try:
        # Move to the repository path
        os.chdir(REPO_PATH)

        # Fetch updates from the remote
        fetch_output = subprocess.check_output(["git", "fetch"]).decode()
        
        # Check if there are updates
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", "@{u}"]).decode().strip()

        # If the commits are different, there are updates to pull
        if local_commit != remote_commit:
            print("Updates found, pulling changes...")
            subprocess.check_call(["git", "pull"])
            return True
        else:
            print("No updates found.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def restart_script():
    """Restart the current Python script."""
    print("Restarting script to apply updates...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

def main():
    """Main loop to periodically check for updates."""
    while True:
        print("Checking for updates...")
        if check_for_updates():
            print("Found Update... beginning...")
            restart_script()
        time.sleep(CHECK_INTERVAL)

'''
if __name__ == "__main__":
    main()
'''