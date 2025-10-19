<!DOCTYPE html>
<html lang="en">
<body>

  <h1>🧾 Blue Team Log Analyzer</h1>

  <p>A modular and intelligent <strong>Log Analysis System</strong> designed to <strong>parse, store, and summarize</strong> logs from multiple sources.  
  Built using <strong>Python</strong>, <strong>TinyDB</strong> for lightweight storage, and the <strong>Gemini API (LLM)</strong> for automated insights.</p>

  <h2>🚀 Overview</h2>
  <p>The project simplifies log analysis by automatically:</p>
  <ul>
    <li>Detecting log file types</li>
    <li>Parsing and converting logs into structured JSON</li>
    <li>Storing logs in a <strong>TinyDB database</strong></li>
    <li>Filtering suspicious or error entries</li>
    <li>Summarizing key insights via an <strong>LLM (Gemini)</strong></li>
  </ul>

  <h2>🧩 Features</h2>
  <ul>
    <li><strong>Log File Ingestion:</strong> Load log files from any supported source.</li>
    <li><strong>Parsing & JSON Conversion:</strong> Transform raw logs into structured JSON objects for easier analysis.</li>
    <li><strong>Database Storage:</strong> Store logs and filtered entries in TinyDB for lightweight project-based management.</li>
    <li><strong>Filtering:</strong> Remove noise and focus on errors or suspicious entries.</li>
    <li><strong>LLM Summarization:</strong> Generate summaries of logs and highlight important patterns or anomalies.</li>
    <li><strong>Project Management:</strong> Create, delete, and read projects with organized log data.</li>
  </ul>

  <h2>⚙️ Requirements</h2>
  <ul>
    <li>Python 3.10+</li>
    <li>pip packages:
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Gemini API Key (set in <code>.env</code>)</li>
  </ul>

  <h2>📂 Project Structure</h2>
  <pre><code>
project/
├─ main.py          # Entry point
├─ parser/
│  ├─ log_parser.py # Parsing logic
├─ database.py      # TinyDB integration
├─ ai/
│  ├─ genai.py      # LLM summarization
├─ .env             # API keys
  </code></pre>

  <h2>💡 Notes</h2>
  <ul>
    <li>The project is modular — TinyDB can be swapped for SQLite or other databases.</li>
    <li>Filtering rules can be customized in <code>log_parser.py</code>.</li>
    <li>LLM summarization currently uses the Gemini API, but it can be replaced with other LLMs.</li>
  </ul>

  <h2>🛠️ CLI Usage</h2>

  <h3>1. Basic Log Analysis</h3>
  <pre><code>python main.py path/to/logfile.log --project ProjectName [--save] [--format txt|json|csv]</code></pre>
  <ul>
    <li><code>path/to/logfile.log</code> → Path to the log file (optional if using <code>--delete</code>)</li>
    <li><code>--project, -p</code> → Project name (creates if it doesn't exist)</li>
    <li><code>--save</code> → Save summarized output (optional)</li>
    <li><code>--format</code> → Output format (default <code>txt</code>; options: <code>txt</code>, <code>json</code>, <code>csv</code>)</li>
  </ul>

  <p><strong>Example:</strong></p>
  <pre><code>python main.py logs/system.log --project SecurityLogs --save --format json</code></pre>

  <h3>2. Delete a Project</h3>
  <pre><code>python main.py --delete ProjectName</code></pre>
  <ul>
    <li><code>--delete, -d</code> → Name of the project to delete</li>
    <li>Does <strong>not require</strong> a log file or <code>--project</code></li>
  </ul>

  <p><strong>Example:</strong></p>
  <pre><code>python main.py --delete SecurityLogs</code></pre>

  <h3>3. Notes</h3>
  <ul>
    <li>If <code>--delete</code> is not used, both <code>path</code> and <code>--project</code> are required.</li>
    <li>Output is shown in the console unless <code>--save</code> is specified.</li>
    <li>Supported output formats: <code>txt</code>, <code>json</code>, <code>csv</code>.</li>
  </ul>

  <h2>✨ Next Steps</h2>
  <ul>
    <li>Advanced filtering for complex error patterns</li>
    <li>Web interface to visualize logs and summaries</li>
    <li>Multi-project dashboard for managing multiple log analysis sessions</li>
  </ul>

</body>
</html>
