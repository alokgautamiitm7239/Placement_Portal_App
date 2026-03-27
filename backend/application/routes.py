from .database import db 
from .models import User, Role
from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required,current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

# @app.route('/')
# @auth_required('token')
# @roles_required('admin')
# def home():
#     return 'This is admin dashboard',200

@app.route('/student')
@auth_required('token')
@roles_required('student')
def student_home():
    user=current_user
    return jsonify({
        "username":user.username, "email":user.email
    })

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
