# JSON to CSV Converter

A beautiful GUI application built with Python Tkinter for converting JSON files to CSV format.

## 🚀 Features

- **Modern GUI Interface**: Clean and intuitive design with progress tracking
- **Batch Processing**: Convert up to 50 JSON files at once
- **File Management**: Easy file selection, removal, and clearing
- **Output Control**: Choose your desired output folder
- **Progress Tracking**: Real-time progress bar and status updates
- **Error Handling**: Comprehensive error reporting with detailed results
- **Multi-threading**: Non-blocking conversion process

## 📋 Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)
- pandas
- json (built-in)
- csv (built-in)
- threading (built-in)
- pathlib (built-in)

## 🛠️ Installation

### Option 1: Download Executable (Recommended for Windows)
1. Go to the [Releases](https://github.com/brewmecoffee/json-to-csv-converter/releases) page
2. Download the latest `JSON_to_CSV_Converter.exe` file
3. Run the executable directly - no installation required!

### Option 2: Run from Source
1. Clone or download this repository:
   ```bash
   git clone https://github.com/brewmecoffee/json-to-csv-converter.git
   cd json-to-csv-converter
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python json_to_csv_converter.py
   ```

## 🎯 Usage

1. **Add Files**: Click "Add JSON Files" to select your JSON files (max 50)
2. **Choose Output**: Click "Browse" to select an output folder for the CSV files
3. **Convert**: Click "Convert to CSV" to start the conversion process
4. **Monitor**: Watch the real-time progress and view results in the results section

## 📊 Supported JSON Formats

- **Array of Objects**: `[{"key": "value"}, {"key": "value"}]`
- **Single Object**: `{"key": "value", "nested": {"key": "value"}}`
- **Nested Objects**: Automatically flattened using pandas.json_normalize()

## 📝 Example

**Input JSON:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "address": {
      "street": "123 Main St",
      "city": "New York"
    }
  }
]
```

**Output CSV:**
```csv
id,name,email,age,address.street,address.city
1,John Doe,john.doe@example.com,30,123 Main St,New York
```

## ✨ Features Overview

- **File Selection**: Supports multiple file selection with validation
- **Progress Tracking**: Real-time progress bar and status messages
- **Error Handling**: Detailed error messages for failed conversions
- **Results Display**: Shows successful and failed conversions
- **Threading**: Conversion runs in background to keep GUI responsive
- **Nested JSON**: Automatically flattens nested structures

## 🏗️ Building from Source

To create your own executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller JSON_to_CSV_Converter.spec
   ```

The executable will be created in the `dist/` folder.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/brewmecoffee/json-to-csv-converter/issues) on GitHub.

---

**Made with ❤️ for easy JSON to CSV conversion**
