"""Tests for the activities API endpoints."""
import pytest


def test_root_redirect(client):
    """Test that root path redirects to static HTML."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client, reset_activities):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Drama Club" in data
    assert "Art Studio" in data
    assert "Debate Club" in data
    assert "Science Club" in data


def test_get_activities_structure(client, reset_activities):
    """Test the structure of activity data."""
    response = client.get("/activities")
    data = response.json()
    
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_new_participant(client, reset_activities):
    """Test signing up a new participant for an activity."""
    response = client.post(
        "/activities/Basketball Team/signup?email=alice@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "alice@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "alice@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_already_registered(client, reset_activities):
    """Test signing up a participant who is already registered."""
    # michael@mergington.edu is already in Chess Club
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signing up for a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=bob@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_participant(client, reset_activities):
    """Test unregistering a participant from an activity."""
    # michael@mergington.edu is in Chess Club
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from a non-existent activity."""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister?email=bob@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_nonexistent_participant(client, reset_activities):
    """Test unregistering a participant who is not in the activity."""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_signup_and_unregister_flow(client, reset_activities):
    """Test a complete flow of signing up and then unregistering."""
    # Sign up
    signup_response = client.post(
        "/activities/Tennis Club/signup?email=testuser@mergington.edu"
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    activities_response = client.get("/activities")
    assert "testuser@mergington.edu" in activities_response.json()["Tennis Club"]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        "/activities/Tennis Club/unregister?email=testuser@mergington.edu"
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister
    activities_response = client.get("/activities")
    assert "testuser@mergington.edu" not in activities_response.json()["Tennis Club"]["participants"]


def test_multiple_signups_same_activity(client, reset_activities):
    """Test multiple participants signing up for the same activity."""
    user1 = "user1@mergington.edu"
    user2 = "user2@mergington.edu"
    user3 = "user3@mergington.edu"
    
    # Sign up multiple users
    for user in [user1, user2, user3]:
        response = client.post(
            f"/activities/Drama Club/signup?email={user}"
        )
        assert response.status_code == 200
    
    # Verify all are registered
    activities_response = client.get("/activities")
    drama_participants = activities_response.json()["Drama Club"]["participants"]
    assert user1 in drama_participants
    assert user2 in drama_participants
    assert user3 in drama_participants
    assert len(drama_participants) == 3


def test_availability_calculation(client, reset_activities):
    """Test that availability is calculated correctly."""
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club has max 12, currently has 2
    chess = activities["Chess Club"]
    expected_availability = chess["max_participants"] - len(chess["participants"])
    assert expected_availability == 10
