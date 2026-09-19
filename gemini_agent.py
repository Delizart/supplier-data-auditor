
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from supplier_auditor.tools import (
    check_missing_data,
    validate_contacts,
)


# ============================================================
# Configuration
# ============================================================

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# ============================================================
# Tool Registry
# ============================================================

TOOL_REGISTRY = {
    "check_missing_data": check_missing_data,
    "validate_contacts": validate_contacts,
}


# ============================================================
# Gemini Tool Definitions
# ============================================================

missing_data_tool = types.FunctionDeclaration(
    name="check_missing_data",
    description=(
        "Check a supplier Excel file for missing required fields."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the supplier Excel file."
            )
        },
        required=["file_path"],
    ),
)


contact_validation_tool = types.FunctionDeclaration(
    name="validate_contacts",
    description=(
        "Validate supplier email and phone formats "
        "in an Excel supplier database."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the supplier Excel file."
            )
        },
        required=["file_path"],
    ),
)


tool_config = types.Tool(
    function_declarations=[
        missing_data_tool,
        contact_validation_tool,
    ]
)


# ============================================================
# Agent
# ============================================================

def run_agent(file_path: str):

    prompt = f"""
You are a supplier data quality analyst.

Analyze the supplier database located at:

{file_path}

You have access to these tools:

1. check_missing_data
   Detect missing required supplier fields.

2. validate_contacts
   Validate supplier email and phone formats.

Choose the appropriate tools based on the audit request.

For a complete supplier data quality audit, use all relevant tools.

After receiving the tool results, provide a concise audit summary including:

- total number of issues
- affected suppliers
- issue types
- affected fields
- severity
- recommended next actions

Do not invent information that is not present in the tool results.
"""

    # --------------------------------------------------------
    # STEP 1 — Ask Gemini whether a tool is needed
    # --------------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[tool_config]
        ),
    )

    # --------------------------------------------------------
    # STEP 2 — Extract function calls
    # --------------------------------------------------------

    function_calls = []

    for part in response.candidates[0].content.parts:

        if part.function_call:
            function_calls.append(part.function_call)

    # No tool requested
    if not function_calls:

        return response.text

    # --------------------------------------------------------
    # STEP 3 — Execute requested tools
    # --------------------------------------------------------

    print("\n=== TOOL CALLS ===")

    tool_response_parts = []

    for function_call in function_calls:

        tool_name = function_call.name
        arguments = dict(function_call.args)

        print(f"\nTool: {tool_name}")
        print(f"Arguments: {arguments}")

        # ---------------------------------------------
        # Find tool in registry
        # ---------------------------------------------

        if tool_name not in TOOL_REGISTRY:

            raise ValueError(
                f"Unknown tool requested by Gemini: {tool_name}"
            )

        tool_function = TOOL_REGISTRY[tool_name]

        # ---------------------------------------------
        # Execute Python function
        # ---------------------------------------------

        tool_result = tool_function(
            arguments["file_path"]
        )

        print("\nTool result:")
        print(
            json.dumps(
                tool_result,
                indent=2,
                ensure_ascii=False,
            )
        )

        # ---------------------------------------------
        # Prepare response for Gemini
        # ---------------------------------------------

        tool_response_parts.append(
            types.Part.from_function_response(
                name=tool_name,
                response=tool_result,
            )
        )

    # --------------------------------------------------------
    # STEP 4 — Send tool results back to Gemini
    # --------------------------------------------------------

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=prompt
                )
            ],
        ),

        # Gemini's previous function-call message
        response.candidates[0].content,

        # Tool results
        types.Content(
            role="user",
            parts=tool_response_parts,
        ),
    ]

    # --------------------------------------------------------
    # STEP 5 — Ask Gemini for final answer
    # --------------------------------------------------------

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[tool_config]
        ),
    )

    return final_response.text


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    file_path = (
        "data/input/suppliers_sample.xlsx"
    )

    result = run_agent(file_path)

    print("\n")
    print("=" * 60)
    print("FINAL AGENT RESPONSE")
    print("=" * 60)
    print(result)
