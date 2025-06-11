from nlp.parser import fallback_parser
from nlp.semantic_parser_ai import semantic_parse_ai
from config.settings import TEST_APP

# Mappature da AI/fallback verso moduli Python reali
DOMAIN_MAPPING = {
    "risorse umane": "hr",
    "vendite": "sales",
    "e-commerce": "ecommerce",
    "prodotti": "ecommerce"
}

INTENT_MAPPING = {
    "visualizzare reparto con più turnover": "turnover_per_department",
    "visualizzare": "show_sales_by_store",
    "ottenere_prodotti_piu_acquistati": "top_purchased_products"
}

def normalize(intent_dict: dict) -> dict:
    domain = intent_dict.get("domain", "").strip().lower()
    intent = intent_dict.get("intent", "").strip().lower()
    filters = intent_dict.get("filters", {})

    domain = DOMAIN_MAPPING.get(domain, domain)
    intent = INTENT_MAPPING.get(intent, intent)

    return {
        "domain": domain,
        "intent": intent,
        "filters": filters
    }

def normalize_ai (intent_dict: dict) -> dict:
    domain = intent_dict.get("domain", "").strip().lower()
    intent = intent_dict.get("intent", "").strip().lower()
    filters = intent_dict.get("filters", {})
    return {
            "domain": domain,
            "intent": intent,
            "filters": filters
        }


def parse_question(text: str) -> dict:
    if TEST_APP:
        raw = fallback_parser(text)
        return normalize(raw)
    else:
        raw = semantic_parse_ai(text)
        return normalize_ai(raw)
