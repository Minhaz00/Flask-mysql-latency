# app.py
from flask import Flask, jsonify
import mysql.connector
import time
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/')
def query_latency():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Start timing
        start_time = time.time()

        # Execute the query
        cursor.execute("SELECT * FROM users")

        # Fetch the results (optional, depending on what you want to measure)
        results = cursor.fetchall()

        # End timing
        end_time = time.time()

        # Calculate latency
        latency = end_time - start_time

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({
            'latency': latency,
            'results': results  # You can remove this if you don't want to return the results
        })

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)
