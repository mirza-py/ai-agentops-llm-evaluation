import json
import re
from typing import Dict, Any

from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


JUDGE_MODEL = "qwen/qwen3.8-27b"


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON object from an LLM response.
    """

    text = text.strip()

    # Direct JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # JSON inside markdown code block
    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Find first JSON object
    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from evaluator response.")


def llm_judge(
    question: str,
    answer: str
) -> Dict[str, Any]:
    """
    Evaluate an LLM response using another LLM as a judge.
    """

    evaluation_prompt = f"""
You are an expert LLM evaluation system.

Evaluate the following AI response.

USER QUESTION:
{question}

AI RESPONSE:
{answer}

Evaluate the response using these criteria:

1. relevance:
How directly does the response answer the question?
Score from 0 to 10.

2. accuracy:
How factually correct is the response?
Score from 0 to 10.

3. completeness:
Does the response adequately cover the question?
Score from 0 to 10.

4. clarity:
Is the response clear and understandable?
Score from 0 to 10.

5. overall_score:
Give an overall quality score from 0 to 10.

6. failure:
Set true if the response is empty, refuses unnecessarily,
is clearly incorrect, or has a serious problem.
Otherwise false.

7. feedback:
Give a short explanation of the evaluation.

Return ONLY valid JSON.

Required format:

{{
    "relevance": 0,
    "accuracy": 0,
    "completeness": 0,
    "clarity": 0,
    "overall_score": 0,
    "failure": false,
    "feedback": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON-only evaluation engine."
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0
    )

    raw_result = response.choices[0].message.content

    result = extract_json(raw_result)

    return {
        "relevance": float(result.get("relevance", 0)),
        "accuracy": float(result.get("accuracy", 0)),
        "completeness": float(result.get("completeness", 0)),
        "clarity": float(result.get("clarity", 0)),
        "quality_score": float(result.get("overall_score", 0)),
        "failure": bool(result.get("failure", False)),
        "reason": result.get(
            "feedback",
            "No feedback available."
        )
    }


def evaluate_response(
    prompt: str,
    response: str
) -> Dict[str, Any]:
    """
    Main evaluation function.
    """

    # Basic failure check before calling judge
    if not response or not response.strip():

        return {
            "relevance": 0,
            "accuracy": 0,
            "completeness": 0,
            "clarity": 0,
            "quality_score": 0,
            "failure": True,
            "reason": "LLM returned an empty response."
        }

    try:

        evaluation = llm_judge(
            prompt,
            response
        )

        return evaluation

    except Exception as e:

        # Evaluation failure should not crash the main LLM response
        return {
            "relevance": 0,
            "accuracy": 0,
            "completeness": 0,
            "clarity": 0,
            "quality_score": 0,
            "failure": True,
            "reason": f"Evaluation failed: {str(e)}"
        }