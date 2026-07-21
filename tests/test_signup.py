def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert body["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_when_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    body = response.json()
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_signup_returns_400_when_email_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    body = response.json()
    assert response.status_code == 400
    assert body["detail"] == "Student already signed up for this activity"


def test_signup_supports_url_encoded_activity_name(client):
    # Arrange
    encoded_activity_name = "Programming%20Class"
    resolved_activity_name = "Programming Class"
    email = "coder@mergington.edu"
    route = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert body["message"] == f"Signed up {email} for {resolved_activity_name}"

    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[resolved_activity_name]["participants"]