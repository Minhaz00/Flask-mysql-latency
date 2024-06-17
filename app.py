from flask import Flask
import mysql.connector
import time
from prometheus_client import start_http_server, Summary
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Create a metric to track time spent and requests made
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNTER = Counter('request_processing_count', 'Number of requests processed')

@app.route('/metrics')
def metrics():
    return generate_latest()

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='my_db'
    )
    return connection

@REQUEST_TIME.time()
@app.route('/')
def query():
    start_time = time.time()
    REQUEST_COUNTER.inc()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    end_time = time.time()
    latency = end_time - start_time
    REQUEST_TIME.observe(latency)
    return f"Query latency: {latency} seconds. Result: {result}"

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Run the Flask app
    app.run(port=5000)