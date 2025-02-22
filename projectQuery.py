import os
import sys
import tiktoken  # OpenAI's tokenization library
import google.generativeai as genai  # Gemini API

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
def count_tokens(prompt):
    """Estimate the number of tokens in the prompt."""
    return len(prompt.split())

def call_gemini_api(prompt):
    """Call the Gemini API with the provided prompt and return the response."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key is not set.")
        return None
    
    # Count tokens in the prompt
    token_count = count_tokens(prompt)
    print(f"Number of tokens in the prompt: {token_count}")

    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response else None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None


def process_query(user_query):
    """Generate a structured prompt and get a response."""
    # Define file paths
    prompt_template_path = "/workspaces/CodeVision1/input/promptForChat.txt"
    class_content_path = "/workspaces/CodeVision1/output/ZIP/Extracted/GenAINumHandler/GenAINumHandler/enhanced_merged_output.txt"

    # Read prompt template
    prompt_template = read_file(prompt_template_path)
    if not prompt_template:
        return "Error: Prompt template not available."

    # Read class content
    class_content = read_file(class_content_path)
    if not class_content:
        return "Error: Class content not found."

    # Format the final prompt
    final_prompt = prompt_template.replace("{enhanced_merged_output}", class_content).replace("{userQuery}", user_query)

    # Call Gemini API
    response = call_gemini_api(final_prompt)
    #print(response)
    return response if response else "Error: Unable to get a response from the AI."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
        print(process_query(user_query))
    else:
        print("Error: No user query provided.")
