On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

Okay. Since Git says working tree clean while GitHub shows an empty README, the most likely issue is that Git has README.md marked as assume-unchanged/skip-worktree.

Let's fix that directly.

In the VS Code terminal, run these commands one by one:

git update-index --no-assume-unchanged README.md
git update-index --no-skip-worktree README.md

Now run:

git status
If it shows modified: README.md

Run:

git add README.md
git commit -m "Add complete README documentation"
git push

Then refresh GitHub.

If it STILL says nothing to commit

Run this:

git hash-object README.md

and:

git rev-parse HEAD:README.md

Send me the two outputs.

Don't change or delete anything else in the project.

e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391

Exactly — we found the problem.

Both hashes are:

e69de29bb2d1d6434b8b29ae775ad8c2e48c5391

That is the Git hash for an empty file. So GitHub is correct: your committed README.md is empty. The content you saw in VS Code was not actually saved to the file on disk.

I created a clean, properly formatted README.md from the README content you provided.

Download the corrected README.md

Do this now
Download the file above.
In VS Code, replace your current:
ai-agentops-llm-evaluation/README.md

with the downloaded README.md.
3. Open it in VS Code and press:

Ctrl + S
Run:
git status

You should now see:

modified: README.md
Then run:
git add README.md
git commit -m "Add complete README documentation"
git push
Refresh your GitHub repository.

The README should then appear on the GitHub page.

Don't modify any other project files.

README.md
Document
actually i mistakely clone project

Ahh, yes 😄 — that explains the whole confusion.

You cloned the project again, so you were probably working in a different copy/folder than the original project where your README content was saved.

That's why Git was consistently showing:

nothing to commit, working tree clean

and:

e69de29...

because the newly cloned repository's README.md was genuinely empty.

Let's identify the correct project folder

In your VS Code terminal, run:

pwd

Then:

git remote -v

And:

git status

Send me those three outputs.

I'll tell you which folder you're currently working in and then we'll put the README in the correct project — without messing up your existing code.

I understand. 😕 We went around in circles because of that cloned folder. Let's stop troubleshooting it for now.

You haven't lost your actual project. The folder we're trying to delete is only the new clone.

Easiest solution

Don't fight with Windows deletion right now.

Close VS Code completely.
Restart your PC.
Don't open the cloned folder again.
Open File Explorer and go to:
C:\ai-agentops
Delete only:
ai-agentops-llm-evaluation

Leave your original project folder untouched.

If Windows still refuses to delete it after a restart, stop there and send me a screenshot. I'll give you one precise method to remove the locked folder.

And don't worry: we can continue the project from your original folder after this.

ok its delete now what next

Good. 👍 Let's reset cleanly and continue from your original project.

Step 1 — Open the original project

Open VS Code and open:

C:\ai-agentops\ai-agentops

Make sure you see:

app
dashboard
prompts
tests
.github
requirements.txt
README.md
Step 2 — Open the terminal

In VS Code:

Terminal → New Terminal

Then run:

cd C:\ai-agentops\ai-agentops
Step 3 — Check Git

Run:

git status

Send me the output.

Don't clone anything again and don't change any files yet. We'll first confirm that this is your original working project, then we'll fix the README and continue with the final project check.

On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\ai-agentops> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\ai-agentops\venv\Scripts\Activate.ps1)

Perfect. 👍 Now we're back in your original project, and this is exactly what we wanted.

Your output shows:

modified: README.md

So your README content is now detected correctly. Do not delete or replace anything.

Step 1 — Commit the README

Run:

git add README.md

Then:

git commit -m "Add complete README documentation"

Then:

git push
Step 2 — Verify

Run:

git status

You should get:

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

Then refresh your GitHub repository page.

Your README should now appear on GitHub.

After that, send me the git status output. Then we'll move to the next project check.

Library
/
README.md
AI AgentOps & LLM Evaluation Platform

An AI observability and evaluation platform for building, testing, evaluating, and monitoring Large Language Model (LLM) applications.

The platform uses Groq-hosted LLMs to generate responses and an LLM-as-a-Judge pipeline to evaluate those responses for relevance, accuracy, completeness, clarity, quality, latency, and failure conditions.

Evaluation results are stored in SQLite and visualized through a Streamlit monitoring dashboard. Automated tests are implemented using Pytest and executed automatically through GitHub Actions.

Project Overview

Modern LLM applications need more than just a model that generates responses.

They also need mechanisms to:

Evaluate response quality
Track response latency
Detect failures
Compare prompt versions
Store evaluation results
Monitor model behavior
Test application logic
Automatically validate code changes

This project demonstrates a practical LLMOps / AI engineering workflow for evaluating and monitoring LLM applications.

