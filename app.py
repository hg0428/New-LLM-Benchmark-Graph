from flask import Flask, render_template, jsonify
import json
import os
import pandas as pd
import re
import glob

app = Flask(__name__)


def load_model_data():
    models_data = []
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    for filename in os.listdir(models_dir):
        if filename.endswith(".json"):
            with open(os.path.join(models_dir, filename), "r") as f:
                model_data = json.load(f)
                # Calculate average of all benchmarks
                if 'benchmarks' in model_data:
                    benchmark_values = [v for v in model_data['benchmarks'].values() if v is not None]
                    if benchmark_values:
                        model_data['benchmarks']['Average'] = sum(benchmark_values) / len(benchmark_values)
                models_data.append(model_data)
    return models_data


def get_available_metrics():
    models = load_model_data()
    parameters = set()
    benchmarks = set()
    
    for model in models:
        if "parameters" in model:
            parameters.update(model["parameters"].keys())
        if "benchmarks" in model:
            benchmarks.update(model["benchmarks"].keys())
    
    return {
        "parameters": sorted(list(parameters)),
        "benchmarks": sorted(list(benchmarks), key=lambda x: (x != 'Average', x))
    }


def normalize_key(key):
    """Normalize a key by removing spaces, dashes, underscores and converting to lowercase."""
    return re.sub(r'[-_\s]+', '', key.lower())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/models")
def get_models():
    models = []
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    for filename in os.listdir(models_dir):
        if filename.endswith(".json"):
            with open(os.path.join(models_dir, filename)) as f:
                model_data = json.load(f)
                # Calculate average of all benchmarks
                if 'benchmarks' in model_data:
                    benchmark_values = [float(v) for v in model_data['benchmarks'].values() if v is not None and str(v).replace('.', '').isdigit()]
                    if benchmark_values:
                        model_data['benchmarks']['Average'] = round(sum(benchmark_values) / len(benchmark_values), 2)
                models.append(model_data)
    return jsonify(models)


@app.route('/api/metrics')
def metrics():
    return jsonify(get_available_metrics())


if __name__ == "__main__":
    app.run(debug=True, port=2001)
