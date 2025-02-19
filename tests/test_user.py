def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "newpassword",
        "role": "user"
    })

    if response.status_code == 409:  # Usuario ya registrado
        assert response.get_json()["message"] == "Username already exists"
    else:
        assert response.status_code == 201
        assert response.is_json
        json_data = response.get_json()
        assert json_data["message"] == "User created successfully"


def test_get_users(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json().get("token", None)
    assert token, "Token de autenticación no recibido"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"  # ✅ Asegurar que se pida JSON
    }

    response = client.get("/users/", headers=headers)
    assert response.status_code in [200, 404]



def test_get_user(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = client.get("/users/1", headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["username"] == "testuser"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "User not found"


def test_update_user(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = client.put("/users/1", json={"username": "updateduser"}, headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["message"] == "User updated successfully"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "User not found"


def test_delete_user(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = client.delete("/users/1", headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["message"] == "User deleted"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "User not found"
    