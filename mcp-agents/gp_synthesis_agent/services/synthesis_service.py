from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from config import settings
from schemas.consultation import GPConsultation

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "gp_synthesis.md"


def _load_system_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _format_findings(findings: list[dict]) -> str:
    lines: list[str] = [
        f"## Consilium Report — {len(findings)} Specialist Finding(s)\n"
    ]
    for i, finding in enumerate(findings, start=1):
        specialty = finding.get("specialty", "unknown").replace("_", " ").title()
        lines.append(f"### [{i}] {specialty}")
        lines.append(f"**Probable Diagnosis:** {finding.get('probable_diagnosis', 'N/A')}")
        lines.append(f"**Risks:** {finding.get('risks', 'N/A')}")
        lines.append(f"**Recommended Treatment:** {finding.get('treatment', 'N/A')}")
        lines.append(f"**Prognosis:** {finding.get('prognosis', 'N/A')}")
        lines.append("")
    return "\n".join(lines)


class SynthesisService:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
        )

    async def synthesize(self, findings: list[dict]) -> GPConsultation:
        findings_text = _format_findings(findings)
        logger.info(f"Sending {len(findings)} specialist findings to GP synthesis LLM...")

        structured_llm = self._llm.with_structured_output(GPConsultation)
        consultation: GPConsultation = await structured_llm.ainvoke(
            [
                SystemMessage(content=_load_system_prompt()),
                HumanMessage(content=findings_text),
            ]
        )

        logger.info("GP synthesis complete.")
        return consultation
