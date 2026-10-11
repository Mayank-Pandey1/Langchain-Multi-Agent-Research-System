# 🔎 LangChain Multi-Agent Research System

An AI-powered research assistant built with **LangChain, Google Gemini, Tavily Search, and Streamlit**. The system automates the research process through a sequential multi-agent workflow that searches the web, extracts relevant information, generates a structured report, and evaluates the report using a critic chain.

## ✨ Features

- **🤖 Multi-Agent Architecture:** Separates research into specialized agents and chains.
- **🌐 Web Search:** Uses Tavily Search to discover relevant online information.
- **📖 Content Extraction:** Identifies relevant URLs and extracts deeper content for research.
- **✍️ Automated Report Generation:** Synthesizes search results and extracted content into a structured report.
- **🧐 AI-Powered Critique:** Reviews the generated report and provides feedback.
- **🖥️ Streamlit Interface:** Provides an interactive interface for entering research topics and viewing results.
- **📊 Pipeline Visibility:** Displays search results, extracted content, the final report, and critic feedback separately.
- **⬇️ Report Export:** Supports downloading the generated report in Markdown format.

## 🏗️ Architecture

The application follows a sequential research pipeline:

```text
              ┌────────────────────────┐
              │   User Research Topic  │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     Search Agent       │
              │    Tavily Web Search   │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     Reader Agent       │
              │   URL Content Scraping │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │      Writer Chain      │
              │  Research Report       │
              │      Generation       │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │      Critic Chain      │
              │   Report Evaluation    │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Final Report +       │
              │   Critic Feedback      │
              └────────────────────────┘
```

## 🔄 How It Works

The system processes a research topic through four stages.

| Stage | Component | Responsibility |
|---|---|---|
| 1 | Search Agent | Searches the web for recent, relevant information using Tavily. |
| 2 | Reader Agent | Selects relevant URLs and extracts additional content for deeper research. |
| 3 | Writer Chain | Combines search results and extracted content to generate a structured report. |
| 4 | Critic Chain | Evaluates the generated report and provides feedback. |

The output of each stage is stored in the pipeline state and passed to subsequent stages when required.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent creation, tool integration, and chain orchestration |
| Google Gemini | Large language model for research and report generation |
| Tavily Search API | Web search and information retrieval |
| Streamlit | Interactive web application |
| Python-dotenv | Environment variable management |
| Requests / web scraping libraries | HTTP requests and source content extraction, as configured in the project |

## 📁 Project Structure

```text
Langchain-Multi-Agent-Research-System/
│
├── app.py
│   └── Streamlit user interface
│
├── main.py
│   └── Script entry point for running the research pipeline
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── .gitignore
│   └── Files excluded from version control
│
├── LICENSE
│   └── MIT License
│
└── src/
    ├── agents/
    │   └── agents.py
    │       ├── build_search_agent()
    │       ├── build_reader_agent()
    │       ├── writer_chain
    │       └── critic_chain
    │
    ├── tools/
    │   └── tools.py
    │       └── Custom research and scraping tools
    │
    └── pipelines/
        └── pipeline.py
            └── run_research_pipeline()
```

*Note: The tree highlights the main application modules. Your actual directory structure and available tools may vary with your current implementation.*

## 🚀 Getting Started

### Prerequisites

Before running the application, ensure you have:

- Python 3.10 or later.
- A Google Gemini API key.
- A Tavily API key.
- Git installed on your system.

### 1. Clone the repository

```bash
git clone https://github.com/Mayank-Pandey1/Langchain-Multi-Agent-Research-System.git

cd Langchain-Multi-Agent-Research-System
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python executable directly or use Command Prompt:

```bat
myenv\Scripts\activate.bat
```

On macOS or Linux:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root directory.

Add the credentials required by your application:

```dotenv
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

If your current implementation uses additional external services, add their corresponding API keys as well.

**Getting API keys:**

- Google Gemini: https://aistudio.google.com/apikey
- Tavily: https://tavily.com/

Keep your API keys private. Do not commit your `.env` file to GitHub.

### 5. Run the application

Launch the Streamlit interface:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

To run the script entry point instead:

```bash
python main.py
```

Use the entry point appropriate to your current `main.py` implementation.

## 💻 Usage

1. Launch the application.
2. Enter a research topic, such as *How is Agentic AI transforming cybersecurity operations?*
3. Start the research process.
4. Let the Search Agent retrieve relevant web information.
5. Let the Reader Agent extract additional content from selected sources.
6. Review the report generated by the Writer Chain.
7. Examine the Critic Chain's feedback.
8. Download the final report as a Markdown file if the interface provides the export option.

## 📦 Pipeline State

The research pipeline returns a dictionary containing the outputs of each stage:

```python
{
    "search_results": "...",
    "scraped_content": "...",
    "report": "...",
    "feedback": "..."
}
```

These fields represent:

- `search_results`: Information returned by the Search Agent.
- `scraped_content`: Content extracted by the Reader Agent.
- `report`: Research report produced by the Writer Chain.
- `feedback`: Evaluation and feedback produced by the Critic Chain.

Example usage:

```python
from src.pipelines.pipeline import run_research_pipeline

topic = "Applications of Agentic AI in Cybersecurity"

result = run_research_pipeline(topic)

print("Search Results:")
print(result["search_results"])

print("\nExtracted Content:")
print(result["scraped_content"])

print("\nFinal Report:")
print(result["report"])

print("\nCritic Feedback:")
print(result["feedback"])
```

## 🔐 Security and Configuration

- Store API keys in environment variables or a local `.env` file.
- Add `.env` and virtual environment directories to `.gitignore`.
- Never publish API keys, tokens, or other secrets in source code.
- Be mindful of API usage limits and costs.
- Treat scraped webpages as untrusted input.
- Verify important claims against their original sources before relying on generated reports.

## 🚧 Potential Improvements

- Add live progress updates for individual pipeline stages.
- Support multiple sources and PDF content extraction.
- Include source URLs and citations directly in the generated report.
- Add retry logic and handling for empty agent responses.
- Allow users to export reports to PDF or DOCX.
- Add research history and reusable topic templates.
- Introduce automated evaluation metrics for factual accuracy and source quality.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request describing the changes.

## 📄 License

This project is distributed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

## 👨‍💻 Author

**Mayank Pandey**

- GitHub: [Mayank-Pandey1](https://github.com/Mayank-Pandey1)
- Project: [LangChain Multi-Agent Research System](https://github.com/Mayank-Pandey1/Langchain-Multi-Agent-Research-System)

---

*Built to explore agentic AI, tool-augmented research, LangChain orchestration, and automated report generation.*