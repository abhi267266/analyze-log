import json
import os
import sys
from dotenv import load_dotenv

from ai.genai import setup_client, summarize_log
from parser.log_parser import delete_project, parse_logs, read_log, save_log, take_input, log_detection
from database import ProjectDatabase

load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = "gemini-2.0-flash-001"

    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    # Initialize AI clients
    summary_client = setup_client(api_key, model_name)
    log_client = setup_client(api_key, model_name)

    # Parse CLI arguments
    args = take_input()

    # Delete project if requested
    if args.delete:
        delete_project(args.delete)
        sys.exit(0)

    # Initialize project DB
    db = ProjectDatabase(args.project)

    # Read and inspect log file
    log_content = read_log(args.path)
    first_lines = "\n".join(log_content.splitlines()[:5])

    # Detect log type & regex
    log_type, ai_regex = log_detection(log_client, model_name, first_lines)
    print(f"🔍 Detected log type: {log_type}")

    # Parse the log file
    parsed_logs = parse_logs(args.path, ai_regex)

    # Identify important logs
    important_logs = [log for log in parsed_logs if log.get("level") in ["ERROR", "WARNING", "CRITICAL"]]

    # Summarize logs
    print("\n🧩 Summarizing log...\n")
    summary = summarize_log(summary_client, model_name, json.dumps(parsed_logs, indent=2))

    # Create or update project (handles deduplication internally)
    db.create_or_update_project(
        log_type=log_type,
        logs=parsed_logs,
        important_logs=important_logs,
        summary=summary,
        file_content=log_content  # pass file content for automatic file-level deduplication
    )

    # Save summary to file if requested
    if args.save:
        save_log(args, summary)
        print(f"💾 Summary saved in {args.format} format.")

    print(f"\n✅ Project '{args.project}' updated successfully.")


if __name__ == "__main__":
    main()
