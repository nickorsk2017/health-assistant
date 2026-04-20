from loguru import logger

from config import settings
from schemas.http import ClinicalContext, ValidationResponse
from services.cache import PubMedCache
from services.pubmed_client import PubMedClient

_STOPWORDS = {"with", "from", "this", "that", "have", "been", "were", "their", "there"}


def _extract_clinical_terms(ctx: ClinicalContext) -> list[str]:
    raw: list[str] = []
    for r in ctx.complaint_records:
        raw.extend(r.get("problem_health", "").lower().split())
    for r in ctx.lab_records:
        raw.extend((r.get("analysis_text", "") or "").lower().split())
    for r in ctx.history_records:
        for field in ("assessment", "subjective", "chief_complaint"):
            raw.extend(r.get(field, "").lower().split())
    return [t.strip(".,;:()") for t in raw if len(t) > 4 and t not in _STOPWORDS]


def _compute_score(abstracts: list[dict], terms: list[str]) -> int:
    if not abstracts:
        return 0
    if not terms:
        return min(len(abstracts) * 12, 50)
    scores: list[float] = []
    for item in abstracts:
        text = (item.get("abstract", "") + " " + item.get("title", "")).lower()
        matched = sum(1 for t in terms if t in text)
        scores.append(matched / len(terms))
    paper_coverage = min(len(abstracts) / settings.pubmed_max_results, 1.0)
    term_match = sum(scores) / len(scores)
    return min(int((0.4 * paper_coverage + 0.6 * term_match) * 100), 100)


def _build_summary(score: int, keywords: list[str], abstracts: list[dict]) -> str:
    keyword_str = ", ".join(f'"{k}"' for k in keywords)
    if not abstracts:
        return (
            f"PubMed returned no results for {keyword_str} with the given clinical context. "
            "The score reflects diagnostic uncertainty due to absent literature evidence."
        )
    titles = "; ".join(a["title"] for a in abstracts[:3] if a.get("title"))
    confidence = "strong" if score >= 70 else "moderate" if score >= 45 else "limited"
    return (
        f"PubMed analysis for {keyword_str} found {len(abstracts)} relevant article(s). "
        f"Clinical term matching against patient context yields {confidence} evidence support "
        f"(score: {score}/100). Representative publications: {titles}."
    )


class ValidationService:
    def __init__(self) -> None:
        self._pubmed = PubMedClient(
            api_key=settings.ncbi_api_key,
            max_results=settings.pubmed_max_results,
        )
        self._cache = PubMedCache(ttl_seconds=settings.cache_ttl_seconds)

    async def validate(
        self,
        keywords: list[str],
        clinical_context: ClinicalContext,
    ) -> ValidationResponse:
        clinical_terms = _extract_clinical_terms(clinical_context)
        logger.info(
            f"Validating {len(keywords)} keyword(s) against "
            f"{len(clinical_terms)} clinical term(s)"
        )

        all_pmids: set[str] = set()
        top_terms = clinical_terms[:5]

        for keyword in keywords:
            query = f"{keyword} {' '.join(top_terms)}" if top_terms else keyword
            cached = await self._cache.get(query)
            if cached is not None:
                logger.info(f"Cache hit for query: '{query[:60]}'")
                pmids: list[str] = cached
            else:
                pmids = await self._pubmed.search(query)
                await self._cache.set(query, pmids)
            all_pmids.update(pmids)

        if not all_pmids:
            return ValidationResponse(
                validation_score=0,
                citations=[],
                summary=_build_summary(0, keywords, []),
            )

        abstracts = await self._pubmed.fetch_abstracts(list(all_pmids))
        score = _compute_score(abstracts, clinical_terms)
        citations = [f"PMID:{a['pmid']}" for a in abstracts if a.get("pmid")]
        summary = _build_summary(score, keywords, abstracts)

        logger.info(f"Validation complete: score={score}, citations={len(citations)}")
        return ValidationResponse(
            validation_score=score,
            citations=citations,
            summary=summary,
        )
