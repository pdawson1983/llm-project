import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.ai_schemas import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.call_function import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def main():
    load_dotenv()
    args = sys.argv[1:]

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("LLM Assistant")
        print('Usage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I print in python?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    
    generate_content(client, messages, verbose)




def generate_content(client, messages, verbose):
    count = 20
    while count >= 0:
        count -= 1
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],system_instruction=system_prompt),
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        messages.append(response.candidates[0].content)
        
        function_call = response.function_calls

        if function_call:
            for function_call_part in function_call:
                try:
                    function_call_result = call_function(function_call_part, verbose=True)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("fatal exception with function call")
                    elif verbose:
                        result_data = function_call_result.parts[0].function_response.response
                        if isinstance(result_data, dict) and 'result' in result_data:
                            print(f"-> {result_data['result']}")
                        else:
                            print(f"-> {result_data}")
                    messages.append(function_call_result)
                except Exception as e:
                    print(f"Error: {e}")
                    error_response = types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"error": str(e)},
                            )
                        ],
                    )
                    messages.append(error_response)
            continue
        else:
            print("Response:")
            print(response.text)
            break
        
        if count < 0:
            print("Maximum iterations reached")
        


if __name__ == "__main__":
    main()
