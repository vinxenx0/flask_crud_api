#!/bin/bash

# Configuración
BASE_URL="http://localhost:5000"
USERNAME="testuser"
PASSWORD="password123"

# 1️⃣ Registrar usuario (ignorar si ya existe)
echo "🔹 Registrando usuario..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\", \"role\": \"user\"}")

echo "✅ Respuesta de registro: $REGISTER_RESPONSE"

# 2️⃣ Iniciar sesión y obtener token
echo "🔹 Iniciando sesión..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | jq -r '.token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ ERROR: No se pudo obtener el token de autenticación."
    exit 1
fi

echo "✅ Token obtenido: $TOKEN"

# 3️⃣ Probar endpoints con el token

# Obtener usuarios
echo "🔹 Obteniendo lista de usuarios..."
curl -s -X GET "$BASE_URL/users/" -H "Authorization: Bearer $TOKEN"

# Crear un ítem
echo "🔹 Creando un ítem..."
ITEM_RESPONSE=$(curl -s -X POST "$BASE_URL/items/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "Laptop", "description": "Laptop Dell"}')

ITEM_ID=$(echo $ITEM_RESPONSE | jq -r '.id')
echo "✅ Ítem creado con ID: $ITEM_ID"

# Obtener ítems
echo "🔹 Obteniendo lista de ítems..."
curl -s -X GET "$BASE_URL/items/" -H "Authorization: Bearer $TOKEN"

# Obtener ítem específico
echo "🔹 Obteniendo ítem con ID $ITEM_ID..."
curl -s -X GET "$BASE_URL/items/$ITEM_ID" -H "Authorization: Bearer $TOKEN"

# Actualizar ítem
echo "🔹 Actualizando ítem con ID $ITEM_ID..."
curl -s -X PUT "$BASE_URL/items/$ITEM_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "Updated Laptop"}'

# Eliminar ítem
echo "🔹 Eliminando ítem con ID $ITEM_ID..."
curl -s -X DELETE "$BASE_URL/items/$ITEM_ID" -H "Authorization: Bearer $TOKEN"

echo "✅ Pruebas completadas correctamente."
