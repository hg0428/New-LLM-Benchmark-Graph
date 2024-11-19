from flask import Flask, render_template, jsonify
import json
import os
import pandas as pd
import re

app = Flask(__name__)


def load_model_data():
    models_data = []
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    for filename in os.listdir(models_dir):
        if filename.endswith(".json"):
            with open(os.path.join(models_dir, filename), "r") as f:
                model_data = json.load(f)
                models_data.append(model_data)
    return models_data


def get_available_metrics():
    models_data = load_model_data()
    if not models_data:
        return {"parameters": [], "benchmarks": []}
    
    # Get all unique parameter and benchmark keys
    parameters = set()
    benchmarks = set()
    
    for model in models_data:
        if "parameters" in model:
            parameters.update(model["parameters"].keys())
        if "benchmarks" in model:
            benchmarks.update(model["benchmarks"].keys())
    
    return {
        "parameters": sorted(list(parameters)),
        "benchmarks": sorted(list(benchmarks))
    }


def normalize_key(key):
    """Normalize a key by removing spaces, dashes, underscores and converting to lowercase."""
    return re.sub(r'[-_\s]+', '', key.lower())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/models")
def get_models():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    models = []
    for filename in os.listdir(models_dir):
        if filename.endswith('.json'):
            with open(os.path.join(models_dir, filename)) as f:
                model_data = json.load(f)
                
                # Normalize benchmark keys while preserving original display names
                if 'benchmarks' in model_data:
                    normalized_benchmarks = {}
                    for key, value in model_data['benchmarks'].items():
                        normalized_key = normalize_key(key)
                        # Use the first encountered version of the benchmark name as display name
                        if normalized_key not in normalized_benchmarks:
                            normalized_benchmarks[key] = value
                        else:
                            # If we find a duplicate (normalized) key, keep the value but don't add a new key
                            continue
                    model_data['benchmarks'] = normalized_benchmarks
                
                models.append(model_data)
    return jsonify(models)


@app.route('/api/metrics')
def get_available_metrics():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    parameters = set()
    benchmarks = {}  # Use dict to store normalized key -> display name mapping
    
    for filename in os.listdir(models_dir):
        if filename.endswith('.json'):
            with open(os.path.join(models_dir, filename)) as f:
                model_data = json.load(f)
                if 'parameters' in model_data:
                    parameters.update(model_data['parameters'].keys())
                if 'benchmarks' in model_data:
                    for benchmark in model_data['benchmarks'].keys():
                        normalized_key = normalize_key(benchmark)
                        # Store the first encountered version as the display name
                        if normalized_key not in benchmarks:
                            benchmarks[normalized_key] = benchmark
    
    return jsonify({
        'parameters': sorted(list(parameters)),
        'benchmarks': sorted(list(benchmarks.values()))  # Return display names
    })


if __name__ == "__main__":
    app.run(debug=True, port=2001)
