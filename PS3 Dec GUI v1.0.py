import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading

# Folder where PS3dec is located
def browse_program_folder():
    folder = filedialog.askdirectory()
    if folder:
        program_folder_var.set(folder)

# ISO file to Decrypt
def browse_iso_file():
    file_path = filedialog.askopenfilename(filetypes=[("ISO files", "*.iso")])
    if file_path:
        iso_file_var.set(file_path)

# Output for the decrypted ISO
def browse_save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".iso", filetypes=[("ISO files", "*.iso")])
    if file_path:
        save_file_var.set(file_path)

# Load the DKey from a file
def browse_dkey_file():
    file_path = filedialog.askopenfilename(filetypes=[("DKey files", "*.dkey *.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                dkey = file.read().strip()
                dkey_var.set(dkey)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read DKey file: {e}")

# Execute the ps3dec command in a separate thread
def run_command_in_thread():
    thread = threading.Thread(target=execute_command)
    thread.start()

# Eexecute the ps3dec command
def execute_command():
    program_folder = program_folder_var.get()
    dkey = dkey_var.get()
    iso_file = iso_file_var.get()
    save_file = save_file_var.get()

    if not all([program_folder, dkey, iso_file, save_file]):
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return
    
    command = f'cd /d "{program_folder}" && ps3dec d key {dkey} "{iso_file}" "{save_file}"'
    
    try:
        subprocess.Popen(command, shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# 
# Main application window
app = tk.Tk()
app.title("PS3dec GUI")

# Folder for ps3dec program
tk.Label(app, text="Program Folder:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
program_folder_var = tk.StringVar()
tk.Entry(app, textvariable=program_folder_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(app, text="Browse...", command=browse_program_folder).grid(row=0, column=2, padx=10, pady=5)

# DKey input
tk.Label(app, text="DKey:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
dkey_var = tk.StringVar()
tk.Entry(app, textvariable=dkey_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(app, text="Load from file...", command=browse_dkey_file).grid(row=1, column=2, padx=10, pady=5)

# ISO file to decrypt
tk.Label(app, text="ISO File:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
iso_file_var = tk.StringVar()
tk.Entry(app, textvariable=iso_file_var, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(app, text="Browse...", command=browse_iso_file).grid(row=2, column=2, padx=10, pady=5)

# Save file
tk.Label(app, text="Save As:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
save_file_var = tk.StringVar()
tk.Entry(app, textvariable=save_file_var, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(app, text="Browse...", command=browse_save_file).grid(row=3, column=2, padx=10, pady=5)

# Execute button
tk.Button(app, text="Execute", command=run_command_in_thread).grid(row=4, column=0, columnspan=3, pady=10)

app.mainloop()
