# Architecture & code structure: Split the app into main.py (UI), 
# config.py (env/secret loading), 
# api_client.py (HTTP to n8n), 
# and models.py (typed InventoryStatus + payload conversion).
# main.py now uses these layers instead of talking directly to requests.
import json
import logging
import time
import uuid

import streamlit as st

from api_client import send_image_to_n8n
from config import get_webhook_url
from models import inventory_status_from_payload


logging.basicConfig(level=logging.INFO)


st.title("⚙️ V0.2 AI Parts Inspector by Clark")
st.write("Upload a photo of a mechanical component to identify it and check stock.")

env_choice = st.radio("Environment", ["Test", "Production"], horizontal=True)
env_key = "test" if env_choice == "Test" else "prod"

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

identify_button = st.button("Identify Part", disabled=uploaded_file is None)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Component Preview", width=300)

if identify_button and uploaded_file is not None:
    request_id = str(uuid.uuid4())
    try:
        webhook_url = get_webhook_url(env_key)
    except RuntimeError as cfg_err:
        st.error(str(cfg_err))
        logging.error("request_id=%s config_error=%s", request_id, cfg_err)
    else:
        with st.spinner("Transmitting to n8n controller..."):
            start = time.time()
            try:
                response_payload = send_image_to_n8n(
                    webhook_url=webhook_url,
                    filename=uploaded_file.name,
                    content=uploaded_file.getvalue(),
                    mime_type=uploaded_file.type,
                )
                elapsed = time.time() - start

                logging.info(
                    json.dumps(
                        {
                            "event": "analysis_completed",
                            "request_id": request_id,
                            "elapsed_seconds": round(elapsed, 2),
                        }
                    )
                )

                status = inventory_status_from_payload(response_payload)

                st.success("Analysis complete!")
                st.subheader("Inspection Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("Part", status.part_name)
                col2.metric("Stock", status.stock)
                col3.metric("Minimum Threshold", status.min_threshold)

                st.caption(f"System status: {status.status}")

                st.subheader("Raw Inspection Payload")
                st.json(response_payload)

            except Exception as e:  # noqa: BLE001
                logging.exception("request_id=%s analysis_failed", request_id)
                st.error(f"Analysis failed: {e}")