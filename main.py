import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found.")

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_promt)])]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages
    )
    if not response.usage_metadata:
        raise RuntimeError(
            "Error occured during the request to Gemini API for content generation."
        )
    if args.verbose is True:
        print(f"User prompt: {args.user_promt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        print(response.text)
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