Key Features
LLM response generation using Groq
Qwen LLM integration
LLM-as-a-Judge evaluation
Relevance scoring
Accuracy scoring
Completeness scoring
Clarity scoring
Overall quality scoring
Failure detection
Response latency tracking
Prompt version management
SQLite evaluation logging
SQLAlchemy database layer
FastAPI REST API
Interactive Swagger API documentation
Streamlit monitoring dashboard
Automated testing using Pytest
GitHub Actions CI
Environment-based API key management
External LLM calls mocked during testing
Architecture

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


Request Flow
User sends a question through the FastAPI `/chat` endpoint.
The selected prompt version is loaded from the `prompts/` directory.
The prompt and user question are sent to the Groq-hosted Qwen model.
The model generates an AI response.
Response latency is calculated.
The response is passed to the LLM-as-a-Judge evaluator.
The evaluator scores relevance, accuracy, completeness, clarity, and overall quality.
Failure conditions are detected.
The evaluation result is stored in SQLite.
The Streamlit dashboard reads the stored data and displays monitoring metrics.
Tech Stack

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

Project Structure

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



The SQLite database `agentops.db` is generated automatically when the application runs and is excluded from Git using `.gitignore`.

Prerequisites

Install the following before running the project:

Python 3.10+
Git
VS Code or another code editor
A Groq API key
Installation
1. Clone the repository

git clone https://github.com/mirza-py/ai-agentops-llm-evaluation.git

cd ai-agentops-llm-evaluation


2. Create a virtual environment

Windows:


python -m venv venv


3. Activate the virtual environment

PowerShell:


.\venv\Scripts\Activate.ps1



If using Command Prompt:


venv\Scripts\activate


4. Install dependencies

pip install -r requirements.txt


Environment Variables

Create a `.env` file in the project root:


GROQ_API_KEY=YOUR_GROQ_API_KEY



Do not commit the `.env` file to GitHub.

The project includes `.env` in `.gitignore` to prevent accidental exposure of API credentials.

Running the FastAPI Application

From the project root:


uvicorn app.main:app --reload



The API will be available at:


http://127.0.0.1:8000



FastAPI automatically provides interactive API documentation at:


http://127.0.0.1:8000/docs


API Endpoints
Health Check

GET /health



Example response:


{

  "status": "healthy"

}


Root Endpoint

GET /



Example response:


{

  "message": "AI AgentOps Platform is running",

  "version": "2.0.0"

}


Chat Endpoint

POST /chat



Request:


{

  "prompt": "What is machine learning?",

  "prompt_version": "v1"

}



The API generates an LLM response and evaluates it automatically.

The response contains:

Generated answer
Model information
Prompt version
Response latency
Relevance score
Accuracy score
Completeness score
Clarity score
Overall quality score
Failure status
Evaluation feedback
Database status
LLM Integration

The project uses the Groq API to generate responses from a Qwen-hosted language model.

The LLM integration is implemented in:


app/llm.py



The API key is loaded from the environment using `python-dotenv`.

The application does not hard-code the API key.

LLM-as-a-Judge Evaluation

The project uses a second LLM evaluation step to assess the generated response.

The evaluator checks five major quality dimensions:

Relevance

Measures how directly the response answers the user's question.

Accuracy

Measures whether the response is factually correct.

Completeness

Measures whether the response adequately covers the question.

Clarity

Measures how understandable and well-structured the response is.

Overall Quality

Provides an overall quality score from 0 to 10.

The evaluator also checks for failure conditions and generates short feedback explaining the evaluation.

The evaluator is implemented in:


app/evaluator.py


Structured Evaluation Output

The evaluator returns structured data similar to:


{

  "relevance": 9,

  "accuracy": 8,

  "completeness": 9,

  "clarity": 10,

  "quality_score": 9,

  "failure": false,

  "reason": "Strong response."

}



The evaluator also includes JSON extraction logic so that structured evaluation data can be recovered when the LLM wraps JSON inside a Markdown code block.

Prompt Versioning

Prompt templates are stored separately in the `prompts/` directory.

Example:


prompts/

├── v1.txt

└── v2.txt



`v1` provides a basic assistant instruction.

`v2` provides a more structured expert-assistant instruction.

The API allows the user to select a prompt version:


{

  "prompt": "Explain machine learning.",

  "prompt_version": "v2"

}



This makes it possible to compare how different prompt versions affect response quality and latency.

Database

The project uses SQLite for storing evaluation results.

Database file:


agentops.db



SQLAlchemy is used as the ORM layer.

The database stores information such as:

Prompt
Generated response
Model
Prompt version
Latency
Relevance
Accuracy
Completeness
Clarity
Quality score
Failure status
Failure reason

The database implementation is located in:


app/database.py


Streamlit Monitoring Dashboard

The project includes a Streamlit dashboard for monitoring LLM evaluation results.

Run the dashboard from the project root:


streamlit run dashboard/app.py



The dashboard provides:

