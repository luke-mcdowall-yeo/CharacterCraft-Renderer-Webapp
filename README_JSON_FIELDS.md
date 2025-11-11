# JSON Schema Fields Reference

This document outlines the key fields from the JSON schema that the `generate_character_sheet.py` script checks for and handles.

## Table of Contents
- [Core Character Information](#core-character-information)
- [Species/Race Information](#speciesrace-information)
- [Class Information](#class-information)
- [Background Information](#background-information)
- [Ability Scores](#ability-scores)
- [Notes](#notes)
- [Error Handling](#error-handling)
- [Usage](#usage)

## Core Character Information
- `name` - Character name
- `alignment` - Character alignment (e.g., "Chaotic Neutral")
- `maxHP` - Maximum hit points (fallback to `currentHP`)
- `armorClass` - Armor class value

## Species/Race Information
- `species.name` - Species name (e.g., "Dragonborn [2024]")
- `species.description` - Detailed species description
- `species.size` - Character size (e.g., "Medium")
- `species.speed` - Movement speed (e.g., "30 ft.")

## Class Information
- `class` - Array of class objects, each containing:
  - `name` - Class name (e.g., "Fighter [2024]")
  - `level` - Class level

## Background Information
- `background.name` - Background name (e.g., "Custom Background [2024]")

## Ability Scores
The script checks for ability scores in two possible locations:
- `abilityScores` - Primary location for ability scores
- `attributes` - Fallback location for ability scores

### Supported Abilities
- Strength
- Dexterity
- Constitution
- Intelligence
- Wisdom
- Charisma

## Notes
- `notes` - Array of note objects, each containing:
  - `title` - Note title
  - `content` - Note content (supports various formats including JSON insert format)

## Error Handling
The script includes robust error handling for:
- Missing or malformed JSON files
- Missing required fields (uses sensible defaults)
- Invalid data types (converts or defaults as needed)
- Template processing errors
- File I/O errors

## Usage
```bash
python generate_character_sheet.py [json_file] [output_file] [template_file]
```

### Default Files
- **JSON Input:** `Talon_the_Pale_Reaper_Dragonborn_2024_Fighter_2024_Warlock_2024.json`
- **Template:** `character_template.html`
- **Output:** `character_sheet.html`