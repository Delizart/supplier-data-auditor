from supplier_auditor.llm.client import explain_issue


result = explain_issue(
    issue_type="INVALID_EMAIL",
    field="email",
    severity="MEDIUM",
    details="Invalid email format: contact@invalid",
)

print("\n=== GEMINI RESULT ===")
print("Explanation:", result.explanation)
print("Recommendation:", result.recommendation)
print("Priority:", result.priority)