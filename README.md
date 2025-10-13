<!DOCTYPE html>
<html lang="en">
<body>

  <h1>🧾 Log Analysis Project</h1>

  <p>A modular and intelligent <strong>Log Analysis System</strong> built for MCA coursework — designed to <strong>parse, store, and summarize</strong> logs from multiple sources.  
  This project blends <strong>Python</strong>, <strong>TinyDB</strong> for lightweight storage, and the <strong>Gemini API (LLM)</strong> for automated insights.</p>

  <h2>🚀 Overview</h2>
  <p>The project aims to simplify log analysis by automatically:</p>
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

  <h2>⚙️ How It Works</h2>
  <ol>
    <li>Place your log files in a directory accessible to the script.</li>
    <li>Set up your Gemini API key in a <code>.env</code> file as <code>GEMINI_API_KEY=your_key_here</code>.</li>
    <li>Run <code>main.py</code> to start the workflow:</li>
    <pre><code>python main.py</code></pre>
    <li>The program will:
      <ul>
        <li>Parse the logs</li>
        <li>Convert them to JSON</li>
        <li>Store everything in TinyDB</li>
        <li>Filter and summarize important entries using the LLM</li>
      </ul>
    </li>
    <li>View the results in the console or query the TinyDB database for detailed entries.</li>
  </ol>

  <h2>🛠️ Requirements</h2>
  <ul>
    <li>Python 3.10+</li>
    <li>pip packages:
      <pre><code>pip install python-dotenv tinydb</code></pre>
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
    <li>The project is modular — you can swap TinyDB for SQLite or any other database later.</li>
    <li>Filtering rules can be customized in <code>log_parser.py</code>.</li>
    <li>LLM summarization currently uses the Gemini API; this can be replaced with other LLMs as needed.</li>
  </ul>

  <h2>✨ Next Steps</h2>
  <ul>
    <li>Advanced filtering for more complex error patterns</li>
    <li>Web interface to visualize logs and summaries</li>
    <li>Multi-project dashboard for managing multiple log analysis sessions</li>
  </ul>

</body>
</html>
