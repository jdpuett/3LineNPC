import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import datetime
import os
from tkinter import filedialog

def export_to_campaign_logger(npcs, default_filename=None):
    """
    Export NPCs to Campaign Logger XML format
    
    Args:
        npcs: List of NPC dictionaries, each with 'title', 'appearance', 'role', and 'hook' keys
        default_filename: Optional default filename to suggest
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    # Create root element
    root = ET.Element("entries")
    
    # Add metadata
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "title").text = "3LineNPC Export"
    ET.SubElement(metadata, "date").text = datetime.datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(metadata, "type").text = "npc"
    
    # Add each NPC as an entry
    for npc in npcs:
        entry = ET.SubElement(root, "entry")
        
        # Add tags based on NPC type
        tags = ET.SubElement(entry, "tags")
        ET.SubElement(tags, "tag").text = "npc"
        
        # Add NPC details
        ET.SubElement(entry, "title").text = npc.get("title", "Unnamed NPC")
        
        # Create content with appearance, role, and hook
        content = ET.SubElement(entry, "content")
        
        # Create a CDATA section for the content
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
    
    # Ask user where to save the file
    if default_filename is None:
        default_filename = f"3LineNPC_Export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    
    filename = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".xml",
        filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")],
        title="Export to Campaign Logger XML"
    )
    
    if not filename:  # User cancelled
        return False
    
    # Save the XML file
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(pretty_xml)
        return True
    except Exception as e:
        print(f"Error saving XML file: {e}")
        return False
    