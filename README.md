# AI AgentOps & LLM Evaluation Platform

An AI observability and evaluation platform for building, testing, evaluating, and monitoring Large Language Model (LLM) applications.

The platform uses Groq-hosted LLMs to generate responses and an LLM-as-a-Judge pipeline to evaluate those responses for relevance, accuracy, completeness, clarity, quality, latency, and failure conditions.

Evaluation results are stored in SQLite and visualized through a Streamlit monitoring dashboard. Automated tests are implemented using Pytest and executed automatically through GitHub Actions.

---

## Project Overview

Modern LLM applications need more than just a model that generates responses.

They also need mechanisms to:

- Evaluate response quality
- Track response latency
- Detect failures
- Compare prompt versions
- Store evaluation results
- Monitor model behavior
- Test application logic
- Automatically validate code changes

This project demonstrates a practical LLMOps / AI engineering workflow for evaluating and monitoring LLM applications.

---

## Key Features

- LLM response generation using Groq
- Qwen LLM integration
- LLM-as-a-Judge evaluation
- Relevance scoring
- Accuracy scoring
- Completeness scoring
- Clarity scoring
- Overall quality scoring
- Failure detection
- Response latency tracking
- Prompt version management
- SQLite evaluation logging
- SQLAlchemy database layer
- FastAPI REST API
- Interactive Swagger API documentation
- Streamlit monitoring dashboard
- Automated testing using Pytest
- GitHub Actions CI
- Environment-based API key management
- External LLM calls mocked during testing

---

## Architecture

```text
                           User
                            |
                            v
                    FastAPI REST API
                            |
                            v
                     Prompt Manager
                            |
                            v
                        Groq LLM
                            |
                            v
                   Generated Response
                            |
                            v
                    LLM-as-a-Judge
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Relevance      Accuracy       Completeness
             |              |              |
             +--------------+--------------+
                            |
                            v
                         Clarity
                            |
                            v
                     Overall Score
                            |
                            v
                    Failure Detection
                            |
                            v
                    Latency Tracking
                            |
                            v
                     SQLite Database
                            |
                            v
                  Streamlit Dashboard
```

---

## Request Flow

1. User sends a question through the FastAPI `/chat` endpoint.
2. The selected prompt version is loaded from the `prompts/` directory.
3. The prompt and user question are sent to the Groq-hosted Qwen model.
4. The model generates an AI response.
5. Response latency is calculated.
6. The response is passed to the LLM-as-a-Judge evaluator.
7. The evaluator scores relevance, accuracy, completeness, clarity, and overall quality.
8. Failure conditions are detected.
9. The evaluation result is stored in SQLite.
10. The Streamlit dashboard reads the stored data and displays monitoring metrics.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API development |
| Groq | LLM API provider |
| Qwen | LLM used for generation and evaluation |
| SQLAlchemy | Database ORM |
| SQLite | Local evaluation database |
| Streamlit | Monitoring dashboard |
| Pandas | Data analysis |
| Pytest | Automated testing |
| GitHub Actions | Continuous Integration |
| python-dotenv | Environment variable management |

---

## Project Structure

