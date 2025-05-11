import tkinter as tk
import random
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to read lines from a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]  # Skip empty lines
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"Could not find file: {os.path.basename(file_path)}")
        return []

# File paths with correct directory
appearances_file = os.path.join(script_dir, 'appearances.txt')
roles_file = os.path.join(script_dir, 'roles.txt')
hooks_file = os.path.join(script_dir, 'hooks.txt')

# Create the main window before reading files
root = tk.Tk()
root.title("NPC Generator")
root.geometry("500x300")  # Set the window size

# Read traits from files
appearances = read_file(appearances_file)
roles = read_file(roles_file)
hooks = read_file(hooks_file)

# Function to generate a 3 Line NPC
def generate_3_line_npc():
    if not appearances or not roles or not hooks:
        return "Error: One or more trait files are missing or empty."
    
    appearance = random.choice(appearances)
    role = random.choice(roles)
    hook = random.choice(hooks)
    return f"Appearance: {appearance}\nRole: {role}\nHook: {hook}"

# Function to update the output in the same window
def update_output():
    npc = generate_3_line_npc()
    output_text.delete('1.0', tk.END)  # Clear the existing text
    output_text.insert(tk.END, npc)  # Insert the new NPC

# Output Text widget
output_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
output_text.pack(pady=20)

# Generate button
generate_button = tk.Button(root, text="Generate", command=update_output)
generate_button.pack(pady=20)

# Generate an NPC at startup
update_output()

# Run the main loop
root.mainloop()