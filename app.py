import os
import json
from flask import Flask, render_template, request, send_file
from generate_character_sheet import generate_sheet

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file provided", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        try:
            json_data = json.load(file)
            html_output = generate_sheet(json_data, 'character_template.html')
            
            output_filename = f"{os.path.splitext(file.filename)[0]}.html"
            with open(output_filename, 'w') as f:
                f.write(html_output)
            
            return send_file(output_filename, as_attachment=True, download_name=output_filename)
        except Exception as e:
            return f"Error processing file: {str(e)}", 500
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>D&D 5e Character Sheet Generator</title></head>
    <body>
        <h1>Character Sheet Generator</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".json" required>
            <button type="submit">Generate Sheet</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
