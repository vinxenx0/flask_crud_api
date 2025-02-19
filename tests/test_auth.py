import json

def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "newpassword",
        "role": "user"
    })

    assert response.status_code == 201
    assert response.is_json  # 👈 Verificar que Flask devuelve JSON
    json_data = response.get_json()  # 👈 Acceder a los datos correctamente
    assert json_data["message"] == "User created successfully"


def test_login_user(client):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.is_json  # 👈 Verificar que la respuesta es JSON
    json_data = response.get_json()  # 👈 Acceder a los datos correctamente
    assert "token" in json_data

