import re
import logging

logger = logging.getLogger(__name__)


def fallback_parser(text: str) -> dict:
    text = text.lower()
    year = extract_year(text)

    domain = "unknown"
    intent = "unknown"
    filters = {}

    if "turnover" in text or "abbandono" in text:
        domain = "hr"
        intent = "turnover_per_department"

    elif "vendite" in text or "negozi" in text:
        domain = "sales"
        intent = "show_sales_by_store"
        if year:
            filters["year"] = year

    elif "prodotti" in text or "acquistati" in text:
        domain = "ecommerce"
        intent = "top_purchased_products"

    return {
        "domain": domain,
        "intent": intent,
        "filters": filters
    }
def extract_year(text: str):
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return int(match.group()) if match else None
