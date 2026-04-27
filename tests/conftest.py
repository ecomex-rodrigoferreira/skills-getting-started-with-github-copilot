"""Pytest configuration and fixtures for FastAPI tests"""
import pytest
import sys
from pathlib import Path

# Add src folder to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Provide a sample activity for testing"""
    return {
        "name": "Test Club",
        "description": "A test activity",
        "schedule": "Mondays 3:00 PM",
        "max_participants": 5,
        "participants": ["john@test.edu"]
    }


@pytest.fixture
def sample_email():
    """Provide a sample email for testing"""
    return "student@mergington.edu"
