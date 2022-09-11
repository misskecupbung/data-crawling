from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.model import item, linkResult, transaction, user
from app import auth
app.register_blueprint(auth.bp)
from app import dc
app.register_blueprint(dc.bp)
app.add_url_rule('/', endpoint='index')

@app.errorhandler(404)
def page_not_found(i):
    # note that we set the 404 status explicitly
    return render_template('dc/page-404.html'), 404





