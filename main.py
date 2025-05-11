import tkinter as tk
import random
import os
import json
from tkinter import messagebox, scrolledtext, filedialog

class NPCGenerator:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.appearances = self.load_traits("appearances.txt")
        self.roles = self.load_traits("roles.txt")
        self.hooks = self.load_traits("hooks.txt")
        self.saved_npcs = []
    
    def load_traits(self, filename):
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"Could not find {filename}")
            return []
    
    def generate_npc(self):
        if not (self.appearances and self.roles and self.hooks):
            return "Error: One or more trait files are empty or missing."
        
        return {
            "appearance": random.choice(self.appearances),
            "role": random.choice(self.roles),
            "hook": random.choice(self.hooks)
        }
    
    def format_npc(self, npc):
        return f"Appearance: {npc['appearance']}\nRole: {npc['role']}\nHook: {npc['hook']}"
    
    def save_npc(self, npc, name=""):
        npc_with_name = npc.copy()
        npc_with_name["name"] = name
        self.saved_npcs.append(npc_with_name)
        
    def export_saved_npcs(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.saved_npcs, file, indent=4)


class NPCGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.generator = NPCGenerator()
        self.current_npc = None
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("3 Line NPC Generator")
        self.root.geometry("600x400")
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output area
        self.output_text = scrolledtext.ScrolledText(main_frame, height=10, width=60, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate button
        generate_btn = tk.Button(button_frame, text="Generate NPC", command=self.generate_npc)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_btn = tk.Button(button_frame, text="Save NPC", command=self.save_npc)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = tk.Button(button_frame, text="Export Saved NPCs", command=self.export_npcs)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # NPC Name entry
        name_frame = tk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=5)
        tk.Label(name_frame, text="NPC Name:").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def generate_npc(self):
        self.current_npc = self.generator.generate_npc()
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, self.generator.format_npc(self.current_npc))
        
    def save_npc(self):
        if not self.current_npc:
            messagebox.showinfo("No NPC", "Generate an NPC first!")
            return
            
        name = self.name_entry.get().strip() or "Unnamed NPC"
        self.generator.save_npc(self.current_npc, name)
        messagebox.showinfo("Saved", f"NPC '{name}' saved!")
        
    def export_npcs(self):
        if not self.generator.saved_npcs:
            messagebox.showinfo("No NPCs", "No NPCs have been saved yet!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if filename:
            self.generator.export_saved_npcs(filename)
            messagebox.showinfo("Export Complete", f"Saved {len(self.generator.saved_npcs)} NPCs to {filename}")


def main():
    root = tk.Tk()
    app = NPCGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()