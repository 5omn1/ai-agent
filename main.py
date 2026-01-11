import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

MAX_ITERATIONS = 20


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found.")

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    # Conversation state starts with the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    last_usage = None  # keep last usage metadata for verbose printing

    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        # Track usage for verbose mode
        last_usage = getattr(response, "usage_metadata", None)

        # Append the model's message (use top candidate)
        if response.candidates and response.candidates[0].content:
            messages.append(response.candidates[0].content)

        # If the model is done (no tool calls), print and exit
        if not getattr(response, "function_calls", None):
            if args.verbose and last_usage:
                print(f"Prompt tokens: {last_usage.prompt_token_count}")
                print(f"Response tokens: {last_usage.candidates_token_count}")

            print(response.text)
            return

        # Otherwise execute tool calls and collect their results
        function_results_parts = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("Error: function returned an empty parts list")

            part0 = function_call_result.parts[0]
            if part0.function_response is None:
                raise Exception("Error: Expected FunctionResponse, got None")

            if part0.function_response.response is None:
                raise Exception("Error: FunctionResponse.response is None")

            function_results_parts.append(part0)

            if args.verbose:
                print(f"-> {part0.function_response.response}")

        # Feed ALL tool results back to the model as one user turn
        messages.append(types.Content(role="user", parts=function_results_parts))

    # Only reached if the loop never returned
    print(
        "Error: maximum number of iterations reached. "
        "The model did not produce a final response."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
