import pytest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Configura la aplicación Flask en modo de pruebas"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",  # ✅ Usar un archivo en disco para evitar reinicios
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()  # ✅ Crear tablas antes de las pruebas

        # Verifica si el usuario de prueba ya existe
        if not User.query.filter_by(username="testuser").first():
            user = User(username="testuser", password=generate_password_hash("password123"), role="user")
            db.session.add(user)
            db.session.commit()

    yield app  # ✅ Devuelve la app después de la configuración

    with app.app_context():
        db.drop_all()  # ✅ Limpiar la base de datos después de las pruebas

@pytest.fixture
def client(app):
    """Devuelve el cliente de pruebas"""
    return app.test_client()
