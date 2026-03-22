#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import csv
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Default mappings dictionary (you can easily add/update mappings here)
DEFAULT_MAPPINGS = {
    "\\ref": "Reference",
    "\\ge": "Gloss",
    "\\gn": "IndonesianGloss",
    "\\sf": "SoundFile",
    "\\ph": "Phonetic",
    "\\ps": "Category",
    "\\var1": "Variant1",
    "\\var2": "Variant2",
    "\\n": "Notes"
}



def convert_dict_to_tuple_list(mapping_dict):
    """Converts the default mappings dictionary to a list of tuples."""
    return [(label, tag) for label, tag in mapping_dict.items()]

def load_csv_mapping(csv_file):
    """Loads the CSV mapping into a list of tuples (label, xml_tag), skipping the header row."""
    mapping = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header row
        for row in reader:
            if len(row) >= 2:
                label, xml_tag = row[0].strip(), row[1].strip()
                mapping.append((label, xml_tag))
    return mapping

def process_xml(xml_file, mapping):
    """Processes the XML file and generates the output text based on the CSV mapping."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    if root.tag != "phon_data":
        messagebox.showerror("Error", "Root element is not <phon_data>.")
        return
    
    output_lines = ["\\_sh v3.0  400  PhoneticData\n"]
    
    # Iterate through data_form elements
    for data_form in root.findall("data_form"):
        for label, xml_tag in mapping:
            if label and xml_tag:  # Only process non-blank labels
                element = data_form.find(xml_tag)
                if element is not None and element.text:
                    output_lines.append(f"{label} {element.text.strip()}")
        
        # Add two blank lines after processing each data_form
        output_lines.append("\n")
        output_lines.append("\n")
    
    return output_lines

def write_output_file(xml_file, lines):
    """Writes the extracted text to the output .db file."""
    output_file = os.path.splitext(xml_file)[0] + ".db"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    messagebox.showinfo("Success", f"Output written to: {output_file}")

def get_files_from_gui():
    """Opens a GUI for file selection."""
    root = tk.Tk()
    root.withdraw()
    
    xml_file = filedialog.askopenfilename(title="Select XML File", filetypes=[("XML Files", "*.xml")])
    if not xml_file:
        messagebox.showerror("Error", "No XML file selected. Exiting.")
        sys.exit()
    
    return xml_file

def ask_use_default_mappings():
    """Ask the user if they want to use default mappings or provide a CSV."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    use_default = messagebox.askyesno("Use Default Mappings", 
                                      "Do you want to use the default mappings?\nClick 'No' to provide your own CSV file.")
    return use_default

def main():
    if len(sys.argv) == 3:
        xml_file, csv_file = sys.argv[1], sys.argv[2]
    else:
        xml_file = get_files_from_gui()
        
        # Ask if the user wants to use default mappings or supply a CSV
        use_default = ask_use_default_mappings()
        
        if use_default:
            mapping = convert_dict_to_tuple_list(DEFAULT_MAPPINGS)
        else:
            messagebox.showinfo("Instructions","Select a CSV file (you can export Excel sheets as CSV) with mappings of SFM codes to Dekereke Fields. Data in Row 1 will be ignored. Column A should have SFM codes (including \\) and Column B should have the Dekereke Field Names that match them. Empty SFM cells will be ignored.")
            csv_file = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
            if not csv_file:
                messagebox.showerror("Error", "No CSV file selected. Exiting.")
                sys.exit()
            mapping = load_csv_mapping(csv_file)
    
    if not mapping:
        messagebox.showerror("Error", "Mapping is empty or invalid.")
        return
    
    output_lines = process_xml(xml_file, mapping)
    if output_lines:
        write_output_file(xml_file, output_lines)
    else:
        messagebox.showwarning("Warning", "No data processed from XML.")

if __name__ == "__main__":
    main()
