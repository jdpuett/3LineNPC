import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import random
import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import datetime

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
    
    def export_to_campaign_logger(self, filename):
        """Export saved NPCs to Campaign Logger XML format."""
        try:
            # Create root element
            root = ET.Element("entries")
            
            # Add metadata
            metadata = ET.SubElement(root, "metadata")
            ET.SubElement(metadata, "title").text = "3LineNPC Export"
            ET.SubElement(metadata, "date").text = datetime.datetime.now().strftime("%Y-%m-%d")
            ET.SubElement(metadata, "type").text = "npc"
            
            # Add each NPC as an entry
            for npc in self.saved_npcs:
                entry = ET.SubElement(root, "entry")
                
                # Add tags based on NPC type
                tags = ET.SubElement(entry, "tags")
                ET.SubElement(tags, "tag").text = "npc"
                
                # Add NPC details
                name = npc.get("name", "Unnamed NPC")
                ET.SubElement(entry, "title").text = name
                
                # Create content with appearance, role, and hook
                content = ET.SubElement(entry, "content")
                
                # Create HTML content for Campaign Logger
                content_text = f"<h3>Appearance</h3>\n<p>{npc.get('appearance', '')}</p>\n"
                content_text += f"<h3>Role</h3>\n<p>{npc.get('role', '')}</p>\n"
                content_text += f"<h3>Hook</h3>\n<p>{npc.get('hook', '')}</p>\n"
                
                content.text = content_text
                
                # Add creation date
                ET.SubElement(entry, "date").text = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Convert the XML to a pretty-printed string
            rough_string = ET.tostring(root, encoding='utf-8')
            parsed = minidom.parseString(rough_string)
            pretty_xml = parsed.toprettyxml(indent="  ")
            
            # Remove empty lines (a common issue with minidom)
            pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
            
            # Save the XML file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(pretty_xml)
            return True
        except Exception as e:
            print(f"Error exporting NPCs to Campaign Logger: {str(e)}")
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
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title = tk.Label(main_frame, text="3 Line NPC Generator", font=("Arial", 16, "bold"))
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
        name_frame = tk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(15, 5))
        
        name_label = tk.Label(name_frame, text="NPC Name:", font=("Arial", 10))
        name_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.name_entry = tk.Entry(name_frame, font=("Arial", 10), width=30)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons area
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        # Generate button - using tk.Button for macOS compatibility
        self.generate_btn = tk.Button(
            button_frame, 
            text="Generate NPC",
            command=self.generate_npc
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Save button - using tk.Button for macOS compatibility
        self.save_btn = tk.Button(
            button_frame, 
            text="Save NPC",
            command=self.save_npc
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # View saved button - using tk.Button for macOS compatibility
        self.view_btn = tk.Button(
            button_frame, 
            text="View Saved",
            command=self.view_saved_npcs
        )
        self.view_btn.pack(side=tk.LEFT, padx=5)
        
        # Export/Import buttons
        io_frame = tk.Frame(main_frame)
        io_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.export_btn = tk.Button(
            io_frame, 
            text="Export NPCs",
            command=self.export_npcs
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.import_btn = tk.Button(
            io_frame, 
            text="Import NPCs",
            command=self.import_npcs
        )
        self.import_btn.pack(side=tk.LEFT, padx=5)
        
        # Campaign Logger Export button
        self.export_cl_btn = tk.Button(
            io_frame, 
            text="Export to Campaign Logger",
            command=self.export_to_campaign_logger
        )
        self.export_cl_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def bind_shortcuts(self):
        """Set up keyboard shortcuts with focus checking to prevent conflicts."""
        # Space key generates NPC, but only when not focused on text input
        def space_handler(event):
            # Don't trigger when the focus is in the name entry
            if event.widget != self.name_entry:
                self.generate_npc()
        
        # Bind space key with the handler that checks for focus
        self.root.bind("<space>", space_handler)
        
        # Other shortcuts work regardless of focus
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
    
    def export_to_campaign_logger(self):
        """Export saved NPCs to Campaign Logger XML format."""
        if not self.generator.saved_npcs:
            messagebox.showinfo("No NPCs", "You haven't saved any NPCs yet")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")],
            title="Export to Campaign Logger"
        )
        
        if not filename:
            return
            
        success = self.generator.export_to_campaign_logger(filename)
        
        if success:
            messagebox.showinfo(
                "Export Successful", 
                f"Exported {len(self.generator.saved_npcs)} NPCs to Campaign Logger format"
            )
            self.status_bar.config(
                text=f"Exported {len(self.generator.saved_npcs)} NPCs to Campaign Logger",
                fg="green"
            )
        else:
            messagebox.showerror("Export Failed", "Failed to export NPCs to Campaign Logger")
    
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