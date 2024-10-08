# app.py (Flask backend)
from flask import Flask, jsonify, request, send_file
from models import db, Todo
from config import Config
import os
import csv
from io import StringIO
from google.cloud import storage
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

BUCKET_NAME = 'meri-bucket-meri-jaan'
EXPORT_FILE_NAME = 'todos_export.csv'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './gcp_creds.json'

# Function to upload CSV to GCS
def upload_to_gcs(bucket_name, blob_name, file_data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(file_data.getvalue(), content_type='text/csv')
    return f"gs://{bucket_name}/{blob_name}"

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = Todo(task=data['task'], done=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.json
    todo.task = data.get('task', todo.task)
    todo.done = data.get('done', todo.done)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()
    return '', 204

@app.route('/export-todos', methods=['GET'])
def export_todos():
    todos = Todo.query.all()

    # Create CSV in memory
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(['ID', 'Task', 'Done'])
    
    for todo in todos:
        writer.writerow([todo.id, todo.task, todo.done])
    
    # Upload CSV to GCS
    blob_name = EXPORT_FILE_NAME
    upload_to_gcs(BUCKET_NAME, blob_name, csv_file)
    url = generate_signed_url(BUCKET_NAME, EXPORT_FILE_NAME)

    # Optionally, return the file for download or return GCS link
    return jsonify({'message': 'CSV uploaded successfully', 'gcs_uri': url})


def generate_signed_url(bucket_name, blob_name, expiration=3600):
    """Generates a signed URL for the GCS blob."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate the signed URL
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=expiration),  # URL expires in 1 hour by default
        method="GET",
    )
    return url

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port=5000, host="0.0.0.0")
