from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zamijenite 'your_secret_key' sa svojim tajnim ključem

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return 'Hello, Flask-Login!'

if __name__ == '__main__':
    app.run(debug=True)
print("app.py je uspješno izvršena.")