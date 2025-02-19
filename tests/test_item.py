def test_create_item(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = client.post("/items/", json={"name": "Test Item", "description": "A test item"}, headers=headers)

    print("DEBUG Status Code:", response.status_code)  # 👈 Imprimir código de estado
    print("DEBUG Response Body:", response.get_json())  # 👈 Imprimir JSON recibido

    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Item created"




def test_get_items(client):
    response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    token = response.get_json()["token"]

    response = client.get("/items/", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.is_json
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_get_item(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Crear un ítem y obtener su ID real
    create_response = client.post("/items/", json={"name": "Test Item", "description": "A test item"}, headers=headers)
    assert create_response.status_code == 201
    json_data = create_response.get_json()  # ✅ Ahora `json_data` es un diccionario
    print("DEBUG create_response JSON:", json_data)  # 👈 Imprimir la respuesta para depuración
    item_id = json_data["id"]  # ✅ Acceder correctamente al `id`

    response = client.get(f"/items/{item_id}", headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["name"] == "Test Item"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "Item not found"

def test_update_item(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Crear un ítem y obtener su ID
    create_response = client.post("/items/", json={"name": "Test Item", "description": "A test item"}, headers=headers)
    assert create_response.status_code == 201
    item_id = create_response.get_json()["id"]  # ✅ Obtener ID real

    response = client.put(f"/items/{item_id}", json={"name": "Updated Item"}, headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["message"] == "Item updated successfully"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "Item not found"


def test_delete_item(client):
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.get_json()["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Crear un ítem y obtener su ID
    create_response = client.post("/items/", json={"name": "Test Item", "description": "A test item"}, headers=headers)
    assert create_response.status_code == 201
    item_id = create_response.get_json()["id"]  # ✅ Obtener ID real

    response = client.delete(f"/items/{item_id}", headers=headers)

    if response.status_code == 200:
        assert response.is_json
        json_data = response.get_json()
        assert json_data["message"] == "Item deleted"
    else:
        assert response.status_code == 404
        assert response.get_json()["message"] == "Item not found"
