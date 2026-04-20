from pydantic import BaseModel, Field


class ClinicalContext(BaseModel):
    history_records: list[dict] = Field(default_factory=list)
    lab_records: list[dict] = Field(default_factory=list)
    complaint_records: list[dict] = Field(default_factory=list)
    device_records: list[dict] = Field(default_factory=list)


class ValidationRequest(BaseModel):
    keywords_diagnosis: list[str] = Field(
        description="Medical keyword variants of the suspected diagnosis for PubMed search."
    )
    clinical_context: ClinicalContext = Field(
        description="Patient clinical data used to score abstract relevance."
    )


class ValidationResponse(BaseModel):
    validation_score: int = Field(description="Evidence match score (0-100).")
    citations: list[str] = Field(description="PubMed IDs (e.g. 'PMID:12345678').")
    summary: str = Field(description="Scientific justification for the score.")
