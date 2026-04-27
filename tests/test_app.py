"""Tests for the FastAPI application"""
import pytest
import sys
from pathlib import Path

# Add src folder to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200"""
        # Arrange - already done by client fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_json(self, client):
        """Test that GET /activities returns valid JSON with activities"""
        # Arrange
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data

    def test_activities_have_required_fields(self, client):
        """Test that each activity has required fields"""
        # Arrange
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        # Arrange
        email = "test_student@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity returns 404"""
        # Arrange
        email = "test_student@mergington.edu"
        activity = "Non-existent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_prevention(self, client):
        """Test that duplicate signup is prevented"""
        # Arrange
        email = "duplicate_test@mergington.edu"
        activity = "Programming Class"
        
        # Act - First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Act - Second signup should fail
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]

    def test_signup_with_url_encoded_email(self, client):
        """Test signup with special characters in email"""
        # Arrange
        email = "test+special@mergington.edu"
        activity = "Gym Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_redirects(self, client):
        """Test that root endpoint redirects to static files"""
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert "/static" in response.headers.get("location", "")
