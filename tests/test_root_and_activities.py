def test_root_redirects_to_static_index(client):
    # Arrange
    route = "/"

    # Act
    response = client.get(route, allow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    route = "/activities"

    # Act
    response = client.get(route)

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body, dict)
    assert len(body) > 0


def test_get_activities_items_include_required_fields(client):
    # Arrange
    route = "/activities"
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get(route)

    # Assert
    body = response.json()
    assert response.status_code == 200

    first_activity = next(iter(body.values()))
    assert required_fields.issubset(first_activity.keys())
    assert isinstance(first_activity["participants"], list)