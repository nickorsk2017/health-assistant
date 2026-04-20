from xml.etree import ElementTree

import httpx
from loguru import logger

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


class PubMedClient:
    def __init__(self, api_key: str = "", max_results: int = 5) -> None:
        self._api_key = api_key
        self._max_results = max_results

    def _base_params(self) -> dict:
        params: dict = {"db": "pubmed"}
        if self._api_key:
            params["api_key"] = self._api_key
        return params

    async def search(self, query: str) -> list[str]:
        params = {
            **self._base_params(),
            "term": query,
            "retmax": self._max_results,
            "retmode": "json",
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(ESEARCH_URL, params=params)
                response.raise_for_status()
            pmids: list[str] = response.json()["esearchresult"]["idlist"]
            logger.info(f"PubMed search '{query[:60]}' → {len(pmids)} result(s)")
            return pmids
        except Exception as exc:
            logger.error(f"PubMed search failed for '{query[:60]}': {exc}")
            return []

    async def fetch_abstracts(self, pmids: list[str]) -> list[dict]:
        if not pmids:
            return []
        params = {
            **self._base_params(),
            "id": ",".join(pmids),
            "rettype": "abstract",
            "retmode": "xml",
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(EFETCH_URL, params=params)
                response.raise_for_status()
            return _parse_abstracts(response.text)
        except Exception as exc:
            logger.error(f"PubMed fetch failed for PMIDs {pmids}: {exc}")
            return []


def _parse_abstracts(xml_text: str) -> list[dict]:
    root = ElementTree.fromstring(xml_text)
    results: list[dict] = []
    for article in root.findall(".//PubmedArticle"):
        pmid_el = article.find(".//PMID")
        title_el = article.find(".//ArticleTitle")
        abstract_el = article.find(".//AbstractText")
        results.append({
            "pmid": pmid_el.text if pmid_el is not None else "",
            "title": title_el.text if title_el is not None else "",
            "abstract": abstract_el.text if abstract_el is not None else "",
        })
    return results