Total requests
Average quality score
Average latency
Failure rate
Evaluation metric charts
Latency trends
Prompt version performance
Recent LLM requests
Failed evaluations

The dashboard reads evaluation data directly from the SQLite database.

Dashboard Metrics

The dashboard tracks four main evaluation dimensions:


Relevance

Accuracy

Completeness

Clarity



It also tracks:


Overall Quality

Response Latency

Failure Rate

Request Count



These metrics provide visibility into the behavior of the LLM application.

Testing

The project uses Pytest for automated testing.

Run all tests:


pytest -v



The test suite covers:

API endpoints
Evaluator behavior
JSON extraction
Empty responses
Prompt loading
Invalid prompt versions
LLM evaluation logic
Mocking LLM Calls

The tests do not require a real Groq API request.

External LLM calls are mocked during testing.

This provides several advantages:

Tests run without an API key
Tests are faster
Tests do not consume API credits
CI can run automatically
Test results are deterministic

The evaluator tests replace the real LLM client with a fake client that returns controlled evaluation data.

Pytest Configuration

The project uses:


pytest.ini



Configuration:


[pytest]

testpaths = tests

python_files = test_*.py

python_functions = test_*

pythonpath = .



This allows Pytest to correctly discover the application package and test files.

Continuous Integration

GitHub Actions automatically runs the test suite whenever changes are pushed to the repository or a pull request is created.

Workflow file:


.github/workflows/ci.yml



The CI pipeline:

Checks out the repository.
Sets up Python.
Installs project dependencies.
Runs the Pytest test suite.

Example command used by CI:


pytest -v



This helps ensure that code changes do not break the application.

Security

The project follows basic API credential security practices.

API keys are stored in `.env`

GROQ_API_KEY=YOUR_GROQ_API_KEY


`.env` is ignored by Git

.env


Runtime database is ignored

agentops.db


Testing does not require the real API key

The LLM client is mocked during automated tests.

Never commit real API keys, passwords, tokens, or other secrets to GitHub.

Git Ignore

Important ignored files include:


venv/

.env

__pycache__/

*.pyc

.vscode/

agentops.db

.pytest_cache/


Troubleshooting
1. Groq API key error

If the application reports:


GROQ_API_KEY is not configured.



Check that `.env` exists in the project root and contains:


GROQ_API_KEY=YOUR_GROQ_API_KEY



Then restart the FastAPI server.

2. ModuleNotFoundError: app

Run the application and tests from the project root:


ai-agentops-llm-evaluation/



Also make sure:


app/__init__.py



exists.

3. Tests cannot find the application package

Make sure `pytest.ini` contains:


pythonpath = .



Then run:


pytest -v


4. Dashboard cannot find the database

Start the FastAPI application and send at least one request through `/chat`.

This creates:


agentops.db



Then run:


streamlit run dashboard/app.py



Run Streamlit from the project root so the relative database path is correct.

5. SQLite schema error

If the database structure is outdated after changing the SQLAlchemy model, stop the application and remove the local:


agentops.db



Then restart FastAPI.

A new database will be created automatically.

Do not commit the local database to GitHub.

Complete Local Workflow
Terminal 1 — Start FastAPI

uvicorn app.main:app --reload


Open Swagger

http://127.0.0.1:8000/docs


Send a request

Use:


POST /chat



with:


{

  "prompt": "What is Python?",

  "prompt_version": "v1"

}



The system then:


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


Terminal 2 — Start Dashboard

streamlit run dashboard/app.py



The dashboard then displays the stored evaluation results.

Example Development Workflow

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


Why This Project Matters

This project demonstrates practical concepts used in modern AI engineering and LLMOps workflows:

LLM application development
REST API development
Prompt engineering
Prompt versioning
LLM evaluation
LLM-as-a-Judge
AI observability
Response quality monitoring
Latency monitoring
Failure tracking
Database logging
Automated testing
CI/CD fundamentals
Dashboard development
Secure environment configuration
Limitations

This project is designed as a practical portfolio and learning project.

The evaluation scores are generated by an LLM judge, so they should be treated as automated evaluation signals rather than absolute ground truth.

The project currently uses SQLite for local storage and a single LLM provider.

For production-scale systems, additional improvements could include distributed databases, authentication, monitoring infrastructure, multiple model providers, stronger evaluation datasets, and human review workflows.

Future Improvements

Possible future improvements include:

Add authentication and authorization
Add multiple LLM providers
Add human evaluation workflows
Add evaluation datasets
Add automated regression testing for prompts
Add model comparison
Add token usage tracking
Add cost tracking
Add advanced analytics
Add evaluation history filtering
Add alerting for quality degradation
Add production database support
Add experiment tracking
Add more detailed observability metrics
Repository

GitHub:

https://github.com/mirza-py/ai-agentops-llm-evaluation

Author

Mirza Niyaz Baig

GitHub:

https://github.com/mirza-py