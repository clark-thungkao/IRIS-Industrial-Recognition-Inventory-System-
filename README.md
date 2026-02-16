# AI Technical Inventory Manager
## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-FF6D5A?style=for-the-badge&logo=n8n&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
## Overview
An automated, AI-driven inventory inspection system designed for industrial and mechatronic components. This project replaces manual stock logging with a computer vision pipeline. A Streamlit frontend allows technicians to capture component images, which are processed by an n8n orchestration backend. GPT-4o identifies the specific part against an authorized database, checks stock levels, and flags low-inventory items in real-time.

## Architecture
The system follows a decoupled frontend/backend structure, adhering to standard systems engineering principles:

* **Frontend (HMI):** Streamlit (Python). Transmits binary image data via a `multipart/form-data` POST request.
* **Orchestration (Logic Controller):** n8n. Handles routing, data extraction, and conditional logic.
* **Cognitive Engine:** OpenAI API (GPT-4o).
* **Database:** Google Sheets.

## Repository Structure
```text
/
├── app/
│   ├── main.py              # Streamlit user interface
│   └── requirements.txt     # Python dependencies (streamlit, requests)
├── workflows/
│   └── inventory_flow.json  # Exported n8n workflow code
├── .gitignore               # Excludes virtual environments and keys
└── README.md
```

## System Logic (n8n Pipeline)
The workflow operates sequentially to process the image and evaluate stock levels:

1. **Webhook Trigger:** Listens for POST requests from the Python app.
2. **Database Pull (Grounding):** Retrieves the list of authorized part names (e.g., "ATmega328P-PU Microcontroller") from Google Sheets.
3. **List Formatting:** Aggregates the part names into a single string.
4. **AI Analysis (GPT-4o):** Evaluates the binary image (`data0`). The prompt forces the AI to select the part strictly from the provided database list to ensure 100% database matching.
5. **JSON Parser:** Extracts the `part_name` from the AI's markdown text output into usable data fields.
6. **Database Query:** Searches Google Sheets for the exact part name to retrieve the current Stock and Minimum Threshold.
7. **Conditional Logic (If Node):** Evaluates if Stock < Minimum Threshold.
8. **Actuator (Respond to Webhook):** Returns a structured JSON payload (Normal or Warning) back to the Streamlit UI.

## Technical Configuration Notes
Based on system testing, the following specific configurations are required for the workflow to function correctly:

* **Webhook Response Routing:** The Webhook trigger node must have its Respond setting configured to Using 'Respond to Webhook' node. If set to When Last Node Finishes or Immediately, it creates a conflict with the branching logic and throws a 500 Error.
* **Binary Data Mapping:** When the Python requests library sends a file named `data`, n8n parses it as an indexed binary object. The OpenAI node must be configured to look for the Input Data Field Name `data0`.
* **AI Model Selection:** GPT-4o must be used over GPT-4o-mini. The mini model lacks the visual reasoning depth required to distinguish highly specific industrial components from generic guesses.

## Setup & Deployment

### Backend (n8n)
1. Import `inventory_flow.json` into  n8n instance.
2. Connect  Google Sheets and OpenAI API credentials.
3. Activate the workflow and copy  Webhook URL (Test or Production).

### Frontend (Streamlit)
1. Navigate to the `app/` directory.
2. Create and activate a virtual environment.
3. Run `pip install -r requirements.txt`.
4. Update the `WEBHOOK_URL` variable in `main.py` with the n8n endpoint.
5. Run the application using `streamlit run main.py`.
