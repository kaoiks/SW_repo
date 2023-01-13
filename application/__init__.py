from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app = Flask(__name__)
app.config['SECRET_KEY'] = "JLKJJJO3IURYoiouolnojojouuoo=5y9y9youjuy952oohhbafdnoglhoho"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sw_db.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

with app.app_context():
    db.session.execute('pragma foreign_keys=on')

from application import routes
