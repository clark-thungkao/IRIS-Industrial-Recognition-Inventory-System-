import os
from functools import lru_cache

import streamlit as st


@lru_cache(maxsize=1)
def get_webhook_url(env: str = "prod") -> str:
    """
    Resolve the n8n webhook URL from Streamlit secrets or environment variables.

    Priority:
    1. Streamlit secrets (for Streamlit Cloud / local secrets.toml)
    2. Environment variables
    """
    env_key = "https://germancapybara.app.n8n.cloud/webhook-test/4bdb11b9-6f5c-449e-a90c-d5bc77b23635" if env == "prod" else "https://germancapybara.app.n8n.cloud/webhook-test/4bdb11b9-6f5c-449e-a90c-d5bc77b23635"

    # 1) Streamlit secrets
    value = st.secrets.get(env_key) if hasattr(st, "secrets") else None

    # 2) Fall back to environment variables
    if not value:
        value = os.getenv(env_key)

    if not value:
        raise RuntimeError(
            f"{env_key} is not configured. "
            "Set it in .streamlit/secrets.toml or as an environment variable."
        )

    return value

