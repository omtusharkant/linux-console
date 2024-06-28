from flask import Flask, jsonify
from flask_cors import CORS
from sys_info import ResourceUsage

app = Flask(__name__)
CORS(app)

# Dummy data for resource values

@app.route('/api/greet', methods=['GET'])
def greet():
    return jsonify(message='Hello from Flask!')


# Create an instance of ResourceUsage
resource_usage = ResourceUsage()

# Define new routes for system information
@app.route('/api/system/cpu', methods=['GET'])
def get_cpu_info():
    return jsonify(resource_usage.cpu_info())

@app.route('/api/system/ram', methods=['GET'])
def get_ram_info():
    return jsonify(resource_usage.ram_info())

@app.route('/api/system/disk', methods=['GET'])
def get_disk_info():
    return jsonify(resource_usage.disk_info())

@app.route('/api/system/packet_sent', methods=['GET'])
def get_packet_up():
    return jsonify(resource_usage.get_packets_sent())

@app.route('/api/system/packet_recv', methods=['GET'])
def get_packet_down():
    return jsonify(resource_usage.get_packets_recv())

if __name__ == '__main__':
    app.run(debug=True)
