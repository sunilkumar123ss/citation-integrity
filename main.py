"""Check citation references and literal quotations, not semantic truth."""
import argparse
import json
from pathlib import Path


def normalize(text):
    return " ".join(text.casefold().split())

