# Student Services Bot — AI Evaluation Framework

## Overview
This project implements an AI evaluation framework for a Student Services Bot that helps students with:
1. Password reset
2. Course registration

## Setup

### 1. Install Dependencies
```bash
python3 -m pip install google-genai
```

### 2. Configure API Key
Create a `.env` file or export directly:
```bash
export GENAI_API_KEY="your_api_key_here"
```

## Running the Agent

Test the bot interactively:
```bash
export GENAI_API_KEY="your_api_key_here"
python3 chat.py
```

Save transcripts while testing:
```bash
export GENAI_API_KEY="your_api_key_here"
export TRANSCRIPT_PATH="data/transcripts/my_transcript.txt"
python3 chat.py
```

## Running Evaluations

Execute the evaluation framework:
```bash
export GENAI_API_KEY="your_api_key_here"
python3 evals/run_evals.py
```

### Results
- `results/results.jsonl` — detailed evaluation results (JSON Lines format)
- `results/results.csv` — summary table (PASS/FAIL for correctness and politeness)

## Project Structure
```
tsis3/
├── chat.py                          # Agent entry point
├── evals/
│   └── run_evals.py                # Evaluation runner
├── data/
│   └── synthetic_dataset.jsonl      # Test dataset (8 conversations)
├── results/                         # Output folder (auto-generated)
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Evaluation Framework

### JTBD (Jobs To Be Done)
1. **Reset Password** — Students should be able to reset passwords without calling support
2. **Course Registration** — Students should register for courses independently

### Evals
- **Correctness** — Does the response contain expected keywords?
- **Politeness** — Is the response free of inappropriate language?

## Next Steps
1. Run: `python3 evals/run_evals.py`
2. Check results in `results/results.csv`
3. Create PDF report with evaluation results