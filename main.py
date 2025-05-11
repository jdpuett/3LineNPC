import tkinter as tk
import random

# Function to read lines from a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# File paths
appearances_file = 'appearances.txt'
roles_file = 'roles.txt'
hooks_file = 'hooks.txt'

# Read traits from files
appearances = read_file(appearances_file)
roles = read_file(roles_file)
hooks = read_file(hooks_file)

# Function to generate a 3 Line NPC
def generate_3_line_npc():
    appearance = random.choice(appearances)
    role = random.choice(roles)
    hook = random.choice(hooks)
    return f"Appearance: {appearance}\nRole: {role}\nHook: {hook}"

# Function to update the output in the same window
def update_output():
    npc = generate_3_line_npc()
    output_text.delete('1.0', tk.END)  # Clear the existing text
    output_text.insert(tk.END, npc)  # Insert the new NPC

# Main window
root = tk.Tk()
root.title("NPC Generator")
root.geometry("500x300")  # Set the window size

# Output Text widget
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=20)

# Generate button
generate_button = tk.Button(root, text="Generate", command=update_output)
generate_button.pack(pady=20)

# Run the main loop
root.mainloop()
