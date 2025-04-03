from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# ✅ Secure database connection using environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "your-database-host"),
        user=os.getenv("DB_USER", "your-database-username"),
        password=os.getenv("DB_PASSWORD", "your-database-password"),
        database=os.getenv("DB_NAME", "tamilvandi")
    )

# ✅ Health Check Route (Prevents 404 on Render)
@app.route('/')
def home():
    return "TamilVandi API is running!", 200

# ✅ Main API Route for Travel Search
@app.route('/api/travel', methods=['GET'])
def get_travel_data():
    origin = request.args.get('from', '')
    destination = request.args.get('to', '')

    print(f"Received search request: From={origin}, To={destination}")  # Debugging log

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM travel_info WHERE origin LIKE %s AND destination LIKE %s"
    cursor.execute(query, (f"%{origin}%", f"%{destination}%"))

    results = cursor.fetchall()
    cursor.close()
    db.close()  # Always close the connection

    print(f"Database results: {results}")  # Debugging log
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))  # ✅ Render assigns a port dynamically
