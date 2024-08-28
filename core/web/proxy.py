import os
from flask import Flask, request, jsonify
from threading import Thread
import requests

app = Flask(__name__)
registered_plugins = {}


@app.route('/register', methods=['POST'])
def register_plugin():
    data = request.get_json()
    plugin_name = data.get('name')
    plugin_base_url = data.get('base_url')

    if plugin_name and plugin_base_url:
        registered_plugins[plugin_name] = plugin_base_url
        return jsonify({'status': 'success', 'message': f'Plugin {plugin_name} registered successfully.'}), 200
    return jsonify({'status': 'error', 'message': 'Invalid plugin data.'}), 400


@app.route('/plugins/<plugin_name>/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_to_plugin(plugin_name, endpoint):
    base_url = registered_plugins.get(plugin_name)

    if not base_url:
        return jsonify({'status': 'error', 'message': f'Plugin {plugin_name} not found.'}), 404

    method = request.method
    url = f"{base_url}/{endpoint}"

    try:
        # Forward the request to the appropriate plugin
        if method == 'GET':
            response = requests.get(url, params=request.args)
        elif method == 'POST':
            response = requests.post(url, json=request.get_json())
        elif method == 'PUT':
            response = requests.put(url, json=request.get_json())
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            return jsonify({'status': 'error', 'message': 'Method not allowed.'}), 405

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Error forwarding request to plugin: {e}'}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions."""
    return jsonify({'status': 'error', 'message': str(e)}), 500


def run_proxy(port):
    app.run(host='0.0.0.0', port=port)


def start_proxy_service(port=8000):
    thread = Thread(target=run_proxy, args=(port,))
    thread.daemon = True
    thread.start()
