from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User,Role
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    CORS(app)
    datastore = SQLAlchemyUserDatastore(db, User,Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    return app

app = create_app()
celery=celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_report.s(),
    )

    sender.add_periodic_task(
            crontab(minute = '*/1'),
            deadline_update.s(),)



with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name = "admin", description = "Superuser of app")
    app.security.datastore.find_or_create_role(name = "student", description = "Student user")
    app.security.datastore.find_or_create_role(name = "company", description = "Company recruiter")
    db.session.commit()
    if not app.security.datastore.find_user(email = "user0@admin.com"):
        app.security.datastore.create_user(email = "user0@admin.com",
                                           username = "Admin",
                                           password = generate_password_hash("1234"),
                                           roles = ['admin'])
        
    db.session.commit()
from application.routes import *


if __name__ == "__main__":
    app.run(debug=True)
