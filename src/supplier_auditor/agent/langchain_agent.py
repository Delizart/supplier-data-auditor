import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from supplier_auditor.tools import (
    check_missing_data,
    validate_contacts,
)

load_dotenv()


# ============================================================
# 1. TOOLS
# ============================================================

@tool
def check_supplier_missing_data(file_path: str) -> dict:
    """
    Check a supplier Excel file for missing required fields.
    """
    return check_missing_data(file_path)


@tool
def validate_supplier_contacts(file_path: str) -> dict:
    """
    Validate supplier email and phone formats.
    """
    return validate_contacts(file_path)


# ============================================================
# 2. GEMINI
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
)


# ============================================================
# 3. TOOLS AVAILABLE TO GEMINI
# ============================================================

tools = [
    check_supplier_missing_data,
    validate_supplier_contacts,
]

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 4. TOOL REGISTRY
# ============================================================

tool_registry = {
    check_supplier_missing_data.name: check_supplier_missing_data,
    validate_supplier_contacts.name: validate_supplier_contacts,
}


# ============================================================
# 5. AGENT LOOP
# ============================================================

def run_agent(file_path: str):

    prompt = f"""
You are a Supplier Data Quality Auditor.

Analyze the supplier database:

{file_path}

Your objective is to identify data quality issues.

You have two tools available:

1. check_supplier_missing_data
   - Detects missing required supplier fields.

2. validate_supplier_contacts
   - Detects invalid email and phone formats.

Use the appropriate tools to perform a complete audit.

After receiving the tool results, provide a concise business-oriented
summary of the detected issues.

Include:
- total number of issues
- issue types
- affected suppliers
- severity
- recommended actions
"""

    messages = [
        ("user", prompt)
    ]

    # --------------------------------------------------------
    # Agent loop
    # --------------------------------------------------------

    while True:

        response = llm_with_tools.invoke(messages)

        print("\n=== LLM RESPONSE ===")
        print(response)

        # Add model response to conversation
        messages.append(response)

        # ----------------------------------------------------
        # No tool call = final answer
        # ----------------------------------------------------

        if not response.tool_calls:
            return response.content

        # ----------------------------------------------------
        # Execute requested tools
        # ----------------------------------------------------

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print("\n=== TOOL CALL ===")
            print(f"Tool: {tool_name}")
            print(f"Arguments: {tool_args}")

            tool_function = tool_registry.get(tool_name)

            if tool_function is None:
                raise ValueError(
                    f"Unknown tool requested: {tool_name}"
                )

            result = tool_function.invoke(tool_args)

            print("\n=== TOOL RESULT ===")
            print(result)

            # ------------------------------------------------
            # Send tool result back to Gemini
            # ------------------------------------------------

            from langchain_core.messages import ToolMessage

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )


# ============================================================
# 6. MAIN
# ============================================================

if __name__ == "__main__":

    file_path = "data/input/suppliers_sample.xlsx"

    final_result = run_agent(file_path)

    print("\n")
    print("=" * 60)
    print("FINAL AGENT RESPONSE")
    print("=" * 60)
    print(final_result)