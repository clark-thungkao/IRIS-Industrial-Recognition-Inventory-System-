from dataclasses import dataclass
from typing import Literal

Status = Literal["OK", "LOW", "CRITICAL", "UNKNOWN"]


@dataclass
class InventoryStatus:
    part_name: str
    stock: int
    min_threshold: int
    status: Status


def inventory_status_from_payload(payload: dict) -> InventoryStatus:
    """
    Convert a raw JSON payload from n8n into a strongly-typed InventoryStatus.
    Falls back to safe defaults when fields are missing.
    """
    part_name = str(payload.get("part_name", "Unknown"))

    def _to_int(key: str) -> int:
        try:
            return int(payload.get(key, 0))
        except (TypeError, ValueError):
            return 0

    stock = _to_int("stock")
    min_threshold = _to_int("min_threshold")

    raw_status = str(payload.get("status", "UNKNOWN")).upper()
    if raw_status not in {"OK", "LOW", "CRITICAL", "UNKNOWN"}:
        raw_status = "UNKNOWN"

    return InventoryStatus(
        part_name=part_name,
        stock=stock,
        min_threshold=min_threshold,
        status=raw_status,  # type: ignore[arg-type]
    )

