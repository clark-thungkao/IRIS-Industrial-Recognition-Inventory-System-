import os
from functools import lru_cache

import streamlit as st


@lru_cache(maxsize=1)
def get_webhook_url(env: str = "prod") -> str:
    """
    Resolve the n8n webhook URL from environment variables or Streamlit secrets.

    Priority:
    1. Environment variables (for local/dev and Docker)
    2. Streamlit secrets (for Streamlit Cloud / local secrets.toml)
    """
    env_key = "WEBHOOK_URL_PROD" if env == "prod" else "WEBHOOK_URL_TEST"

    # 1) Environment variables
    value = os.getenv(env_key)

    # 2) Fall back to Streamlit secrets (handle missing secrets.toml gracefully)
    if not value:
        try:
            value = st.secrets[env_key]  # type: ignore[index]
        except Exception:  # noqa: BLE001
            value = None

    if not value:
        raise RuntimeError(
            f"{env_key} is not configured. "
            "Set it in .streamlit/secrets.toml or as an environment variable."
        )

    return value

