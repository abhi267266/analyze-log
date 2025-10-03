from google import genai
from google.genai import types
from ai.system_prompt import prompt

def setup_client(api_key, model_name):
    return genai.Client(api_key=api_key)



def summarize_log(client, model_name, log_content):
    system_prompt = prompt()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=log_content)]
        )
    ]

    stream = client.models.generate_content_stream(
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


