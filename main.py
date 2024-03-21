from tqdm import tqdm
import subprocess

def run_script(script_path, desc):
    with tqdm(total=1, desc=desc, unit="script") as pbar:
        try:
            subprocess.run([script_path], check=True)  # Raise an exception if script fails
            pbar.update(1)  # Update progress bar if successful
        except subprocess.CalledProcessError as e:
            print(f"Error: Script '{script_path}' failed with exit code {e.returncode}.")

if __name__ == "__main__":
    scripts = ["get.py", "down.py", "mode.py"]
    for script in scripts:
        run_script(script, desc=script)  # Run each script with a progress bar

    print("All scripts completed successfully!")