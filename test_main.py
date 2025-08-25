import unittest
# Load this project's module explicitly, including when invoked from repository root.
import importlib.util as _import_util
from pathlib import Path as _Path
import sys as _sys
_spec = _import_util.spec_from_file_location(
    "sunil_agents_" + _Path(__file__).parent.name, _Path(__file__).with_name("main.py"))
_main = _import_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _main
_spec.loader.exec_module(_main)
audit = _main.audit

class CitationTests(unittest.TestCase):
    def test_whitespace_normalized_quote_is_found(self):
        result = audit([{"text":"claim","citations":[{"source_id":"s","quote":"SEVEN days"}]}], {"s":"Keep for seven\n days."})[0]
        self.assertEqual(result["status"], "quoted_evidence_found")
        self.assertFalse(result["semantic_entailment_checked"])
    def test_unknown_source_invented_quote_and_missing(self):
        claims = [{"text":"x"},{"text":"y","citations":[{"source_id":"bad","quote":"a"}]},
                  {"text":"z","citations":[{"source_id":"s","quote":"invented"}]}]
        results = audit(claims, {"s":"real source"})
        self.assertTrue(all(r["status"] == "citation_integrity_failed" for r in results))
    def test_empty_quote_fails(self):
        result = audit([{"text":"x","citations":[{"source_id":"s","quote":" "}]}], {"s":"real"})
        self.assertIn("empty_quote", result[0]["failures"][0])
    def test_quote_integrity_does_not_imply_claim_truth(self):
        result = audit([{"text":"The service is guaranteed never to fail.", "citations":[{"source_id":"s", "quote":"seven days"}]}], {"s":"Snapshots last seven days."})[0]
        self.assertEqual(result["status"], "quoted_evidence_found")
        self.assertFalse(result["semantic_entailment_checked"])

