# Handbook QA Bot

## Overview
The PDF Bot is an AI-based tool designed to answer questions based on a provided handbook (PDF). It uses a language model to extract relevant information and provide (almost) accurate answers.

## Installation

1. Clone the repository:

    git clone https://github.com/your-repo/handbook-qa-bot.git
    cd handbook-qa-bot


2. Create a virtual environment and install dependencies:

    ```python -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt```

3. Place the handbook PDF in the `data/` directory.

## Usage

1. Define your questions in the `inputs` list in `main.py`.
2. Run the main script:
    python src/main.py
3. The answers will be saved in `output/response.json`.

## Configuration

- The language model and other settings can be configured in `utils.py`.
- Use the `.env` file to store sensitive information like API keys.

## Testing

Run tests using:
    pytest tests/


## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.


