import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Vercel filesystem is read-only. Use /tmp for the database.
    if os.environ.get('VERCEL'):
        db_path = os.path.join('/tmp', 'gcb_monitor.db')
    else:
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        db_path = os.path.join(app.instance_path, 'gcb_monitor.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models, routes
        from .routes import app_routes
        app.register_blueprint(app_routes)
        db.create_all()

    return app
