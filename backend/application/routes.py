from .database import db 
from .models import *
from.requrement import *
from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required,current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash



@app.route('/api/login', methods=['POST'])
def user_login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    if not email:
        return jsonify({
            "message": "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email = email)

    if user:
        print (password)
        print(type(password))
        print(len(password))
        if check_password_hash(user.password,password):
            login_user(user)
            return jsonify({
                "id": user.id,
                "username": user.username,
                "auth-token": user.get_auth_token(),
                "roles": [role.name for role in current_user.roles]
            })
        else:
            return jsonify({
                "message": "Incorrect Password"
            }), 400
    else:
       return jsonify({
            "message": "User Not Found!"
        }), 404 



@app.route('/api/register', methods=['POST'])
def create_user():
    credentials = request.get_json()
    try:
        if not app.security.datastore.find_user(email = credentials["email"]):
            app.security.datastore.create_user(email = credentials["email"],
                                            username = credentials["username"],
                                            password = generate_password_hash(credentials["password"]),
                                            roles = [credentials["role"]])
            db.session.commit()
            return jsonify({
                "message": "User created successfully"
            }), 201
    
        return jsonify({
            "message": "User already exists!"
        }), 400
    except:
        return jsonify({
                "message": "Specific roles are not allowed"
                }), 400


@app.route('/api/admin/dashboard')
@auth_required('token')
@roles_required('admin')
def dashboard():
    if "admin" in [role.name for role in current_user.roles]:
        approved_company=Company.query.filter_by(status="approved").all()
        pending_company=Company.query.filter_by(status="pending").all()
        student=Student.query.all()
        drive=PlacementDrive.query.all()
        application=Application.query.all()


        return jsonify({
            "username":current_user.username, "email":current_user.email ,
            "approved_company":companies(approved_company),"pending_company":companies(pending_company),
            "students":students(student),"student_applications":student_applications(application),
            "drive":drives(drive),
        })
    

@app.route('/api/admin/company/<int:id>', methods=['PUT'])
def update_status(id):
    data = request.get_json()
    company = Company.query.filter(Company.id == id).first()
    company.status = data.get("approval_status")
    db.session.commit()
    return {"message": "Updated"},200

@app.route('/api/admin/student/<int:id>', methods=['PUT'])
def block_student(id):
    data = request.get_json()
    student = Student.query.filter(Student.id == id).first()
    user = student.user
    user.active=data.get("active")
    db.session.commit()
    return {"message": "Done"},200