from supplier_auditor.tools import (
    check_missing_data,
    validate_contacts,
)

file_path = "data/input/suppliers_sample.xlsx"


print("\n=== MISSING DATA ===")

result = check_missing_data(file_path)

print("Total issues:", result["total_issues"])


print("\n=== CONTACT VALIDATION ===")

result = validate_contacts(file_path)

print("Total issues:", result["total_issues"])

for issue in result["issues"]:
    print(issue)