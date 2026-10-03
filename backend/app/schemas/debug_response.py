from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ErrorDetails(BaseModel):
    type: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None


class Hypothesis(BaseModel):
    rank: int
    cause: str
    confidence: str
    evidence: str


class FixEntry(BaseModel):
    file: str
    original_code: str
    fixed_code: str


class TestCase(BaseModel):
    name: str
    code: str


class DebugResponse(BaseModel):
    error: ErrorDetails
    root_cause: str
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    fixes: List[FixEntry] = Field(default_factory=list)
    tests: List[TestCase] = Field(default_factory=list)
    verification: Optional[dict[str, Any]] = None
