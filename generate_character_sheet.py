import json
from string import Template

# HTML Templates
FEATURE_ITEM = Template('<div class="feature-item"><strong>$name</strong><div class="feature-text">$description</div></div>')
SPELL_ITEM = Template('<div class="feature-item"><strong>$name</strong> ($school)<div class="feature-text"><em>Casting Time:</em> $casting_time, <em>Range:</em> $range, <em>Duration:</em> $duration<br>$description</div></div>')
WEAPON_ITEM = Template('<div class="feature-item"><strong>$name</strong><div class="feature-text"><em>Attack Bonus:</em> +$hit_bonus, <em>Damage:</em> $damage<br><em>Properties:</em> $properties</div></div>')
INVENTORY_ITEM = Template('<div class="feature-item"><strong>$name$status</strong><div class="feature-text"><em>Type:</em> $type, <em>Quantity:</em> $quantity, <em>Weight:</em> $weight lbs</div></div>')
ABILITY_GROUP = Template('<div class="ability-group"><div class="abilities-skills-layout"><div class="stat"><label>$short_name</label><div class="stat-value">$score</div><div class="stat-mod">$modifier</div></div><div class="skills-box">$skills</div></div></div>')
SKILL_ITEM = Template('<div class="skill-item"><span class="skill-name">$name</span>$prof_indicator<span class="skill-bonus">$bonus</span></div>')

def style_source_text(text):
    """Style Source: text to be lighter and italic"""
    import re
    return re.sub(r'(Source:.*?)(?=<br>|$)', r'<span style="color: #888; font-style: italic;">\1</span>', text, flags=re.DOTALL)

