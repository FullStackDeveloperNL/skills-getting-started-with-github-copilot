import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    from app import activities
    
    # Store original state
    original = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and training",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Club": {
            "description": "Tennis lessons and friendly matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Acting, theater performances, and stage production",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts exploration",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through experiments",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
    }
    
    yield
    
    # Restore original state
    activities.clear()
    activities.update(original)
