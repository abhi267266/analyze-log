import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from ai.genai import setup_client, summarize_log
from parser.log_parser import delete_project, parse_logs, read_log, save_log, take_input, log_detection
from project_manager import ProjectManager

load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    model_name = "gemini-2.0-flash-001"
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    # Initialize AI clients
    summary_client = setup_client(api_key, model_name)
    log_client = setup_client(api_key, model_name)

    # Parse CLI arguments
    args = take_input()
    if args.delete:
        delete_project(args.delete)
        sys.exit(0)


    # 🧱 Initialize Project
    pm = ProjectManager()
    db = pm.create_project(args.project)  # Create/get project DB

    # 🧾 Read log file
    log_content = read_log(args.path)
    first_lines = "\n".join(log_content.splitlines()[:5])

    # 1️⃣ Detect log type & regex
    log_type, ai_regex = log_detection(log_client, model_name, first_lines)
    print(f"🔍 Detected log type: {log_type}")

    # 2️⃣ Parse the log file
    parsed_logs = parse_logs(args.path, ai_regex)
    print(f"📄 Parsed {len(parsed_logs)} log entries")

    # 🧠 Save parsed logs into the project's TinyDB (deduplicated)
    db.bulk_insert(parsed_logs)

    # ✅ Ensure data is flushed to disk
    db.db.close()

    # 3️⃣ Print parsed logs (optional for debugging)
    log_json_str = json.dumps(parsed_logs, indent=2)
    # print("\nParsed Logs:\n", log_json_str)

    # 4️⃣ Summarize logs using the LLM
    print("\n🧩 Summarizing log...\n")
    summary = summarize_log(summary_client, model_name, log_json_str)

    # 5️⃣ Save summary if requested
    if args.save:
        save_log(args, summary)
        print(f"💾 Summary saved in {args.format} format.")

    print(f"\n✅ Project '{args.project}' updated successfully.")


if __name__ == "__main__":
    main()
