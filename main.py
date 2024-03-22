from tqdm import tqdm
import subprocess
import sys
import os

def run_script(script_name, desc):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    python_executable = sys.executable  # Get path to the Python interpreter
    with tqdm(total=1, desc=desc, unit="script") as pbar:
        try:
            subprocess.run([python_executable, script_path], check=True)  # Execute script with Python interpreter
            pbar.update(1)  # Update progress bar if successful
        except subprocess.CalledProcessError as e:
            print(f"Error: Script '{script_name}' failed with exit code {e.returncode}.")

if __name__ == "__main__":
    scripts = ["get.py", "down.py", "model.py"]
    for script in scripts:
        run_script(script, desc=script)  # Run each script with a progress bar

    print("All scripts completed successfully!")