```text
ai-agentops-llm-evaluation/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   ├── evaluator.py
│   ├── database.py
│   └── prompt_manager.py
│
├── dashboard/
│   └── app.py
│
├── prompts/
│   ├── v1.txt
│   └── v2.txt
│
├── tests/
│   ├── test_api.py
│   ├── test_evaluator.py
│   └── test_prompt_manager.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

The SQLite database `agentops.db` is generated automatically when the application runs and is excluded from Git using `.gitignore`.

---

## Prerequisites

Install the following before running the project:

- Python 3.10+
- Git
- VS Code or another code editor
- A Groq API key

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mirza-py/ai-agentops-llm-evaluation.git
cd ai-agentops-llm-evaluation
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If using Command Prompt:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Do not commit the `.env` file to GitHub.

The project includes `.env` in `.gitignore` to prevent accidental exposure of API credentials.

---

## Running the FastAPI Application

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Root Endpoint

```http
GET /
```

Example response:

```json
{
  "message": "AI AgentOps Platform is running",
  "version": "2.0.0"
}
```

### Chat Endpoint

```http
POST /chat
```

Request:

```json
{
  "prompt": "What is machine learning?",
  "prompt_version": "v1"
}
```

The API generates an LLM response and evaluates it automatically.

The response contains:

- Generated answer
- Model information
- Prompt version
- Response latency
- Relevance score
- Accuracy score
- Completeness score
- Clarity score
- Overall quality score
- Failure status
- Evaluation feedback
- Database status

---

## LLM Integration

The project uses the Groq API to generate responses from a Qwen-hosted language model.

The LLM integration is implemented in:

```text
app/llm.py
```

The API key is loaded from the environment using `python-dotenv`.

The application does not hard-code the API key.

---

## LLM-as-a-Judge Evaluation

The project uses a second LLM evaluation step to assess the generated response.

The evaluator checks five major quality dimensions:

### Relevance

Measures how directly the response answers the user's question.

### Accuracy

Measures whether the response is factually correct.

### Completeness

Measures whether the response adequately covers the question.

### Clarity

Measures how understandable and well-structured the response is.

### Overall Quality

Provides an overall quality score from 0 to 10.

The evaluator also checks for failure conditions and generates short feedback explaining the evaluation.

The evaluator is implemented in:

```text
app/evaluator.py
```

---

## Structured Evaluation Output

The evaluator returns structured data similar to:

```json
{
  "relevance": 9,
  "accuracy": 8,
  "completeness": 9,
  "clarity": 10,
  "quality_score": 9,
  "failure": false,
  "reason": "Strong response."
}
```

The evaluator also includes JSON extraction logic so that structured evaluation data can be recovered when the LLM wraps JSON inside a Markdown code block.

---

## Prompt Versioning

Prompt templates are stored separately in the `prompts/` directory.

Example:

```text
prompts/
├── v1.txt
└── v2.txt
```

`v1` provides a basic assistant instruction.

`v2` provides a more structured expert-assistant instruction.

The API allows the user to select a prompt version:

```json
{
  "prompt": "Explain machine learning.",
  "prompt_version": "v2"
}
```

This makes it possible to compare how different prompt versions affect response quality and latency.

---

## Database

The project uses SQLite for storing evaluation results.

Database file:

```text
agentops.db
```

SQLAlchemy is used as the ORM layer.

The database stores information such as:

- Prompt
- Generated response
- Model
- Prompt version
- Latency
- Relevance
- Accuracy
- Completeness
- Clarity
- Quality score
- Failure status
- Failure reason

The database implementation is located in:

```text
app/database.py
```

---

## Streamlit Monitoring Dashboard

The project includes a Streamlit dashboard for monitoring LLM evaluation results.

Run the dashboard from the project root:

```bash
streamlit run dashboard/app.py
```

The dashboard provides:

- Total requests
- Average quality score
- Average latency
- Failure rate
- Evaluation metric charts
- Latency trends
- Prompt version performance
- Recent LLM requests
- Failed evaluations

The dashboard reads evaluation data directly from the SQLite database.

---

## Dashboard Metrics

The dashboard tracks four main evaluation dimensions:

```text
Relevance
Accuracy
Completeness
Clarity
```

It also tracks:

```text
Overall Quality
Response Latency
Failure Rate
Request Count
```

These metrics provide visibility into the behavior of the LLM application.

---

## Testing

The project uses Pytest for automated testing.

Run all tests:

```bash
pytest -v
```

The test suite covers:

- API endpoints
- Evaluator behavior
- JSON extraction
- Empty responses
- Prompt loading
- Invalid prompt versions
- LLM evaluation logic

---

## Mocking LLM Calls

The tests do not require a real Groq API request.

External LLM calls are mocked during testing.

This provides several advantages:

- Tests run without an API key
- Tests are faster
- Tests do not consume API credits
- CI can run automatically
- Test results are deterministic

The evaluator tests replace the real LLM client with a fake client that returns controlled evaluation data.

---

## Pytest Configuration

The project uses:

```text
pytest.ini
```

Configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
pythonpath = .
```

This allows Pytest to correctly discover the application package and test files.

---

## Continuous Integration

GitHub Actions automatically runs the test suite whenever changes are pushed to the repository or a pull request is created.

Workflow file:

```text
.github/workflows/ci.yml
```

