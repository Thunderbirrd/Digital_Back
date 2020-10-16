from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from flask_session import Session

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Session(app)