import time

from fastapi import (
    FastAPI,
    HTTPException
)

from pydantic import BaseModel

from app.llm import generate_response

from app.evaluator import (
    evaluate_response
)

from app.database import (
    SessionLocal,
    EvaluationLog
)

from app.prompt_manager import (
    load_prompt
)


app = FastAPI(
    title="AI AgentOps & LLM Evaluation Platform",
    description=(
        "LLM evaluation, observability "
        "and prompt monitoring platform"
    ),
    version="2.0.0"
)


class ChatRequest(BaseModel):

    prompt: str

    prompt_version: str = "v1"


@app.get("/")
def home():

    return {
        "message": (
            "AI AgentOps Platform is running"
        ),
        "version": "2.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    start_time = time.perf_counter()

    db = SessionLocal()

    try:

        # --------------------------------
        # 1. Load prompt version
        # --------------------------------

        system_prompt = load_prompt(
            request.prompt_version
        )


        # --------------------------------
        # 2. Build complete prompt
        # --------------------------------

        full_prompt = f"""
{system_prompt}

User question:
{request.prompt}
"""


        # --------------------------------
        # 3. Generate LLM response
        # --------------------------------

        response = generate_response(
            full_prompt
        )


        # --------------------------------
        # 4. Calculate latency
        # --------------------------------

        latency = round(
            time.perf_counter()
            - start_time,
            3
        )


        # --------------------------------
        # 5. Evaluate response
        # --------------------------------

        evaluation = evaluate_response(
            request.prompt,
            response
        )


        # --------------------------------
        # 6. Save evaluation
        # --------------------------------

        log = EvaluationLog(

            prompt=request.prompt,

            response=response,

            model="qwen/qwen3.8-27b",

            prompt_version=(
                request.prompt_version
            ),

            latency_seconds=latency,

            relevance=evaluation[
                "relevance"
            ],

            accuracy=evaluation[
                "accuracy"
            ],

            completeness=evaluation[
                "completeness"
            ],

            clarity=evaluation[
                "clarity"
            ],

            quality_score=evaluation[
                "quality_score"
            ],

            failure=evaluation[
                "failure"
            ],

            failure_reason=evaluation[
                "reason"
            ]
        )


        db.add(log)

        db.commit()

        db.refresh(log)


        # --------------------------------
        # 7. Return response
        # --------------------------------

        return {

            "id": log.id,

            "prompt": request.prompt,

            "prompt_version": (
                request.prompt_version
            ),

            "model": "qwen/qwen3.8-27b",

            "response": response,

            "latency_seconds": latency,

            "evaluation": evaluation,

            "database_status": "saved"
        }


    except Exception as e:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


    finally:

        db.close()