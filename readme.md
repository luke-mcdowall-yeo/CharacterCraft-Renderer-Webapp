# Printable Character Sheet Generator

A Python tool to generate printable D&D 5e character sheets from JSON data.

## Overview

This project converts D&D 5e character data stored in JSON format into beautifully formatted HTML character sheets. Perfect for players who want customizable, printer-friendly character records.

**Note:** This tool is designed to work with character JSON files exported from [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/).

## Features

- **Comprehensive Character Data**: Supports all core D&D 5e character information
- **Multi-class Support**: Handles multiple classes with different levels
- **Spellcasting Integration**: Organized spell lists with slot tracking
- **Equipment Management**: Weapons, armor, and inventory tracking
- **Customizable Template**: Modify the HTML template to customize appearance
- **Robust Error Handling**: Graceful fallbacks for missing or malformed data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CharacterCraft-Renderer
cd CharacterCraft-Renderer
```

2. Ensure you have Python 3.6+ installed

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Usage

#### Display Help

```bash
python generate_character_sheet.py --help
```

#### Basic Usage

Requires a character JSON file exported from [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/):

```bash
python generate_character_sheet.py my_character.json
```

This generates:
- Output: `my_character.html` (same name as input, with .html extension)
- Template: `character_template.html` (customizable)

#### Custom Files

```bash
python generate_character_sheet.py <json_file> [output_file] [template_file]
```

Examples:
```bash
# Generate with default output (input_name.html)
python generate_character_sheet.py my_character.json

# Generate with custom output filename
python generate_character_sheet.py my_character.json my_custom_sheet.html

# Generate with custom output and template
python generate_character_sheet.py my_character.json my_custom_sheet.html custom_template.html
```

### Web Usage

#### Local Development

```bash
python app.py
```

Visit `http://localhost:5000` and upload a character JSON file to generate your sheet.

#### Deploy to Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Make sure you have a `Procfile` in your project root with the following content:
```Procfile
web: gunicorn app:app
```
Also, ensure `gunicorn` is listed in your `requirements.txt` file.

5. Deploy your code:
```bash
git push heroku main
```

6. View your app:
```bash
heroku open
```

7. View logs:
```bash
heroku logs --tail
```

## Printing

### Windows

1. Generate your character sheet:
```bash
python generate_character_sheet.py my_character.json
```

2. Open the generated HTML file in your browser (double-click `my_character.html`)

3. Press `Ctrl+P` or `Cmd+P` to open the print dialog

4. Adjust print settings as needed

5. Click "Print" or save as PDF

## JSON Format

This tool works with character JSON files exported from [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/).

See [README_JSON_FIELDS.md](README_JSON_FIELDS.md) for detailed documentation of supported JSON fields and structure.

### How to Export from CharacterCraft

1. Open your character in [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/)
2. Look for an export or download option
3. Save the JSON file to your local machine
4. Use the filename as the input to this script

## File Structure

```
CharacterCraft-Renderer-Webapp/
├── generate_character_sheet.py       # Core generator script
├── app.py                            # Flask web application
├── character_template.html           # HTML template (customize this)
├── Procfile                          # Heroku configuration
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── README_JSON_FIELDS.md            # JSON schema documentation
└── example_character.json            # Example character data
```

## Template Customization

The `character_template.html` file uses Python string substitution. Modify it to customize:
- Layout and styling
- Color schemes
- Font choices
- Section organization

Available template variables:
- `$character_name`, `$species_name`, `$classes`, `$background`, `$alignment`
- `$max_hp`, `$armor_class`, `$initiative`, `$passive_perception`
- `$abilities_skills_grouped`, `$proficiencies`, `$languages`
- `$species_features`, `$class_features`, `$feats`
- `$spellcasting_sections`, `$spells_sections`, `$spell_details_sections`
- `$weapons`, `$inventory`, `$actions`
- `$bio`, `$notes`

## Supported Features

### Character Information
- Name, alignment, HP, AC
- Species with size and speed
- Multi-class support
- Background information

### Abilities & Skills
- Six core abilities (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma)
- Skill proficiencies and expertise
- Automatic modifier calculation

### Spellcasting
- Per-class spell slot tracking
- Spell attack bonus and save DC calculation
- Organized spell lists by level
- Support for invocations (Warlock)

### Equipment & Actions
- Weapon attacks with bonuses
- Inventory management
- Combat actions with recharge tracking
- Limited use abilities

### Additional Content
- Character bio and physical description
- Notes section
- Species traits and features
- Class features and feats

## Error Handling

The script includes comprehensive error handling for:
- Missing required arguments (displays usage instructions)
- Missing or malformed JSON files
- Missing required fields (uses sensible defaults)
- Invalid data types (converts or defaults as needed)
- Template processing errors
- File I/O errors

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Related Projects

- [CharacterCraft 5.5e](https://renanmgs.github.io/CharacterCraft_5.5e_Public/) - Character creation and management tool
