import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ✅ CORS enabled
# Upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database path (CHANGE HERE)
DB_PATH = os.path.join(os.getcwd(), 'database.db')

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            upload_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized")

# Function to save image data to database
def save_to_db(image_name, upload_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO images (image_name, upload_time) VALUES (?, ?)', (image_name, upload_time))
    conn.commit()
    conn.close()
    print("✅ Image info saved to DB")

# Route to test backend
@app.route('/')
def home():
    return "✅ Flask backend working..."

# Route to handle image upload
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image_file' not in request.files:
        return jsonify({'error': 'No image_file part'}), 400

    image = request.files['image_file']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    

    # Save image with timestamp
    image_name = f"{int(datetime.now().timestamp())}_{image.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, image_name)
    image.save(image_path)

    # Save info to database
    upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_to_db(image_name, upload_time)

    return jsonify({'message': 'Image uploaded and saved successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
