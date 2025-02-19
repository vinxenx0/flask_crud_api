from flask_jwt_extended import create_access_token, get_jwt_identity

from flask_jwt_extended import create_access_token

def generate_token(user):
    return create_access_token(identity=str(user.id))  # 👈 Convertir `id` a string para que JWT lo acepte correctamente



def get_current_user():
    return get_jwt_identity()
