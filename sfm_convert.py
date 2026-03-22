#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import csv
import os

# Configuration parameters (update these as needed)
XML_FILE = "testDB.xml"  # Path to the XML file
CSV_FILE = "sfm_codes.csv"  # Path to the CSV mapping file

# Determine the output filename (same as XML but with .db extension)
OUTPUT_FILE = os.path.splitext(XML_FILE)[0] + ".db"

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
        print("Error: Root element is not <phon_data>.")
        return
    
    output_lines = []
    
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

def write_output_file(output_file, lines):
    """Writes the extracted text to the output .db file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    mapping = load_csv_mapping(CSV_FILE)
    if not mapping:
        print("Error: CSV mapping is empty or invalid.")
        return
    
    output_lines = process_xml(XML_FILE, mapping)
    if output_lines:
        write_output_file(OUTPUT_FILE, output_lines)
        print(f"Output written to: {OUTPUT_FILE}")
    else:
        print("No data processed from XML.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
