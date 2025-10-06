import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from ai.genai import log_detection, setup_client, summarize_log
from parser.log_parser import parse_logs, read_log, save_log, take_input

load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = 'gemini-2.0-flash-001'
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    summary_client = setup_client(api_key, model_name)
    log_client = setup_client(api_key, model_name)
    

    # CLI argument parsing
    args = take_input()
    # Read log file
    log_content = read_log(args.path)
    first_lines = "\n".join(log_content.splitlines()[:5])


    # 1. Detect log type & regex (already done)
    log_type, ai_regex = log_detection(log_client, model_name, first_lines)

    # 2. Parse the full log using AI regex
    parsed_logs = parse_logs(args.path, ai_regex)

    log_json_str = json.dumps(parsed_logs, indent=2)
    print(log_json_str)

    print("Summarizing log...\n")
    summary = summarize_log(summary_client, model_name, log_json_str)
    if args.save:
        save_log(args, summary)

if __name__ == "__main__":
    main()