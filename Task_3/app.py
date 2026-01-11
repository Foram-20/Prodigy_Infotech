from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config
from auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)  # <-- THIS LINE IS MANDATORY

app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return 'JWT Auth API is running!'

if __name__ == '__main__':
    app.run(debug=True)
