from flask import Flask, render_template, request, Response, jsonify, current_app
import time
import os
import json

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
with app.app_context():
    current_app.currently = None

@app.route('/')
def index():
    print(os.getcwd())
    return render_template('index.html')

@app.route("/stream")
def stream():
    def eventStream():
        while True:
            # Poll data from the database
            # and see if there's a new message
            with app.app_context():
                if current_app.currently:
                    for i in range(3):
                        time.sleep(i)
                        yield "data: {}\n\n".format(str(i) + current_app.currently)
                    current_app.currently = None
    
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/process-request', methods=['POST'])
def process_request():
    data = request.json.get('data')
    process_request_task(data)
    with app.app_context():
        current_app.currently = data
    
    return jsonify({'message': 'Data received', 'item': 1}), 201
        

# Function to simulate a long-running task
def process_request_task(data):
    # Simulate long-running task
    print(f"Processing request with data: {data}")
    time.sleep(1)  # Simulate some processing time

if __name__ == '__main__':
    app.run(debug=True)
