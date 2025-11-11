# D&D 5e Character Sheet Generator

## Overview
This is a web-based D&D 5th Edition character sheet generator that converts character data from CharacterCraft 5.5e JSON exports into beautifully formatted, printable HTML character sheets.

**Status**: Fully functional web application
**Last Updated**: November 11, 2025

## Project Structure

### Core Components
- **app.py** - Flask web server that handles file uploads and character sheet generation
- **generate_character_sheet.py** - Core Python script that processes JSON data and fills the HTML template
- **character_template.html** - HTML template with CSS styling for the character sheet output
- **templates/** - Flask HTML templates for the web interface
- **static/** - CSS and JavaScript files for the frontend

### Directories
- **uploads/** - Temporary storage for uploaded JSON files
- **outputs/** - Generated character sheet HTML files
- **templates/** - Flask Jinja2 templates
- **static/css/** - Stylesheets
- **static/js/** - JavaScript files

## Features
- 🎲 Web-based file upload interface with drag-and-drop support
- 📄 Comprehensive D&D 5e character data display
- 🎭 Multi-class support
- ✨ Spellcasting integration with spell slot tracking
- ⚔️ Equipment and inventory management
- 🖨️ Printer-friendly format
- 📥 View or download generated character sheets

## Tech Stack
- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Template Engine**: Jinja2 (for Flask) and Python Template (for character sheets)
- **Package Manager**: UV

## How It Works
1. User uploads a CharacterCraft 5.5e JSON export via the web interface
2. Flask backend receives the file and saves it to the uploads directory
3. The `generate_character_sheet.py` script processes the JSON data
4. Character data is filled into the HTML template
5. Generated HTML is saved to the outputs directory
6. User can view the sheet in browser or download it

## Usage
Visit the web interface and:
1. Upload your CharacterCraft 5.5e JSON file
2. Wait for processing
3. View or download your printable character sheet

## Dependencies
- Flask 3.1.2
- Python 3.11 (standard library only for character generation)

## Configuration
- **Server**: Runs on 0.0.0.0:5000
- **Debug Mode**: Enabled for development
- **Upload Folder**: ./uploads
- **Output Folder**: ./outputs

## Notes
- This tool is designed to work with character JSON files exported from [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/)
- The character sheet template uses a printer-friendly format
- Generated sheets can be saved as PDF using the browser's print function
