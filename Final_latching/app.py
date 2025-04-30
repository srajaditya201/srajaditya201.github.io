from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
import subprocess
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    file = request.files['csv_file']
    if not file:
        return "No file uploaded.", 400

    filename = f"user_upload_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Run flipkart_script.py with the uploaded file
    command = ['python', 'final_cd.py', filepath]
    subprocess.run(command, check=True)

    # The script generates a report like: latching_YYYYMMDD_HHMMSS.csv
    latest_report = sorted(os.listdir(REPORT_FOLDER), reverse=True)[0]
    return render_template('index.html', report_file=latest_report)

@app.route('/reports/<path:filename>')
def download_file(filename):
    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
