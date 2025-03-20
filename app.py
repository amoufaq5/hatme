# app.py
import os
import logging
from flask import Flask, request, render_template, jsonify
from models.diagnosis import diagnose_patient, diagnose_image
from scraping.scraper import start_scraping
from database import init_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQL database (for demonstration, using SQLite)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if request.method == 'POST':
        # Collect all form data (which includes fields from mnemonics like WWHAM, ASMETHOD, etc.)
        data = request.form.to_dict()
        # Process data via text-based diagnosis
        diagnosis_result = diagnose_patient(data)
        return jsonify({'result': diagnosis_result})
    else:
        return render_template('diagnosis_form.html')

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filepath)
        diagnosis_result = diagnose_image(filepath)
        return jsonify({'result': diagnosis_result})
    else:
        return render_template('upload_image.html')

@app.route('/start-scraping')
def scrape():
    try:
        start_scraping()
        return jsonify({'status': 'Scraping started'})
    except Exception as e:
        logging.exception("Error during scraping")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
