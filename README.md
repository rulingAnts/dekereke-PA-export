# Dekereke PA Export

Convert **Dekereke Phonology Assistant XML** databases to **Toolbox `.db` files** so that [SIL Phonology Assistant](https://software.sil.org/phonologyassistant/) can read them — without requiring FLEx (Fieldworks Language Explorer).

---

## Overview

Dekereke exports phonology data as XML. Phonology Assistant can import data from Toolbox SFM (Standard Format Marker) `.db` files. This tool bridges that gap directly, skipping the FLEx round-trip that would otherwise be required.

**Features:**
- GUI application — no Python installation needed
- Built-in default field mappings for Dekereke databases
- Custom CSV mapping support for non-standard field layouts
- Command-line interface for scripting and batch use
- Native app bundles for Windows (x64) and macOS (Apple Silicon)

---

## Download

Pre-built binaries are available on the [Releases page](https://github.com/rulingAnts/dekereke-PA-export/releases).

| Platform | Architecture | Download |
|----------|-------------|---------|
| Windows | x64 | [`sfm_convert_advanced.exe`](https://github.com/rulingAnts/dekereke-PA-export/releases/latest/download/sfm_convert_advanced.exe) |
| macOS | Apple Silicon (arm64) | [`sfm_convert_advanced-macos-arm64.zip`](https://github.com/rulingAnts/dekereke-PA-export/releases/latest/download/sfm_convert_advanced-macos-arm64.zip) |

For full documentation and a platform-detecting download page, visit the [project website](https://rulingAnts.github.io/dekereke-PA-export/).

---

## Usage

### GUI (recommended)

1. **Export** your Dekereke database as XML. The root element must be `<phon_data>` with child `<data_form>` elements.
2. **Launch** the application:
   - **Windows:** double-click `sfm_convert_advanced.exe`
   - **macOS:** unzip the download and open `sfm_convert_advanced.app` (right-click → Open on first launch to bypass Gatekeeper)
3. **Select** your XML file when prompted.
4. **Choose mappings:** click **Yes** for the built-in defaults, or **No** to supply a custom CSV mapping file.
5. The tool writes `<filename>.db` alongside your XML file. Add it as a data source in Phonology Assistant.

### Command Line

```bash
# Windows
sfm_convert_advanced.exe input.xml mappings.csv

# macOS
./sfm_convert_advanced.app/Contents/MacOS/sfm_convert_advanced input.xml mappings.csv
```

When two arguments are provided, the GUI prompts are skipped and the supplied CSV is used.

---

## Default Field Mappings

| SFM Code | XML Field Name   | Description                  |
|----------|-----------------|------------------------------|
| `\ref`   | Reference        | Unique record reference / ID |
| `\ge`    | Gloss            | English gloss                |
| `\gn`    | IndonesianGloss  | Indonesian gloss             |
| `\sf`    | SoundFile        | Linked audio file name       |
| `\ph`    | Phonetic         | Phonetic transcription       |
| `\ps`    | Category         | Part of speech / category    |
| `\var1`  | Variant1         | First phonological variant   |
| `\var2`  | Variant2         | Second phonological variant  |
| `\n`     | Notes            | Free-form notes              |

---

## Custom CSV Mapping

To map different field names, provide a `.csv` file with:

- **Row 1:** header (skipped automatically)
- **Column A:** SFM code (include the backslash, e.g. `\ref`)
- **Column B:** XML field name from your Dekereke export

Rows with an empty SFM code column are ignored.

---

## Output Format

The `.db` file uses the standard Toolbox SFM format:

```
\_sh v3.0  400  PhoneticData

\ref 001
\ge dog
\ph dɔg
\ps noun

\ref 002
\ge house
\ph haʊs
\ps noun
```

---

## Building from Source

Requirements: Python 3.11+, PyInstaller

```bash
# Clone the repository
git clone https://github.com/rulingAnts/dekereke-PA-export.git
cd dekereke-PA-export

pip install pyinstaller

# Windows
pyinstaller sfm_convert_advanced_windows.spec

# macOS
pyinstaller sfm_convert_advanced_gui.spec
```

Artifacts are placed in `dist/`.

---

## License

Copyright © 2025 Seth Johnston

This program is free software: you can redistribute it and/or modify it under the terms of the [GNU Affero General Public License v3.0](LICENSE) as published by the Free Software Foundation.
