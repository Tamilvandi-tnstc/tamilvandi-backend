from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your MySQL password
    database="tamilvandi"
)

@app.route('/api/travel')
def get_travel_data():
    origin = request.args.get('from', '')
    destination = request.args.get('to', '')

    print(f"Received search request: From={origin}, To={destination}")  # Debugging print

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM travel_info WHERE origin LIKE %s AND destination LIKE %s"
    cursor.execute(query, (f"%{origin}%", f"%{destination}%"))
    
    results = cursor.fetchall()
    cursor.close()
    db.close()  # Close the connection after each request

    print(f"Database results: {results}")  # Debugging print
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