The CI pipeline:

1. Checks out the repository.
2. Sets up Python.
3. Installs project dependencies.
4. Runs the Pytest test suite.

Example command used by CI:

```bash
pytest -v
```

This helps ensure that code changes do not break the application.

---

## Security

The project follows basic API credential security practices.

### API keys are stored in `.env`

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### `.env` is ignored by Git

```gitignore
.env
```

### Runtime database is ignored

```gitignore
agentops.db
```

### Testing does not require the real API key

The LLM client is mocked during automated tests.

Never commit real API keys, passwords, tokens, or other secrets to GitHub.

---

## Git Ignore

Important ignored files include:

```text
venv/
.env
__pycache__/
*.pyc
.vscode/
agentops.db
.pytest_cache/
```

---

## Troubleshooting

### 1. Groq API key error

If the application reports:

```text
GROQ_API_KEY is not configured.
```

Check that `.env` exists in the project root and contains:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Then restart the FastAPI server.

---

### 2. ModuleNotFoundError: app

Run the application and tests from the project root:

```text
ai-agentops-llm-evaluation/
```

Also make sure:

```text
app/__init__.py
```

exists.

---

### 3. Tests cannot find the application package

Make sure `pytest.ini` contains:

```ini
pythonpath = .
```

Then run:

```bash
pytest -v
```

---

### 4. Dashboard cannot find the database

Start the FastAPI application and send at least one request through `/chat`.

This creates:

```text
agentops.db
```

Then run:

```bash
streamlit run dashboard/app.py
```

Run Streamlit from the project root so the relative database path is correct.

---

### 5. SQLite schema error

If the database structure is outdated after changing the SQLAlchemy model, stop the application and remove the local:

```text
agentops.db
```

Then restart FastAPI.

A new database will be created automatically.

Do not commit the local database to GitHub.

---

## Complete Local Workflow

### Terminal 1 — Start FastAPI

```bash
uvicorn app.main:app --reload
```

### Open Swagger

```text
http://127.0.0.1:8000/docs
```

### Send a request

Use:

```http
POST /chat
```

with:

```json
{
  "prompt": "What is Python?",
  "prompt_version": "v1"
}
```

The system then:

```text
User Question
      ↓
Prompt Manager
      ↓
Groq / Qwen LLM
      ↓
Generated Response
      ↓
LLM-as-a-Judge
      ↓
Quality Evaluation
      ↓
SQLite
```

### Terminal 2 — Start Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard then displays the stored evaluation results.

---

## Example Development Workflow

```text
Write / modify code
        ↓
Run Pytest locally
        ↓
Commit changes
        ↓
Push to GitHub
        ↓
GitHub Actions runs tests
        ↓
Tests pass
        ↓
Changes validated
```

---

## Why This Project Matters

This project demonstrates practical concepts used in modern AI engineering and LLMOps workflows:

- LLM application development
- REST API development
- Prompt engineering
- Prompt versioning
- LLM evaluation
- LLM-as-a-Judge
- AI observability
- Response quality monitoring
- Latency monitoring
- Failure tracking
- Database logging
- Automated testing
- CI/CD fundamentals
- Dashboard development
- Secure environment configuration

---

## Limitations

This project is designed as a practical portfolio and learning project.

The evaluation scores are generated by an LLM judge, so they should be treated as automated evaluation signals rather than absolute ground truth.

The project currently uses SQLite for local storage and a single LLM provider.

For production-scale systems, additional improvements could include distributed databases, authentication, monitoring infrastructure, multiple model providers, stronger evaluation datasets, and human review workflows.

---

## Future Improvements

Possible future improvements include:

- Add authentication and authorization
- Add multiple LLM providers
- Add human evaluation workflows
- Add evaluation datasets
- Add automated regression testing for prompts
- Add model comparison
- Add token usage tracking
- Add cost tracking
- Add advanced analytics
- Add evaluation history filtering
- Add alerting for quality degradation
- Add production database support
- Add experiment tracking
- Add more detailed observability metrics

---

---

## Repository

GitHub:

https://github.com/mirza-py/ai-agentops-llm-evaluation

---

## Author

**Mirza Niyaz Baig**

GitHub:

https://github.com/mirza-py