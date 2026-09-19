from supplier_auditor.tools import check_missing_data


result = check_missing_data(
    "data/input/suppliers_sample.xlsx"
)

print("\n=== TOOL RESULT ===")
print("Total issues:", result["total_issues"])

for issue in result["issues"]:
    print(issue)