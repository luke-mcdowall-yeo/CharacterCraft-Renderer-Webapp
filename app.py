from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import json
import logging
from pathlib import Path
from generate_character_sheet import fill_template, load_json_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("Upload request received")
        
        if 'file' not in request.files:
            logger.warning("No file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        logger.info(f"File received: {file.filename}")
        
        if file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'File must be a JSON file'}), 400
        
        json_path = os.path.join(UPLOAD_FOLDER, file.filename)
        logger.info(f"Saving file to: {json_path}")
        file.save(json_path)
        
        logger.info("Loading JSON data")
        data = load_json_data(json_path)
        character_name = data.get('name', 'character')
        logger.info(f"Character name: {character_name}")
        
        safe_name = secure_filename(character_name) if character_name else 'character'
        
        output_filename = f"{safe_name}_sheet.html"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        logger.info(f"Generating character sheet: {output_path}")
        fill_template('character_template.html', data, output_path)
        
        logger.info(f"Successfully generated: {output_filename}")
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'character_name': character_name
        })
    
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        logger.info(f"Download request for: {filename}")
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            logger.warning(f"Path traversal attempt: {filename}")
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>')
def view_file(filename):
    try:
        logger.info(f"View request for: {filename}")
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        real_path = os.path.realpath(file_path)
        output_dir = os.path.realpath(OUTPUT_FOLDER)
        
        if not real_path.startswith(output_dir):
            logger.warning(f"Path traversal attempt: {filename}")
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(OUTPUT_FOLDER, safe_filename)
    except Exception as e:
        logger.error(f"Error in view_file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
