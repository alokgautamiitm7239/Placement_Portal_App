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

# --------------------------------------------------ADMIN ENDPOINTS-------------------------------------------------

@app.route('/api/admin/dashboard')
@auth_required('token')
@roles_required('admin')
def dashboard():
        approved_company=len(Company.query.filter_by(status="approved").all())
        student=len(Student.query.all())
        drive=len(PlacementDrive.query.all())
        application=len(Application.query.all())

        return jsonify({
            "username":current_user.username, "email":current_user.email ,
            "company":approved_company,"student":student,"drive":drive,"application":application,
        })


@app.route('/api/admin/student')
@auth_required('token')
@roles_required('admin')
def student():
    student=Student.query.all()
    return jsonify({"students":students(student)})


@app.route('/api/admin/company')
@auth_required('token')
@roles_required('admin')
def company():
    approved_company=Company.query.filter_by(status="approved").all()
    pending_company=Company.query.filter_by(status="pending").all()
    return jsonify({ "approved_company":companies(approved_company),
                    "pending_company":companies(pending_company),
                    })


@app.route('/api/admin/drive')
@auth_required('token')
@roles_required('admin')
def drive():
    drive=PlacementDrive.query.all()
    return jsonify({"drive":drives(drive),})


@app.route('/api/admin/application')
@auth_required('token')
@roles_required('admin')
def application():
    application=Application.query.all()
    return jsonify({"student_applications":student_applications(application)})


@app.route('/api/admin/company/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def update_status(id):
    data = request.get_json()
    company = Company.query.filter(Company.id == id).first()
    company.status = data.get("approval_status")
    db.session.commit()
    return {"message": "Updated"},200


@app.route('/api/admin/student/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def block_student(id):
    data = request.get_json()
    student = Student.query.filter(Student.id == id).first()
    user = student.user
    user.active=data.get("active")
    db.session.commit()
    return {"message": "Done"},200


@app.route('/api/admin/Bcompany/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def block_company(id):
    data = request.get_json()
    company = Company.query.filter(Company.id == id).first()
    user = company.user
    user.active=data.get("active")
    db.session.commit()
    return {"message": "Done"},200

# -------------------------------------------------COMPANY ENDPOINT----------------------------------------------------------

@app.route('/api/company/register', methods=['POST'])
@auth_required('token')
@roles_required('company')
def register_company():
    data = request.get_json()
    if current_user.company_profile:
        return {"message": "Profile already exist"}, 400
    cmp= Company(
        name=data.get("name"),
        contact=data.get("contact"),
        # location=data.get("location"),
    )
    db.session.add(cmp)
    db.session.commit()
    return {"message": "Profile created"}, 201

@app.route('/api/company/creat_drive', methods=['POST'])
@auth_required('token')
@roles_required('company')
def creat_drive():
    data = request.get_json()
    drv= PlacementDrive(
        job_title = data.get("job_title"),
        branch = data.get("branch"),
        cgpa = data.get("cgpa"),
        year = data.get("year"),
        deadline=data.get("deadline"),
            )
    db.session.add(drv)
    db.session.commit()
    return {"message": "Drive created"}, 201


@app.route('/api/company/dashboard')
@auth_required('token')
@roles_required('company')
def company_dashboard():
    company = Company.query.filter_by(user_id=current_user.id).first()
    cmpny_id = company.id
    drive=PlacementDrive.query.filter_by(company_id=cmpny_id).all()
    company_drive=drives(drive)
    return jsonify({"name":company.name,"company_drive":company_drive})

@app.route('/api/company/drive/<int:id>')
@auth_required('token')
@roles_required('company')
def company_drive(id):
    applictn = Application.query.filter_by(drive_id=id).all()
    applications=student_applications(applictn)
    return jsonify({"applications":applications})

@app.route('/api/company/application/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('company')
def application_status(id):
    data = request.get_json()
    applictn = Application.query.filter(Application.id == id).first()
    applictn.status = data.get("status")
    db.session.commit()
    return {"message": "Updated"},200

# ----------------------------------------------STUDENT ENDPOINTS---------------------------------------------------

@app.route('/api/student/dashboard')
@auth_required('token')
@roles_required('student')
def student_dashboard():
        approved_company=Company.query.filter_by(status="approved").all()

        student=Student.query.filter_by(user_id=current_user.id).first()
        student_id=student.id
        applic = Application.query.filter_by(student_id=student_id).all()
        result = []
        for a in applic:
         drive = PlacementDrive.query.get(a.drive_id)
        result.append({
            "title": drive.job_title,
            "status": a.status
        })

        return jsonify({
            "company":companies(approved_company), "name":student.name,
            "drive_status":result,
        })

@app.route('/api/student/update_profile', methods=['PUT'])
@auth_required('token')
@roles_required('student')
def update_profile():
    data = request.get_json()
    student=Student.query.filter_by(user_id=current_user.id).first()
    student.name = data.get("name")
    student.branch = data.get("branch")
    student.cgpa = data.get("cgpa")
    student.year = data.get("year")
    db.session.commit()
    return {"message": "Updated"},200





    


