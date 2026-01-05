import os
import argparse

from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found.")

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_promt", type=str, help="User promt")
    args = parser.parse_args()
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=args.user_promt
    )
    if not response.usage_metadata:
        raise RuntimeError(
            "Error occured during the request to Gemini API for content generation."
        )

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
