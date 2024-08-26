"""Check citation references and literal quotations, not semantic truth."""
import argparse
import json
from pathlib import Path


def normalize(text):
    return " ".join(text.casefold().split())


def audit(claims, sources):
    if not isinstance(sources, dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in sources.items()):
        raise ValueError("sources must map string IDs to source text")
    if not isinstance(claims, list):
        raise ValueError("claims must be a list")
    results = []
    for claim in claims:
        if not isinstance(claim, dict) or not isinstance(claim.get("text"), str):
            raise ValueError("every claim needs text")
        citations = claim.get("citations", [])
        if not isinstance(citations, list):
            raise ValueError("citations must be a list")
        failures = []
        if not citations:
            failures.append("missing_citations")
        for number, citation in enumerate(citations, 1):
            if not isinstance(citation, dict):
                failures.append(f"citation_{number}:invalid_shape")
                continue
            source_id, quote = citation.get("source_id"), citation.get("quote")
            if not isinstance(source_id, str) or source_id not in sources:
                failures.append(f"citation_{number}:unknown_source")
            elif not isinstance(quote, str) or not normalize(quote):
                failures.append(f"citation_{number}:empty_quote")
            elif normalize(quote) not in normalize(sources[source_id]):
                failures.append(f"citation_{number}:quote_not_found")
        results.append({"claim": claim["text"],
                        "status": "citation_integrity_failed" if failures else "quoted_evidence_found",
                        "failures": failures,
                        "semantic_entailment_checked": False})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("claims.json"))
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        results = audit(data["claims"], data["sources"])
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(results, indent=2))

if __name__ == "__main__": main()
