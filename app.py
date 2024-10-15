from flask import Flask
from flask_migrate import Migrate
from models import *

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to Flask"

@app.route("/users")
def users():
    return [user.to_dict() for user in User.query.all()], 200

if __name__ == '__main__':
    app.run(port=8080, debug=True)