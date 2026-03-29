from .database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    # required for flask security
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    roles = db.relationship('Role', backref = 'users', secondary = 'users_roles')
    student_profile = db.relationship('Student', backref='user')
    company_profile = db.relationship('Company', backref='user')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String)

# for many-to-many relationship
class UsersRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    branch = db.Column(db.String,nullable=False)
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('Application', backref='student')


# Company Model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.String)
    # location=db.Column(db.String)
    status = db.Column(db.String, default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    drives = db.relationship('PlacementDrive', backref='company')


# Placement Drive Model
class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String, nullable=False)
    branch = db.Column(db.String)
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    deadline = db.Column(db.String)
    status = db.Column(db.String, default="pending")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    applications = db.relationship('Application', backref='drive')


# Application Model
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_date = db.Column(db.String)
    status = db.Column(db.String, default="applied")
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))