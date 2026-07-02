from pathlib import Path
import json

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Catalog file location
CATALOG_PATH = PROJECT_ROOT / "data" / "raw" / "shl_product_catalog.json"

def load_catalog():
    """
    Loads the SHL product catalog JSON.
    Returns:
        list: List of assessment dictionaries.
    """
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    return catalog