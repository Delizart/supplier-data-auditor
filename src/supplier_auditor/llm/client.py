import os

from dotenv import load_dotenv
from google import genai

from .models import IssueExplanation


load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def explain_issue(
    issue_type: str,
    field: str,
    severity: str,
    details: str,
) -> IssueExplanation:

    prompt = f"""
You are a supplier data quality analyst.

Analyze the following detected issue.

Issue type: {issue_type}
Field: {field}
Severity: {severity}
Details: {details}

Explain the issue clearly.
Recommend a practical corrective action.
Do not invent facts that are not present in the issue.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": IssueExplanation.model_json_schema(),
        },
    )

    return IssueExplanation.model_validate_json(
        interaction.output_text
    )