import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found.")

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config = types.GenerateContentConfig(tools=[available_functions],
                                             system_instruction=system_prompt,
                                             temperature=0,
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError(
            "Error occured during the request to Gemini API for content generation."
        )

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print("Response:")
        print(response.text)

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)

        if not function_call_result.parts:
            raise Exception(f"Error: 'function_call' function return an empty list")

        if function_call_result.parts[0].function_response == None:
            raise Exception(f"Error: Instead of 'FunctionResponse' object we have None")

        if function_call_result.parts[0].function_response.response == None:
            raise Exeception(f"Error: 'FunctionResponse.response' is None")

        function_result = []
        function_result.append(function_call_result.parts[0])

        if args.verbose == True:
            print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
