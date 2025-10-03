from google import genai
from google.genai import types
from ai.system_prompt import prompt


def setup(api_key, model_name):
    client = genai.Client(api_key=api_key)
    system_prompt = prompt()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text="""
    Log filename: system_logs.txt
    Extracted features / flagged events:
    - Multiple failed SSH login attempts from 192.168.1.50
    - Unexpected new process: /tmp/malware
    - Suspicious URL accessed: http://malicious.example.com

    Representative raw log lines:
    Oct 3 12:05:22 server sshd[1234]: Failed password for root from 192.168.1.50 port 54522 ssh2
    Oct 3 12:05:25 server sshd[1235]: Failed password for root from 192.168.1.50 port 54523 ssh2
    Oct 3 12:05:30 server sshd[1236]: Accepted password for admin from 192.168.1.51 port 54524 ssh2
    """)]
        )
    ]

    # Streaming response
    stream = client.models.generate_content_stream(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
    )

    for event in stream:
        if event.candidates:
            for part in event.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)