def load_json_data(json_file):
    """Load JSON data from file with error handling"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Validate that we have the minimum required fields
            if not isinstance(data, dict):
                raise ValueError("JSON data must be an object")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

def extract_features(features_data):
    """Extract and format features from JSON data"""
    if not features_data:
        return "No features available"
    
    features_html = []
    if isinstance(features_data, list):
        for feature in features_data:
            if isinstance(feature, dict):
                name = feature.get('name', 'Unknown Feature') + ':'
                description = feature.get('description', feature.get('text', '')).replace('\n', '<br>')
                description = style_source_text(description)
                features_html.append(FEATURE_ITEM.substitute(name=name, description=description))
            elif isinstance(feature, str):
                features_html.append(FEATURE_ITEM.substitute(name='', description=feature))
    
    return ''.join(features_html) if features_html else "No features available"

def extract_class_features(class_features_data, character_level):
    """Extract class features up to character level"""
    if not class_features_data:
        return "No features available"
    
    features_html = []
    for level_str, level_features in class_features_data.items():
        try:
            level = int(level_str)
            if level <= character_level and isinstance(level_features, list):
                for feature in level_features:
                    if isinstance(feature, dict):
                        name = feature.get('name', 'Unknown Feature') + ':'
                        description = feature.get('description', '').replace('\n', '<br>')
                        description = style_source_text(description)
                        features_html.append(FEATURE_ITEM.substitute(name=name, description=description))
        except ValueError:
            continue
    
    return ''.join(features_html) if features_html else "No features available"

def extract_spells(spells_data, class_name=None):
    """Extract and format spells from JSON data, organized by level"""
    if not spells_data:
        return "No spells available", "No spells available"
    
    # Filter spells by class if specified
    filtered_spells = spells_data
    if class_name:
        filtered_spells = [s for s in spells_data if isinstance(s, dict) and 
                          class_name in s.get('preparingClass', '')]
        # Include invocations for Warlock
        if 'Warlock' in class_name:
            invocations = [s for s in spells_data if isinstance(s, dict) and 
                          s.get('school') == 'Invocation']
            filtered_spells.extend(invocations)
    
    if not filtered_spells:
        return "No spells available", "No spells available"
    
    # Separate invocations from regular spells
    invocations = [s for s in filtered_spells if isinstance(s, dict) and 
                  s.get('school') == 'Invocation']
    regular_spells = [s for s in filtered_spells if isinstance(s, dict) and 
                     s.get('school') != 'Invocation']
    
    # Organize spells by level
    spells_by_level = {}
    for spell in regular_spells:
        if isinstance(spell, dict):
            level = spell.get('level', 0)
            if level not in spells_by_level:
                spells_by_level[level] = []
            spells_by_level[level].append(spell)
    
    # Short list - just names with preparing class
    short_list = []
    detailed_list = []
    
    # Add invocations section if any exist
    if invocations:
        short_list.append(f"<p><strong>Invocations:</strong></p>")
        for inv in invocations:
            name = inv.get('title', 'Unknown Invocation')
            short_list.append(f'<div class="feature-item"><strong>{name}</strong></div>')
        
        detailed_list.append(f"<h4>Invocations</h4>")
        for inv in invocations:
            name = inv.get('title', 'Unknown Invocation')
            description = inv.get('description', '').replace('\n', '<br>')
            description = style_source_text(description)
            detailed_list.append(FEATURE_ITEM.substitute(name=name, description=description))
    
    # Sort levels (cantrips first, then 1st, 2nd, etc.)
    for level in sorted(spells_by_level.keys()):
        level_name = "Cantrips" if level == 0 else f"Level {level}"
        short_list.append(f"<p><strong>{level_name}:</strong></p>")
        for spell in spells_by_level[level]:
            name = spell.get('title', 'Unknown Spell')
            prep_class = spell.get('preparingClass', 'Known')
            if prep_class == '':
                prep_class = 'Known'
            short_list.append(f'<div class="feature-item"><strong>{name}</strong> <em>({prep_class})</em></div>')
        
        detailed_list.append(f"<h4>{level_name} Spells</h4>")
        for spell in spells_by_level[level]:
            name = spell.get('title', 'Unknown Spell')
            school = spell.get('school', '')
            casting_time = spell.get('castingTime', '')
            range_val = spell.get('range', '')
            duration = spell.get('duration', '')
            description = spell.get('description', '').replace('\n', '<br>')
            description = style_source_text(description)
            
            detailed_list.append(SPELL_ITEM.substitute(
                name=name, school=school, casting_time=casting_time,
                range=range_val, duration=duration, description=description
            ))
    
    return ''.join(short_list) if short_list else "No spells available", ''.join(detailed_list) if detailed_list else "No spells available"

def extract_weapons(equipment_data, proficiency_bonus=2):
    """Extract weapons from equipment data"""
    if not equipment_data:
        return "No weapons available"
    
    weapons_html = []
    for item in equipment_data:
        if isinstance(item, dict) and item.get('type') == 'Melee Weapon':
            name = item.get('title', 'Unknown Weapon')
            hit_bonus = item.get('hitBonus', 0)
            damages = item.get('damages', {})
            damage_str = ', '.join([f"{dmg_type}: {formula.replace('+pb', f'+{proficiency_bonus}')}" for dmg_type, formula in damages.items()])
            properties = item.get('properties', '')
            
            weapons_html.append(WEAPON_ITEM.substitute(
                name=name, hit_bonus=hit_bonus, damage=damage_str, properties=properties
            ))
    
    return ''.join(weapons_html) if weapons_html else "No weapons available"

def extract_inventory(equipment_data):
    """Extract inventory items from equipment data"""
    if not equipment_data:
        return "No items available"
    
    inventory_html = []
    for item in equipment_data:
        if isinstance(item, dict):
            name = item.get('title', 'Unknown Item')
            quantity = item.get('quantity', 1)
            weight = item.get('weight', 0)
            item_type = item.get('type', 'Item')
            equipped = item.get('equipped', False)
            
            status = " (Equipped)" if equipped else ""
            inventory_html.append(INVENTORY_ITEM.substitute(
                name=name, status=status, type=item_type, quantity=quantity, weight=weight
            ))
    
    return ''.join(inventory_html) if inventory_html else "No items available"

def extract_actions(data):
    """Extract combat actions with limited uses and recharge info"""
    import re
    actions_html = []
    proficiency_bonus = data.get('proficiencyBonus', 2)
    abilities = data.get('abilityScores', data.get('attributes', {}))
    
    def calculate_uses(feature):
        uses = 0
        custom_fields = feature.get('customFields', {})
        for field_name, field_data in custom_fields.items():
            if isinstance(field_data, dict) and 'scaling' in field_data:
                scaling = field_data['scaling']
                base = scaling.get('baseValue', 0)
                scale_type = scaling.get('type', '')
                
                if scale_type == 'proficiency':
                    uses = proficiency_bonus + base
                elif scale_type == 'attribute':
                    attr = scaling.get('attribute', '')
                    ability_score = abilities.get(attr, 10)
                    try:
                        ability_score = int(ability_score)
                    except (ValueError, TypeError):
                        ability_score = 10
                    modifier = (ability_score - 10) // 2
                    uses = max(1, modifier + base)
                elif scale_type == 'level':
                    total_level = sum(c.get('level', 1) for c in data.get('class', []) if isinstance(c, dict))
                    uses = total_level + base
        
        if uses == 0:
            uses = int(feature.get('customResource', 0)) if feature.get('customResource') else 0
        return uses
    
    # Add attack action with equipped weapons
    equipment_data = data.get('equipment', [])
    equipped_weapons = [item.get('title', 'Weapon') for item in equipment_data if isinstance(item, dict) and item.get('equipped') and 'Weapon' in item.get('type', '')]
    if equipped_weapons:
        weapons_list = ', '.join(equipped_weapons)
        actions_html.append(f'<div class="feature-item"><strong>Attack</strong><div class="feature-text">{weapons_list}</div></div>')
    else:
        actions_html.append('<div class="feature-item"><strong>Attack</strong></div>')
    
    # Add species-specific actions
    species_data = data.get('species', {})
    if isinstance(species_data, dict):
        traits = species_data.get('traits', [])
        for trait in traits:
            if isinstance(trait, dict):
                name = trait.get('name', '')
                description = trait.get('description', '')
                if 'breath' in name.lower() or 'action' in description.lower():
                    uses = calculate_uses(trait)
                    if uses == 0:
                        uses_match = re.search(r'use this feature (once|twice|thrice|\d+ times?)', description, re.IGNORECASE)
                        if uses_match:
                            use_text = uses_match.group(1).lower()
                            if use_text == 'once': uses = 1
                            elif use_text == 'twice': uses = 2
                            elif use_text == 'thrice': uses = 3
                            else: uses = int(re.search(r'\d+', use_text).group())
                    
                    recharge_match = re.search(r'Short Rest|Long Rest', description)
                    recharge = 'Short' if recharge_match and 'Short' in recharge_match.group() else ('Long' if recharge_match else '')
                    
                    if uses > 0:
                        boxes = ''.join(['<span class="prof-indicator"></span>'] * uses)
                        recharge_text = f'{recharge} Rest' if recharge else ''
                        actions_html.append(f'<div class="feature-item"><strong>{name}</strong><div class="uses-row"><span>{recharge_text}</span><span class="uses-boxes">{boxes}</span></div></div>')
                    else:
                        actions_html.append(f'<div class="feature-item"><strong>{name}</strong></div>')
    
    # Add class-specific actions
    features_data = data.get('featuresAndTraits', [])
    if isinstance(features_data, list):
        for feature in features_data:
            if isinstance(feature, dict):
                name = feature.get('name', '')
                description = feature.get('description', '')
                desc_lower = description.lower()
                if any(keyword in desc_lower for keyword in ['action', 'bonus action', 'reaction']) or re.search(r'\battack\b', desc_lower):
                    uses = calculate_uses(feature)
                    if uses == 0:
                        uses_match = re.search(r'use this feature (once|twice|thrice|\d+ times?)', description, re.IGNORECASE)
                        if uses_match:
                            use_text = uses_match.group(1).lower()
                            if use_text == 'once': uses = 1
                            elif use_text == 'twice': uses = 2
                            elif use_text == 'thrice': uses = 3
                            else: uses = int(re.search(r'\d+', use_text).group())
                    
                    recharge_match = re.search(r'Short Rest|Long Rest', description)
                    recharge = 'Short' if recharge_match and 'Short' in recharge_match.group() else ('Long' if recharge_match else '')
                    
                    if uses > 0:
                        boxes = ''.join(['<span class="prof-indicator"></span>'] * uses)
                        recharge_text = f'{recharge} Rest' if recharge else ''
                        actions_html.append(f'<div class="feature-item"><strong>{name}</strong><div class="uses-row"><span>{recharge_text}</span><span class="uses-boxes">{boxes}</span></div></div>')
                    else:
                        actions_html.append(f'<div class="feature-item"><strong>{name}</strong></div>')
    
    return ''.join(actions_html) if actions_html else '<div class="feature-item"><strong>Attack</strong></div>'

def extract_spell_slots(class_info, features_list):
    """Extract spell slot information for a specific class"""
    if not isinstance(class_info, dict):
        return "No spell slots available"
    
    character_level = class_info.get('level', 1)
    class_name = class_info.get('name', '')
    spell_slots = []
    
    # Look for spellSlotsPerLevel in features matching this class
    for feature in features_list:
        if isinstance(feature, dict) and 'spellSlotsPerLevel' in feature:
            feature_type = feature.get('type', '')
            # Match feature to class by checking if class name is in feature type
            if class_name.replace(' [2024]', '') in feature_type or class_name in feature_type:
                slots_per_level = feature.get('spellSlotsPerLevel', {})
                if str(character_level) in slots_per_level:
                    spell_slots = slots_per_level[str(character_level)]
                    break
    
    if not spell_slots:
        return "No spell slots available"
    
    slots_html = []
    for i, slots in enumerate(spell_slots, 1):
        if slots > 0:
            boxes = ''.join(['<span class="prof-indicator"></span>'] * slots)
            slots_html.append(f'<div class="spell-slot-row"><span class="slot-label">Level {i}:</span><span class="slot-boxes">{boxes}</span></div>')
    
    return ''.join(slots_html) if slots_html else "No spell slots available"

def fill_template(template_file, data, output_file):
    """Fill HTML template with JSON data"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_file}")
    except Exception as e:
        raise Exception(f"Error reading template file: {e}")
    
    template = Template(template_content)
    
    # Extract relevant data for template
    classes_info = []
    class_data = data.get('class', [])
    if isinstance(class_data, list):
        for cls in class_data:
            if isinstance(cls, dict):
                classes_info.append(f"{cls.get('name', 'Unknown')} {cls.get('level', 1)}")
    elif isinstance(class_data, dict):
        # Handle single class as dict instead of list
        classes_info.append(f"{class_data.get('name', 'Unknown')} {class_data.get('level', 1)}")
    
    # Build ability scores table - check both 'abilityScores' and 'attributes' fields
    abilities = data.get('abilityScores', data.get('attributes', {}))
    if not isinstance(abilities, dict):
        abilities = {}
    
    ability_stats = ""
    for ability in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
        score = abilities.get(ability, 10)
        # Ensure score is a number
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = 10
        
        modifier = (score - 10) // 2
        mod_str = f"+{modifier}" if modifier >= 0 else str(modifier)
        short_name = ability[:3].upper()
        ability_stats += f'<div class="stat"><label>{short_name}</label><div class="stat-value">{score}</div><div class="stat-mod">{mod_str}</div></div>'
    
    # Extract skill proficiencies
    proficiency_bonus = data.get('proficiencyBonus', 2)
    skills_html = []
    
    # Get skill proficiencies from top-level fields
    skill_proficiencies = {k: v for k, v in data.get('skillProficiencies', {}).items() if v}
    skill_expertise = {k: v for k, v in data.get('skillExpertise', {}).items() if v}
    
    # Build ability groups with skills
    skills_by_ability = {
        'Strength': ['Athletics'],
        'Dexterity': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
        'Intelligence': ['Arcana', 'History', 'Investigation', 'Nature', 'Religion'],
        'Wisdom': ['Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
        'Charisma': ['Deception', 'Intimidation', 'Performance', 'Persuasion']
    }
    
    ability_groups = []
    for ability in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
        ability_score = abilities.get(ability, 10)
        try:
            ability_score = int(ability_score)
        except (ValueError, TypeError):
            ability_score = 10
        
        ability_mod = (ability_score - 10) // 2
        mod_str = f"+{ability_mod}" if ability_mod >= 0 else str(ability_mod)
        short_name = ability[:3].upper()
        
        group_html = '<div class="ability-group">'
        group_html += '<div class="abilities-skills-layout">'
        group_html += f'<div class="stat"><label>{short_name}</label><div class="stat-value">{ability_score}</div><div class="stat-mod">{mod_str}</div></div>'
        group_html += '<div class="skills-box">'
        
        if ability in skills_by_ability:
            for skill in skills_by_ability[ability]:
                if skill in skill_expertise:
                    bonus = ability_mod + (proficiency_bonus * 2)
                    prof_indicator = '<span class="prof-indicator expertise">E</span>'
                elif skill in skill_proficiencies:
                    bonus = ability_mod + proficiency_bonus
                    prof_indicator = '<span class="prof-indicator proficient">P</span>'
                else:
                    bonus = ability_mod
                    prof_indicator = '<span class="prof-indicator"></span>'
                
                bonus_str = f"+{bonus}" if bonus >= 0 else str(bonus)
                group_html += f'<div class="skill-item"><span class="skill-name">{skill}</span>{prof_indicator}<span class="skill-bonus">{bonus_str}</span></div>'
        
        group_html += '</div></div></div>'
        ability_groups.append(group_html)
    
    abilities_skills_grouped = ''.join(ability_groups)
    
    # Parse notes - handle various note formats
    notes_text = "No notes available"
    notes_data = data.get('notes', [])
    if notes_data:
        parsed_notes = []
        if isinstance(notes_data, list):
            for note in notes_data:
                if isinstance(note, dict):
                    title = note.get('title', 'Note')
                    content = note.get('content', '')
                    # Parse content if it's JSON string
                    if isinstance(content, str) and content.startswith('[{"insert"'):
                        try:
                            import re
                            # Extract text from insert format
                            text = re.findall(r'"insert":"([^"]+)"', content)
                            content = ''.join(text).replace('\\n', '<br>')
                        except:
                            pass
                    else:
                        content = content.replace('\n', '<br>')
                    parsed_notes.append(f'<div class="feature-item"><strong>{title}</strong><div class="feature-text">{content}</div></div>')
                elif isinstance(note, str):
                    parsed_notes.append(f'<div class="feature-item"><div class="feature-text">{note.replace(chr(10), "<br>")}</div></div>')
        elif isinstance(notes_data, str):
            parsed_notes.append(f'<div class="feature-item"><div class="feature-text">{notes_data.replace(chr(10), "<br>")}</div></div>')
        
        notes_text = ''.join(parsed_notes) if parsed_notes else "No notes available"
    
    # Get additional character information with safe access
    background_data = data.get('background', {})
    background_name = background_data.get('name', 'Unknown') if isinstance(background_data, dict) else 'Unknown'
    
    alignment = data.get('alignment', 'Unknown')
    max_hp = data.get('maxHP', data.get('currentHP', 'Unknown'))
    armor_class = data.get('armorClass', 'Unknown')
    
    # Calculate derived stats
    dex_score = abilities.get('Dexterity', 10)
    try:
        dex_score = int(dex_score)
    except (ValueError, TypeError):
        dex_score = 10
    dex_mod = (dex_score - 10) // 2
    initiative = f"+{dex_mod}" if dex_mod >= 0 else str(dex_mod)
    
    wis_score = abilities.get('Wisdom', 10)
    try:
        wis_score = int(wis_score)
    except (ValueError, TypeError):
        wis_score = 10
    wis_mod = (wis_score - 10) // 2
    
    # Check if proficient in Perception
    perception_bonus = wis_mod
    if 'Perception' in skill_proficiencies:
        perception_bonus += proficiency_bonus
    if 'Perception' in skill_expertise:
        perception_bonus += proficiency_bonus
    passive_perception = 10 + perception_bonus
    
    # Hit dice - create vertical list
    hit_dice_html = []
    for class_info in data.get('class', []):
        if isinstance(class_info, dict):
            level = class_info.get('level', 1)
            die = class_info.get('hitPointDie', 'd10')
            # Die format is already like '1d10', just use level and die type
            if die.startswith('1d'):
                die_type = die[1:]  # Remove the '1' to get 'd10'
                die_str = f"{level}{die_type}"
            else:
                die_str = f"{level}{die}"
            hit_dice_html.append(die_str)
    hit_dice_str = ', '.join(hit_dice_html) if hit_dice_html else '1d10'
    
    # Languages and proficiencies
    languages = ', '.join(data.get('languages', [])) if data.get('languages') else 'Common'
    
    # Collect all proficiencies
    prof_list = []
    if data.get('weaponProficiencies'):
        prof_list.extend(data.get('weaponProficiencies'))
    
    # Get armor training from classes
    armor_profs = set()
    for class_info in data.get('class', []):
        if isinstance(class_info, dict) and class_info.get('armorTraining'):
            armor_profs.update([a.strip() for a in class_info.get('armorTraining').split(',')])
    if armor_profs:
        prof_list.extend(sorted(armor_profs))
    
    if data.get('toolProficiencies'):
        prof_list.extend(data.get('toolProficiencies'))
    
    proficiencies = ', '.join(prof_list) if prof_list else 'None'
    
    # Get species information safely
    species_data = data.get('species', {})
    if not isinstance(species_data, dict):
        species_data = {}
    
    species_name = species_data.get('name', 'Unknown')
    species_description = species_data.get('description', '')
    size = species_data.get('size', 'Medium')
    speed = species_data.get('speed', data.get('speed', '30 ft.'))
    
    # Extract species features (traits)
    species_features = extract_features(species_data.get('traits', []))
    
    # Extract class features from featuresAndTraits
    class_features = extract_features(data.get('featuresAndTraits', []))
    
    # Extract feats
    feats = extract_features(data.get('feats', []))
    
    # Collect all spellcasting classes and generate sections
    features_list = data.get('featuresAndTraits', [])
    all_spells = data.get('spells', [])
    spellcasting_sections = ''
    spells_sections = ''
    
    for class_info in data.get('class', []):
        if isinstance(class_info, dict) and class_info.get('spellAbility'):
            class_name = class_info.get('name', 'Unknown')
            
            # Extract spell slots for this specific class
            spell_slots = extract_spell_slots(class_info, features_list)
            
            # Only create section if class actually has spell slots
            if spell_slots != "No spell slots available":
                spell_ability = class_info.get('spellAbility')
                spell_score = abilities.get(spell_ability, 10)
                try:
                    spell_score = int(spell_score)
                except (ValueError, TypeError):
                    spell_score = 10
                spell_mod = (spell_score - 10) // 2
                spell_attack = proficiency_bonus + spell_mod
                spell_dc = 8 + proficiency_bonus + spell_mod
                spell_attack_str = f"+{spell_attack}" if spell_attack >= 0 else str(spell_attack)
                
                spellcasting_sections += f'''
            <div class="section">
                <h2>{class_name} Spellcasting</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="label">Spell Attack</div>
                        <div class="value">{spell_attack_str}</div>
                    </div>
                    <div class="info-card">
                        <div class="label">Spell Save DC</div>
                        <div class="value">{spell_dc}</div>
                    </div>
                    <div class="info-card">
                        <div class="label">Ability</div>
                        <div class="value">{spell_ability}</div>
                    </div>
                </div>
                <div class="content-box">{spell_slots}</div>
            </div>
            '''
    
    # Single unified spell list with all spells
    if all_spells:
        spells_short, _ = extract_spells(all_spells)
        spells_sections = f'''
            <div class="section">
                <h2>Spells</h2>
                <div class="content-box">{spells_short}</div>
            </div>
            '''
    
    # Single spell details section for all spells
    _, all_spells_detailed = extract_spells(all_spells)
    spell_details_sections = f'''
        <div class="section">
            <h2>Spell Details</h2>
            <div class="content-box">{all_spells_detailed}</div>
        </div>
        '''
    
    # Extract weapons and inventory
    equipment_data = data.get('equipment', [])
    weapons = extract_weapons(equipment_data, proficiency_bonus)
    inventory = extract_inventory(equipment_data)
    
    # Extract actions
    actions = extract_actions(data)
    
    # Extract bio information
    bio_parts = []
    if data.get('bio'):
        bio_content = data.get('bio').replace('\n', '<br>')
        bio_parts.append(f'<div class="feature-item"><strong>Bio</strong><div class="feature-text">{bio_content}</div></div>')
    if data.get('age'):
        bio_parts.append(f'<div class="feature-item"><strong>Age</strong><div class="feature-text">{data.get("age")}</div></div>')
    if data.get('height'):
        bio_parts.append(f'<div class="feature-item"><strong>Height</strong><div class="feature-text">{data.get("height")}</div></div>')
    if data.get('weight'):
        bio_parts.append(f'<div class="feature-item"><strong>Weight</strong><div class="feature-text">{data.get("weight")}</div></div>')
    if data.get('eyes'):
        bio_parts.append(f'<div class="feature-item"><strong>Eyes</strong><div class="feature-text">{data.get("eyes")}</div></div>')
    if data.get('hair'):
        bio_parts.append(f'<div class="feature-item"><strong>Hair</strong><div class="feature-text">{data.get("hair")}</div></div>')
    if data.get('skin'):
        bio_parts.append(f'<div class="feature-item"><strong>Skin</strong><div class="feature-text">{data.get("skin")}</div></div>')
    
    bio = ''.join(bio_parts) if bio_parts else "No bio information available"
    
    template_data = {
        'character_name': data.get('name', 'Unknown'),
        'species_name': species_name,
        'species_description': species_description,
        'size': size,
        'speed': speed,
        'classes': ' / '.join(classes_info) if classes_info else 'Unknown',
        'background': background_name,
        'alignment': alignment,
        'max_hp': max_hp,
        'armor_class': armor_class,
        'species_features': species_features,
        'class_features': class_features,
        'feats': feats,
        'spellcasting_sections': spellcasting_sections,
        'spells_sections': spells_sections,
        'spell_details_sections': spell_details_sections,
        'actions': actions,
        'weapons': weapons,
        'inventory': inventory,
        'bio': bio,
        'notes': notes_text,
        'abilities_skills_grouped': abilities_skills_grouped,
        'proficiency_bonus': f'+{proficiency_bonus}',
        'initiative': initiative,
        'passive_perception': passive_perception,
        'hit_dice': hit_dice_str,
        'languages': languages,
        'proficiencies': proficiencies
    }
    
    try:
        filled_content = template.safe_substitute(template_data)
    except Exception as e:
        raise Exception(f"Error filling template: {e}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(filled_content)
    except Exception as e:
        raise Exception(f"Error writing output file: {e}")

def main():
    """Main function with command line argument support"""
    import sys
    import os
    
    # Default files
    json_file = None
    template_file = "character_template.html"
    output_file = None
    
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print("""
Character Sheet Generator - Usage

USAGE:
    python generate_character_sheet.py <json_file> [output_file] [template_file]

ARGUMENTS:
    <json_file>         (Required) Path to the character JSON file
    [output_file]       (Optional) Output HTML file (default: <json_file>.html)
    [template_file]     (Optional) Template file (default: character_template.html)

EXAMPLES:
    python generate_character_sheet.py my_character.json
    python generate_character_sheet.py my_character.json my_sheet.html
    python generate_character_sheet.py my_character.json my_sheet.html custom_template.html

HELP:
    python generate_character_sheet.py --help
        """)
        return 0
    
    # Check for required JSON file argument
    if len(sys.argv) < 2:
        print("Error: Missing required argument <json_file>")
        print("Usage: python generate_character_sheet.py <json_file> [output_file] [template_file]")
        print("Use --help for more information")
        return 1
    
    json_file = sys.argv[1]
    
    # Generate output filename from input JSON if not provided
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Replace .json extension with .html
        output_file = os.path.splitext(json_file)[0] + '.html'
    
    if len(sys.argv) > 3:
        template_file = sys.argv[3]
    
    # Validate files exist
    if not os.path.exists(json_file):
        print(f"Error: JSON file not found: {json_file}")
        return 1
    
    if not os.path.exists(template_file):
        print(f"Error: Template file not found: {template_file}")
        return 1
    
    try:
        print(f"Loading character data from: {json_file}")
        data = load_json_data(json_file)
        
        print(f"Generating character sheet using template: {template_file}")
        fill_template(template_file, data, output_file)
        
        print(f"Character sheet generated successfully: {output_file}")
        return 0
        
    except Exception as e:
        print(f"Error generating character sheet: {e}")
        return 1

if __name__ == "__main__":
    exit(main())