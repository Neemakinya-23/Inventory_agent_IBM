"""
Simple inventory tools for quickmart-inventory-agent.
This module provides JSON-file-backed inventory storage and helper functions for getting and updating stock.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

INVENTORY_FILE = Path("inventory.json")

def _load() -> Dict[str, Any]:
    if not INVENTORY_FILE.exists():
        return {}
    try:
        with INVENTORY_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save(data: Dict[str, Any]) -> None:
    with INVENTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_stock(product_id: str) -> Optional[int]:
    data = _load()
    return data.get(product_id)

def update_stock(product_id: str, delta: int) -> int:
    data = _load()
    current = int(data.get(product_id, 0))
    new = current + delta
    data[product_id] = new
    _save(data)
    return new

def set_stock(product_id: str, amount: int) -> None:
    data = _load()
    data[product_id] = int(amount)
    _save(data)
