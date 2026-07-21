def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    route = f"/activities/{activity_name}/participants/{email}"

    # Act
    response = client.delete(route)

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert body["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_when_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    route = f"/activities/{activity_name}/participants/{email}"

    # Act
    response = client.delete(route)

    # Assert
    body = response.json()
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    route = f"/activities/{activity_name}/participants/{email}"

    # Act
    response = client.delete(route)

    # Assert
    body = response.json()
    assert response.status_code == 404
    assert body["detail"] == "Student is not signed up for this activity"