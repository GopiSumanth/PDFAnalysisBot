import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import get_agent


def handler():
    # Define inputs
    inputs = [
        "Who is the president of India?",
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?",
    ]

    # Load the agent
    agent = get_agent("data/handbook.pdf")

    # Process the questions
    response = {}
    for question in inputs:
        response[question] = agent.query(question)
        print(f"{question} : {response[question]}\n\n")

    # Save the responses to a JSON file
    with open("output/response.json", "w") as f:
        json.dump(response, f, indent=2)
    return response


if __name__ == "__main__":
    response = handler()
