## AI Technical Inventory Manager
Overview
An automated, AI-driven inventory inspection system designed for industrial and mechatronic components. This project replaces manual stock logging with a computer vision pipeline. A Streamlit frontend allows technicians to capture component images, which are processed by an n8n orchestration backend. GPT-4o identifies the specific part against an authorized database, checks stock levels, and flags low-inventory items in real-time.
## Architecture
The system follows a decoupled frontend/backend structure, adhering to standard systems engineering principles:

Frontend (HMI): Streamlit (Python). Transmits binary image data via a multipart/form-data POST request.

Orchestration (Logic Controller): n8n. Handles routing, data extraction, and conditional logic.

Cognitive Engine: OpenAI API (GPT-4o).

Database: Google Sheets.

## System Logic (n8n Pipeline)
The workflow operates sequentially to process the image and evaluate stock levels:

Webhook Trigger: Listens for POST requests from the Python app.

Database Pull (Grounding): Retrieves the list of authorized part names (e.g., "ATmega328P-PU Microcontroller") from Google Sheets.

List Formatting: Aggregates the part names into a single string.

AI Analysis (GPT-4o): Evaluates the binary image (data0). The prompt forces the AI to select the part strictly from the provided database list to ensure 100% database matching.

JSON Parser: Extracts the part_name from the AI's markdown text output into usable data fields.

Database Query: Searches Google Sheets for the exact part name to retrieve the current Stock and Minimum Threshold.

Conditional Logic (If Node): Evaluates if Stock < Minimum Threshold.

Actuator (Respond to Webhook): Returns a structured JSON payload (Normal or Warning) back to the Streamlit UI.

## Technical Configuration Notes
Based on system testing, the following specific configurations are required for the workflow to function correctly:

Webhook Response Routing: The Webhook trigger node must have its Respond setting configured to Using 'Respond to Webhook' node. If set to When Last Node Finishes or Immediately, it creates a conflict with the branching logic and throws a 500 Error.

Binary Data Mapping: When the Python requests library sends a file named data, n8n parses it as an indexed binary object. The OpenAI node must be configured to look for the Input Data Field Name data0.

AI Model Selection: GPT-4o must be used over GPT-4o-mini. The mini model lacks the visual reasoning depth required to distinguish highly specific industrial components from generic guesses.

## Setup & Deployment
#Backend (n8n)
Import inventory_flow.json into your n8n instance.

Connect your Google Sheets and OpenAI API credentials.

Activate the workflow and copy your Webhook URL (Test or Production).

#Frontend (Streamlit)
Navigate to the app/ directory.

Create and activate a virtual environment.

Run pip install -r requirements.txt.

Update the WEBHOOK_URL variable in main.py with your n8n endpoint.

Run the application using streamlit run main.py.
