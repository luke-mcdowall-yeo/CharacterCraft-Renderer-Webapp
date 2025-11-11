from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import json
import traceback
from pathlib import Path
from generate_character_sheet import fill_template, load_json_data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Upload request received")  # Debug logging
        
        if 'file' not in request.files:
            print("No file in request")
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Empty filename")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            print("Not a JSON file")
            return jsonify({'success': False, 'error': 'File must be a JSON file'}), 400
        
        # Save uploaded file
        json_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        print(f"Saving to: {json_path}")
        file.save(json_path)
        
        # Load and validate JSON
        print("Loading JSON data...")
        data = load_json_data(json_path)
        
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400
        
        character_name = data.get('name', 'character')
        print(f"Character name: {character_name}")
        
        safe_name = secure_filename(character_name) if character_name else 'character'
        output_filename = f"{safe_name}_sheet.html"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Generate character sheet
        print(f"Generating sheet: {output_path}")
        fill_template('character_template.html', data, output_path)
        
        # Verify output was created
        if not os.path.exists(output_path):
            return jsonify({'success': False, 'error': 'Failed to generate character sheet'}), 500
        
        print(f"Success! Generated: {output_filename}")
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'character_name': character_name
        }), 200
    
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format: {str(e)}"
        print(f"JSON Error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 400
    
    except FileNotFoundError as e:
        error_msg = f"Template file not found: {str(e)}"
        print(f"File Error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 500
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Error: {error_msg}")
        print(traceback.format_exc())  # Full stack trace
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename, as_attachment=True)
    except Exception as e:
        print(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>')
def view_file(filename):
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename)
    except Exception as e:
        print(f"View error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Health check endpoint for debugging
@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'upload_folder': os.path.exists(UPLOAD_FOLDER),
        'output_folder': os.path.exists(OUTPUT_FOLDER)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)        safe_name = secure_filename(character_name) if character_name else 'character'
        
        output_filename = f"{safe_name}_sheet.html"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        fill_template('character_template.html', data, output_path)
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'character_name': character_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>')
def view_file(filename):
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
