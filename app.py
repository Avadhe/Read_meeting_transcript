from flask import Flask, request, jsonify, send_from_directory
from docx import Document
import os

app = Flask(__name__)

def get_docx_content(file_path):
    # Load the .docx file
    doc = Document(file_path)
    # Read paragraphs into a string
    content = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    return content

@app.route('/process-file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.docx'):
        return jsonify({'error': 'Invalid file type'}), 400

    # Save the file temporarily
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    try:
        # Process the file
        content = get_docx_content(file_path)

        # Save the content into a text file
        text_file_path = os.path.splitext(file_path)[0] + '.txt'
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(content)



        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # finally:
    #     # Clean up the temporary file
    #     os.remove(file_path)

@app.route('/')
def serve_html():
    # Serve the HTML file
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
