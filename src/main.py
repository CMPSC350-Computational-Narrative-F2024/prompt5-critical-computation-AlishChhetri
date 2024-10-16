# Code to generate "text"

#!/usr/bin/python

import os
import openai
from dotenv import dotenv_values

# Set up OpenAI credentials

CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG


def load_file(filename: str = "") -> str:
    """Loads an arbitrary file name"""
    with open(filename, "r") as fh:
        return fh.read()


def main():
    # Load source file
    source_text = load_file("data/the_yellow_wallpaper.txt")

    # Create a chain of thought prompt to guide GPT through the analysis
    messages = [
        {"role": "system", "content": "You are a critical text analyst."},
        {
            "role": "user",
            "content": (
                "Read the following text and provide a chain of thought analysis. "
                "Summarize each paragraph, highlighting the underlying themes, emotions, or stylistic nuances, and then provide an overall summary of the text. "
                "Explain each part of your reasoning step by step.\n\n"
                f"Text: {source_text}\n\n"
                "Chain of Thought and paragraph-by-paragraph Summary:"
            ),
        },
    ]

    # Get the response from GPT
    response = openai.chat.completions.create(
        model="gpt-4o", messages=messages, max_tokens=500, temperature=0.7
    )

    # Extract and print the response
    analysis = response.choices[0].message.content
    print("Chain of Thought Analysis:\n", analysis)

    # Save the output to text.md
    with open("../writing/text.md", "w") as f:
        f.write("# Chain of Thought Analysis\n\n")
        f.write(analysis)


if __name__ == "__main__":
    main()
