import json
import re
from google import genai
from google.genai import types
from ai.system_prompt import summary_prompt, log_detection_prompt

def setup_client(api_key, model_name):
    return genai.Client(api_key=api_key)


def summarize_log(sum_client, model_name, log_content):
    system_prompt = summary_prompt()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=log_content)]
        )
    ]

    stream = sum_client.models.generate_content_stream(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    summary = ""
    for event in stream:
        if event.candidates:
            for part in event.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)
                    summary += part.text
    return summary


def log_detection(log_client, model_name, lines):
    """
    Detects log type and generates a regex to parse log entries.
    
    Args:
        log_client: Gemini client for log detection
        model_name: model to use
        lines: first N lines of the log file (string)
    
    Returns:
        log_type (str), regex_pattern (str)
    """

    system_prompt = log_detection_prompt()

    # Prepare user message
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=f"Identify the log type and generate a parsing regex for these lines:\n{lines}")]
        )
    ]

    # Send to Gemini
    stream = log_client.models.generate_content_stream(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    # Collect the response from the stream
    response_text = ""
    for event in stream:
        if event.candidates:
            for part in event.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text

    # Remove triple backticks or other code fences
    cleaned_response = re.sub(r"^```json\s*|```$", "", response_text.strip(), flags=re.MULTILINE)

    try:
        result = json.loads(cleaned_response)
        log_type = result.get("log_type")
        regex = result.get("regex")
        return log_type, regex
    except json.JSONDecodeError:
        print("Failed to parse AI response:", cleaned_response)
        return None, None


