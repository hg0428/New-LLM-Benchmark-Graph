# Model Benchmark Visualization Tool

This tool allows you to visualize and compare different language models across various benchmarks and parameters.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Adding New Models

To add a new model, create a JSON file in the `models` directory with the following structure:

```json
{
    "model_name": "Model Name",
    "model_family": "family_name",
    "architecture": "transformer",
    "parameters": {
        "total_params": 1000000000,
        "embedding_size": 4096,
        "layers": 32,
        "attention_heads": 32,
        "vocab_size": 32000
    },
    "benchmarks": {
        "mmlu": 50.0,
        "HellaSwag": 80.0,
        "arc_challenge": 45.0,
        "TruthfulQA": 40.0
    }
}
```

## Features

- Interactive visualization of model performance
- Compare models across different families
- Customizable X and Y axes
- Logarithmic scale for parameter values
- Hover tooltips with model details
- Automatic color coding by model family
