import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Frame, Label, Entry, Button
import random
import os
import json

class NPCGenerator:
    def __init__(self):
        # Get the directory where the script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define file paths
        self.appearances_file = os.path.join(self.script_dir, 'appearances.txt')
        self.roles_file = os.path.join(self.script_dir, 'roles.txt')
        self.hooks_file = os.path.join(self.script_dir, 'hooks.txt')
        
        # Load traits
        self.appearances = self.load_traits(self.appearances_file)
        self.roles = self.load_traits(self.roles_file)
        self.hooks = self.load_traits(self.hooks_file)
        
        # Initialize saved NPCs list
        self.saved_npcs = []
    
    def load_traits(self, file_path):
        """Load traits from a file, handling errors gracefully."""
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            filename = os.path.basename(file_path)
            print(f"Warning: Could not find {filename}")
            return []
    
    def generate_npc(self):
        """Generate a random NPC."""
        if not all([self.appearances, self.roles, self.hooks]):
            traits_missing = []
            if not self.appearances:
                traits_missing.append("appearances")
            if not self.roles:
                traits_missing.append("roles")
            if not self.hooks:
                traits_missing.append("hooks")
            
            return {
                "error": f"Error: Missing trait files: {', '.join(traits_missing)}",
                "appearance": "",
                "role": "",
                "hook": ""
            }
        
        return {
            "appearance": random.choice(self.appearances),
            "role": random.choice(self.roles),
            "hook": random.choice(self.hooks),
            "error": None
        }
    
    def format_npc(self, npc):
        """Format an NPC as a string."""
        if npc["error"]:
            return npc["error"]
        
        return (f"Appearance: {npc['appearance']}\n"
                f"Role: {npc['role']}\n"
                f"Hook: {npc['hook']}")
    
    def save_npc(self, npc, name=""):
        """Save an NPC to the collection."""
        if npc.get("error"):
            return False
            
        npc_with_name = npc.copy()
        npc_with_name["name"] = name or "Unnamed NPC"
        self.saved_npcs.append(npc_with_name)
        return True
    
    def export_saved_npcs(self, filename):
        """Export saved NPCs to a JSON file."""
        try:
            with open(filename, 'w') as file:
                json.dump(self.saved_npcs, file, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting NPCs: {str(e)}")
            return False
    
    def import_saved_npcs(self, filename):
        """Import saved NPCs from a JSON file."""
        try:
            with open(filename, 'r') as file:
                npcs = json.load(file)
                self.saved_npcs = npcs
            return True
        except Exception as e:
            print(f"Error importing NPCs: {str(e)}")
            return False


class NPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3 Line NPC Generator")
        self.root.geometry("600x500")
        
        # Create generator instance
        self.generator = NPCGenerator()
        
        # Current NPC
        self.current_npc = None
        
        # Create UI
        self.create_ui()
        
        # Generate initial NPC
        self.generate_npc()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
    
    def create_ui(self):
        """Create the user interface."""
        # Main frame with padding
        main_frame = Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title = Label(main_frame, text="3 Line NPC Generator", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # NPC output area with scrollbar
        self.output_area = scrolledtext.ScrolledText(
            main_frame, 
            height=10, 
            font=("Arial", 12),
            wrap=tk.WORD
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Name input area
        name_frame = Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(15, 5))
        
        name_label = Label(name_frame, text="NPC Name:", font=("Arial", 10))
        name_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.name_entry = Entry(name_frame, font=("Arial", 10), width=30)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons area
        button_frame = Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        # Generate button
        self.generate_btn = Button(
            button_frame, 
            text="Generate NPC (Space)", 
            command=self.generate_npc,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Save button
        self.save_btn = Button(
            button_frame, 
            text="Save NPC (Ctrl+S)", 
            command=self.save_npc,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # View saved button
        self.view_btn = Button(
            button_frame, 
            text="View Saved", 
            command=self.view_saved_npcs,
            font=("Arial", 10),
            padx=10
        )
        self.view_btn.pack(side=tk.LEFT, padx=5)
        
        # Export/Import buttons
        io_frame = Frame(main_frame)
        io_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.export_btn = Button(
            io_frame, 
            text="Export NPCs", 
            command=self.export_npcs,
            font=("Arial", 10),
            padx=10
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.import_btn = Button(
            io_frame, 
            text="Import NPCs", 
            command=self.import_npcs,
            font=("Arial", 10),
            padx=10
        )
        self.import_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = Label(main_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def bind_shortcuts(self):
        """Set up keyboard shortcuts."""
        self.root.bind("<space>", lambda e: self.generate_npc())
        self.root.bind("<Control-s>", lambda e: self.save_npc())
        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def generate_npc(self):
        """Generate and display a new NPC."""
        self.current_npc = self.generator.generate_npc()
        
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete('1.0', tk.END)
        
        formatted_npc = self.generator.format_npc(self.current_npc)
        self.output_area.insert(tk.END, formatted_npc)
        
        # Color code the sections
        if not self.current_npc.get("error"):
            self.output_area.tag_add("appearance", "1.0", "1.end")
            self.output_area.tag_add("role", "2.0", "2.end")
            self.output_area.tag_add("hook", "3.0", "3.end")
            
            self.output_area.tag_config("appearance", foreground="#333333", font=("Arial", 12, "bold"))
            self.output_area.tag_config("role", foreground="#0066CC", font=("Arial", 12, "bold"))
            self.output_area.tag_config("hook", foreground="#CC3300", font=("Arial", 12, "bold"))
        
        self.output_area.config(state=tk.DISABLED)
        
        # Update status
        if self.current_npc.get("error"):
            self.status_bar.config(text="Error: Missing trait files", fg="red")
        else:
            self.status_bar.config(text="NPC generated successfully", fg="green")
    
    def save_npc(self):
        """Save the current NPC."""
        if not self.current_npc:
            return
            
        if self.current_npc.get("error"):
            messagebox.showerror("Error", "Cannot save an NPC with missing traits")
            return
            
        name = self.name_entry.get().strip()
        result = self.generator.save_npc(self.current_npc, name)
        
        if result:
            npc_count = len(self.generator.saved_npcs)
            self.status_bar.config(
                text=f"NPC saved! You have {npc_count} saved NPC{'s' if npc_count != 1 else ''}",
                fg="green"
            )
    
    def view_saved_npcs(self):
        """Show a window with all saved NPCs."""
        if not self.generator.saved_npcs:
            messagebox.showinfo("No NPCs", "You haven't saved any NPCs yet")
            return
            
        # Create a new toplevel window
        saved_window = tk.Toplevel(self.root)
        saved_window.title("Saved NPCs")
        saved_window.geometry("500x400")
        
        # Create a scrolled text widget to display all NPCs
        display = scrolledtext.ScrolledText(saved_window, font=("Arial", 11))
        display.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Add each NPC to the display
        for i, npc in enumerate(self.generator.saved_npcs, 1):
            name = npc.get("name", f"NPC #{i}")
            
            display.insert(tk.END, f"--- {name} ---\n")
            display.insert(tk.END, f"Appearance: {npc['appearance']}\n")
            display.insert(tk.END, f"Role: {npc['role']}\n")
            display.insert(tk.END, f"Hook: {npc['hook']}\n\n")
        
        display.config(state=tk.DISABLED)
    
    def export_npcs(self):
        """Export saved NPCs to a file."""
        if not self.generator.saved_npcs:
            messagebox.showinfo("No NPCs", "You haven't saved any NPCs yet")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Export Saved NPCs"
        )
        
        if not filename:
            return
            
        success = self.generator.export_saved_npcs(filename)
        
        if success:
            messagebox.showinfo(
                "Export Successful", 
                f"Exported {len(self.generator.saved_npcs)} NPCs to {os.path.basename(filename)}"
            )
        else:
            messagebox.showerror("Export Failed", "Failed to export NPCs")
    
    def import_npcs(self):
        """Import NPCs from a file."""
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Import NPCs"
        )
        
        if not filename:
            return
            
        success = self.generator.import_saved_npcs(filename)
        
        if success:
            messagebox.showinfo(
                "Import Successful", 
                f"Imported {len(self.generator.saved_npcs)} NPCs"
            )
            self.status_bar.config(
                text=f"Imported {len(self.generator.saved_npcs)} NPCs",
                fg="green"
            )
        else:
            messagebox.showerror("Import Failed", "Failed to import NPCs")


def main():
    root = tk.Tk()
    app = NPCApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()