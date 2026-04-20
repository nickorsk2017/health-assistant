from pydantic import BaseModel, ConfigDict, Field


class GPConsultation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    diagnosis: str = Field(
        description=(
            "A concise, definitive clinical diagnosis (1-2 sentences). "
            "Name the primary condition and its direct consequences."
        )
    )
    treatment: str = Field(
        description=(
            "A prioritized, numbered step-by-step treatment plan. "
            "Order by clinical urgency. Each step must be actionable and specific."
        )
    )
    prognosis: str = Field(
        description=(
            "A realistic, honest clinical outlook after the proposed treatment (2-3 sentences). "
            "Include expected timeline for improvement and any long-term monitoring needs."
        )
    )
    summary: str = Field(
        description=(
            "A 5-10 sentence narrative titled 'The Story of Your Health'. "
            "Written in clear, empathetic language for the patient — free of unexplained jargon. "
            "Explain how seemingly unrelated symptoms across different specialists are all connected, "
            "why the diagnosis was initially missed, and why the chosen treatment plan gives the best outcome."
        )
    )
    keywords_diagnosis: list[str] = Field(
        default_factory=list,
        description=(
            "2-3 specific medical keyword variants of the primary diagnosis for PubMed search. "
            "Include the canonical name and clinically distinct subtypes. "
            "Example: ['Pheochromocytoma', 'Adrenal Paraganglioma', 'Catecholamine-secreting tumor']."
        ),
    )
