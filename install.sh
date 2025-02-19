python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# pip install pytest pytest-flask Flask-Testing
# pip install flask-bootstrap flask-wtf
apt install sqlite3 flask_migrate
#pip install flask-login


pip install -r requirements.txt
# python run.py

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
