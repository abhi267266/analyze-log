import os
import sys
from dotenv import load_dotenv
from ai.genai import setup



load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = 'gemini-2.0-flash-001'
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
    setup(api_key, model_name)
    
    
   



if __name__ == "__main__":
    main()
