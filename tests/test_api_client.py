# Testing & CI: Added a tests/test_api_client.py 
# using pytest + requests-mock, 
# and a GitHub Actions workflow (.github/workflows/ci.yml) that installs deps and runs pytest on every push/PR.
from app.api_client import send_image_to_n8n


def test_send_image_to_n8n_success(requests_mock):
    url = "https://example.com/webhook"
    expected = {"part_name": "ATmega328P-PU", "stock": 4}
    requests_mock.post(url, json=expected, status_code=200)

    result = send_image_to_n8n(url, "test.png", b"data", "image/png")

    assert result == expected
