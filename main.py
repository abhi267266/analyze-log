import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from ai.genai import setup_client, summarize_log

load_dotenv()

def main():

    # CLI argument parsing
    parser = argparse.ArgumentParser(description="Blue team log analyzer CLI")
    parser.add_argument("path", help="Path to the log file")
    parser.add_argument("--save", action="store_true", help="Save the summarized output")
    parser.add_argument("--format", choices=["txt", "json", "csv"], default="txt", help="Output format")
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = 'gemini-2.0-flash-001'
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    client = setup_client(api_key, model_name)

    # Read log file
    if not os.path.exists(args.path):
        print(f"Error: File '{args.path}' not found.")
        sys.exit(1)
    with open(args.path, "r") as f:
        log_content = f.read()

    print("Summarizing log...\n")
    summary = summarize_log(client, model_name, log_content)

    if args.save:
        # Create summary directory if it doesn't exist
        summary_dir = "summary"
        os.makedirs(summary_dir, exist_ok=True)
        
        # Get filename without extension
        filename = Path(args.path).stem
        
        # Create the save path in the summary folder
        save_path = os.path.join(summary_dir, f"{filename}_summary.{args.format}")
        
        with open(save_path, "w") as f:
            f.write(summary)
        print(f"\nSummary saved to {save_path}")

if __name__ == "__main__":
    main()