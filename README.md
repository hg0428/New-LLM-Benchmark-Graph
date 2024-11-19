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

3. Open your browser and navigate to `http://localhost:2001`

## TODO Models to Add:
- MobileLLM
- Gemma2
- Phi3.5
- Mistral models
- Zamba2
- Others

## Other TODO:
- Add a # of training tokens field to every model.

## Disclaimer:
I did not take into account whether the model used CoT on the benchmarks. Some did some didn't. It's just about impossible to find benchmarks that match up perfectly. Some were 5-shot while others were 1-shot or 0-shot. The benchmarks are not fair, but they can at least give us a rough idea for now. 