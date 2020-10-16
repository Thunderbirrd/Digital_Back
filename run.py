from app import app
from database import db
import routes

if __name__ == '__main__':
    db.create_all()
    app.run()