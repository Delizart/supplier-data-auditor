from pydantic import BaseModel, Field


class IssueExplanation(BaseModel):
    explanation: str = Field(
        description="Clear explanation of the detected supplier data issue."
    )
    recommendation: str = Field(
        description="Recommended action to resolve the issue."
    )
    priority: str = Field(
        description="Action priority: LOW, MEDIUM, or HIGH."
    )