import tkinter as tk
import subprocess

def run_script1():
    subprocess.Popen(["python", "graph.py"])

def run_script2():
    indicator_label.config(text="Running get.py...")
    indicator_label.update()
    subprocess.Popen(["python", "get.py"])
    indicator_label.config(text="")

def run_script3():
    subprocess.Popen(["python", "like.py"])

root = tk.Tk()
root.title("Python Script Launcher")

button1 = tk.Button(root, text="Run Stock Graph", command=run_script1)
button1.pack(pady=20)

button2 = tk.Button(root, text="Get Data", command=run_script2)
button2.pack(pady=20)

button3 = tk.Button(root, text="Show Liked Results", command=run_script3)
button3.pack(pady=20)

indicator_label = tk.Label(root, text="", fg="blue")
indicator_label.pack(pady=10)

root.mainloop()
