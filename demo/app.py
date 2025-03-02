from flask import Flask, request, jsonify, send_file
import os
import subprocess
import uuid
import tempfile
import time
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'mp3'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process', methods=['POST'])
def process_audio():
    # Check if file part exists in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if user selected a file
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only MP3 files are allowed'}), 400
    
    try:
        # Generate a unique ID for this processing job
        job_id = str(uuid.uuid4())
        
        # Secure the filename and save the uploaded file
        filename = secure_filename(file.filename)
        base_name = os.path.splitext(filename)[0]
        mp3_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")
        file.save(mp3_path)
        
        # Create paths for intermediate and output files
        midi_path = os.path.join(PROCESSED_FOLDER, f"{job_id}_{base_name}.mid")
        text_path = os.path.join(PROCESSED_FOLDER, f"{job_id}_{base_name}.txt")
        
        # CHANGE here
        # Step 1: Convert MP3 to MIDI using command line tool
        # Replace 'mp3_to_midi_tool' with your actual tool command

        midi_process = subprocess.run(
            ["./run_basic_pitch.sh", midi_path, mp3_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Step 2: Process MIDI to text using command line tool
        # Replace 'midi_to_text_tool' with your actual tool command
        text_process = subprocess.run(
            ["./run_algo.sh",midi_path, text_path], 
            capture_output=True,
            text=True,
            check=True
        )
        
        # Read the generated text file
        with open(text_path, 'r') as f:
            text_content = f.read()
        
        # Return the job ID and initial text content
        return jsonify({
            'success': True,
            'job_id': job_id,
            'text_content': text_content,
            'filename': base_name
        })
        
    except subprocess.CalledProcessError as e:
        # Handle command line tool errors
        return jsonify({
            'error': f"Processing error: {e.stderr}",
            'step': 'conversion'
        }), 500
    except Exception as e:
        # Handle any other errors
        return jsonify({'error': f"Server error: {str(e)}"}), 500

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Endpoint to check processing status"""
    # This would be implemented if you need to track long-running processes
    # For now, we'll just return a simple response
    return jsonify({'status': 'completed'})

@app.route('/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id, filename):
    """Endpoint to download the processed text file"""
    base_name = os.path.splitext(secure_filename(filename))[0]
    text_path = os.path.join(PROCESSED_FOLDER, f"{job_id}_{base_name}.txt")
    
    if not os.path.exists(text_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(
        text_path,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"{base_name}.txt"
    )

@app.route('/cleanup/<job_id>', methods=['POST'])
def cleanup_files(job_id):
    """Endpoint to clean up temporary files after processing"""
    try:
        # Find all files with this job ID
        for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
            for filename in os.listdir(folder):
                if filename.startswith(job_id):
                    os.remove(os.path.join(folder, filename))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For development only - use a production WSGI server in production
    app.run(debug=True, host='0.0.0.0', port=5000)
