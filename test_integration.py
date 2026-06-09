"""Integration tests for Voice Call Center AI"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def client_fixture():
    return TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check_structure():
    """Test health check response structure"""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "active_calls" in data


def test_incoming_call():
    """Test incoming call endpoint"""
    response = client.post(
        "/incoming-call",
        data={
            "CallSid": "CA1234567890abcdef",
            "From": "+16175551212",
            "To": "+16175551313",
            "CallStatus": "ringing",
        }
    )
    assert response.status_code == 200
    assert "Response" in response.text


def test_get_calls():
    """Test get calls endpoint"""
    response = client.get("/calls")
    assert response.status_code == 200
    data = response.json()
    assert "active_calls" in data
    assert "calls" in data


def test_call_details_not_found():
    """Test getting non-existent call"""
    response = client.get("/calls/NONEXISTENT")
    assert response.status_code == 404


def test_process_input_missing_call():
    """Test process input with non-existent call"""
    response = client.post(
        "/process-input",
        data={
            "CallSid": "NONEXISTENT",
            "SpeechResult": "Hello",
            "Confidence": "0.95",
        }
    )
    # Should still return valid TwiML response
    assert response.status_code == 200


def test_call_workflow():
    """Test a complete call workflow"""
    # Start call
    call_response = client.post(
        "/incoming-call",
        data={
            "CallSid": "CA_TEST_001",
            "From": "+16175551212",
            "To": "+16175551313",
        }
    )
    assert call_response.status_code == 200

    # Get active calls
    calls_response = client.get("/calls")
    assert calls_response.status_code == 200

    # Get call details
    details_response = client.get("/calls/CA_TEST_001")
    assert details_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
