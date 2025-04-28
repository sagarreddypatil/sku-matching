# SKU Matching POC with OpenAI o4-mini-high

## Dependencies
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Instructions for use

Unzip the data folder to `data/`. It should look like this:
```sh
data/
├── emails
│   ├── 0050F2E0-8E13-4DB9-AC2E-6C2DDCA2D871.txt
│   ├── 00959BF5-2065-489E-90B8-4A1EAC56BFBA.txt
│   ├── 012F2C97-23FC-4405-B210-2A8EFAF8211A.txt
│   ├── ...
├── ground_truth_df.csv
└── product_df.csv
```

Run `uv sync` to create a venv and download dependencies. Then,

```sh
uv run give_problem.py
```

This picks a random email, writes the content to `email_input.txt` and the ground-truth label to `ground_truth.txt`.

Then, run
```sh
uv run main.py
```

To solve the problem in the txt files with OpenAI's o4-mini-high model.

**Before running `main.py`**, you need to add your OpenAI API key to an environment variable.
```sh
export OPENAI_API_KEY="<your-key-here>"
```