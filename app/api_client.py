from typing import Any, Dict

import requests


def send_image_to_n8n(
    webhook_url: str,
    filename: str,
    content: bytes,
    mime_type: str,
    timeout_seconds: int = 20,
) -> Dict[str, Any]:
    """
    Send an image to the n8n webhook and return the parsed JSON response.

    This function encapsulates the HTTP layer so it can be easily unit tested
    and swapped out in the future if the backend changes.
    """
    files = {"data": (filename, content, mime_type)}
    response = requests.post(webhook_url, files=files, timeout=timeout_seconds)
    response.raise_for_status()

    try:
        return response.json()
    except Exception as exc:  # noqa: BLE001
        # Surface a clearer error when n8n does not return JSON
        snippet = response.text[:300] if response.text else "<empty body>"
        raise RuntimeError(
            f"Backend did not return JSON (status {response.status_code}). "
            f"Body preview: {snippet}"
        ) from exc


