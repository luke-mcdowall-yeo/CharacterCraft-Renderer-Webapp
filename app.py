from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import json
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
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'File must be a JSON file'}), 400
        
        json_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(json_path)
        
        data = load_json_data(json_path)
        character_name = data.get('name', 'character')
        safe_name = secure_filename(character_name) if character_name else 'character'
        
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
