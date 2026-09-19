import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from supplier_auditor.tools import check_missing_data


load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def run_agent(file_path: str):

    tool = types.FunctionDeclaration(
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

    tool_config = types.Tool(
        function_declarations=[tool]
    )

    prompt = f"""
You are a supplier data quality analyst.

Analyze the supplier database located at:

{file_path}

Use the check_missing_data tool to detect missing required fields.

After receiving the tool result, provide a concise audit summary including:
- total number of issues
- affected suppliers
- missing fields
- recommended next action
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[tool_config]
        ),
    )

    # -------------------------------------------------
    # STEP 1: Check whether Gemini requested a tool
    # -------------------------------------------------

    function_call = None

    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call = part.function_call
            break

    if not function_call:
        return response.text

    print("\n=== TOOL CALL ===")
    print("Tool:", function_call.name)
    print("Arguments:", function_call.args)

    # -------------------------------------------------
    # STEP 2: Execute the requested Python function
    # -------------------------------------------------

    if function_call.name == "check_missing_data":

        tool_result = check_missing_data(
            function_call.args["file_path"]
        )

    else:
        raise ValueError(
            f"Unknown tool: {function_call.name}"
        )

    print("\n=== TOOL RESULT ===")
    print(json.dumps(tool_result, indent=2))

    # -------------------------------------------------
    # STEP 3: Send the result back to Gemini
    # -------------------------------------------------

    tool_response_part = types.Part.from_function_response(
        name=function_call.name,
        response=tool_result,
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ],
        ),
        response.candidates[0].content,
        types.Content(
            role="user",
            parts=[tool_response_part],
        ),
    ]

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[tool_config]
        ),
    )

    return final_response.text


if __name__ == "__main__":

    result = run_agent(
        "data/input/suppliers_sample.xlsx"
    )

    print("\n=== FINAL AGENT RESPONSE ===")
    print(result)