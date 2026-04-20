from pydantic import Field

from _common.schemas.gp_consultation import GPConsultation


class DiagnosisResult(GPConsultation):
    validation_percentage: int = Field(
        default=0,
        description="Evidence match score (0-100) based on PubMed literature correlation.",
    )
    evidence_citations: list[str] = Field(
        default_factory=list,
        description="PubMed IDs (e.g. 'PMID:12345678') supporting the diagnosis.",
    )
    validation_summary: str = Field(
        default="",
        description="Scientific justification for the validation score from PubMed analysis.",
    )
