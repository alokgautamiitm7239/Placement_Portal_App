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
        if check_password_hash(user.password,password):
            login_user(user)
            if not user.active:
                return {"message": "Account blocked by admin"}, 403
            roles=[role.name for role in current_user.roles]
            return jsonify({
                "id": user.id,
                "username": user.username,
                "auth-token": user.get_auth_token(),
                "role": roles[0]
            })
        else:
            return jsonify({
                "message": "Incorrect Password!"
            }), 400
    else:
       return jsonify({
            "message": "User Not Found ? please SignUp!"
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
    rejected_company=Company.query.filter_by(status="rejected").all()
    return jsonify({"approved_company":companies(approved_company),
                    "pending_company":companies(pending_company),
                    "rejected_company":companies(rejected_company),
                    })


@app.route('/api/admin/drive')
@auth_required('token')
@roles_required('admin')
def drive():
    approved_drive=PlacementDrive.query.filter_by(status="approved").all()
    pending_drive=PlacementDrive.query.filter_by(status="pending").all()
    rejected_drive=PlacementDrive.query.filter_by(status="rejected").all()
    return jsonify({"approved_drive":drives(approved_drive),
                    "pending_drive":drives(pending_drive),
                    "rejected_drive":drives(rejected_drive),
                    })


@app.route('/api/admin/application')
@auth_required('token')
@roles_required('admin')
def application():
    application=Application.query.all()
    return jsonify({"applications":student_applications(application)})


@app.route('/api/admin/company/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def update_status(id):
    data = request.get_json()
    company = Company.query.filter(Company.id == id).first()
    company.status = data.get("status")
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

@app.route('/api/admin/drive/<int:id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def drive_status(id):
    data = request.get_json()
    drive=PlacementDrive.query.filter(PlacementDrive.id== id).first()
    drive.status = data.get("status")
    db.session.commit()
    return {"message": "Updated"},200

# -------------------------------------------------COMPANY ENDPOINT----------------------------------------------------------

@app.route('/api/company/register', methods=['POST'])
@auth_required('token')
@roles_required('company')
def register_company():
    data = request.get_json()
    cmp= Company(
        name=data.get("name"),
        contact=data.get("contact"),
        website=data.get("website"),
        location=data.get("location"),
        user_id=current_user.id
    )
    db.session.add(cmp)
    db.session.commit()
    return {"message": "Profile created"}, 201

@app.route('/api/company/create_drive', methods=['POST'])
@auth_required('token')
@roles_required('company')
def creat_drive():
    data = request.get_json()
    drv= PlacementDrive(
        job_title = data.get("job_title"),
        qualification = data.get("qualification"),
        branch = data.get("branch"),
        cgpa = data.get("cgpa"),
        experience_year = data.get("experience_year"),
        deadline=data.get("deadline"),
        company_id=current_user.company_profile[0].id
            )
    db.session.add(drv)
    db.session.commit()
    return {"message": "Drive created"}, 201


@app.route('/api/company/dashboard')
@auth_required('token')
@roles_required('company')
def company_dashboard():
    company = Company.query.filter_by(user_id=current_user.id).first()
    if company:
      cmpny_id = company.id
      company_status=company.status
      drive=PlacementDrive.query.filter_by(company_id=cmpny_id).all()
    #   application_length=len[for app in drive.applications]
      company_drive=drives(drive)
      return jsonify({"name":company.name,"company_drive":company_drive,"status":company_status  ,"message":"Done"}),200
    else:
        return jsonify({"message":"Register the company first"})

@app.route('/api/company/drive/<int:id>')
@auth_required('token')
@roles_required('company')
def company_drive(id):
    shortlisted_applictn = Application.query.filter_by(drive_id=id,status="shortlisted").all()
    applied_applictn = Application.query.filter_by(drive_id=id,status="applied").all()
    rejected_applictn = Application.query.filter_by(drive_id=id,status="rejected").all()
    return jsonify({"shortlisted_applications":student_applications(shortlisted_applictn),
                    "applied_applications":student_applications(applied_applictn),
                    "rejected_applications":student_applications(rejected_applictn)
                    })

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
@app.route('/api/student/register', methods=['POST'])
@auth_required('token')
@roles_required('student')
def register_student():
    data = request.get_json()
    cmp= Student(
        name=data.get("name"),
        course=data.get("course"),
        branch=data.get("branch"),
        cgpa=data.get("cgpa"),
        experience_year=data.get("experience_year"),
        skills=data.get("skills"),
        user_id=current_user.id
    )
    db.session.add(cmp)
    db.session.commit()
    return {"message": "Profile created"}, 201


@app.route('/api/student/dashboard')
@auth_required('token')
@roles_required('student')
def student_dashboard():
        approved_drive=PlacementDrive.query.filter_by(status="approved").all()
        student=Student.query.filter_by(user_id=current_user.id).first()
        if student:
            student_id=student.id
            name=student.name
            applic = Application.query.filter_by(student_id=student_id).all()
            result = []
            for a in applic:
                drive = PlacementDrive.query.get(a.drive_id)
                result.append({
                "job_title":drive.job_title,"company_name":drive.company.name,"status":a.status,
                 })

            return jsonify({"message":"Done", "approved_drive":drives(approved_drive),
                             "name":name, "id":student_id, "applied_drive":result,
                    })
        else:
            return jsonify({"message":"Register student first"
            })
        
@app.route('/api/student/application/<int:drive_id>/<int:student_id>')
@auth_required('token')
@roles_required('student')
def student_application(drive_id,student_id):
    exist= Application.query.filter_by(student_id=student_id,drive_id=drive_id).first()
    if exist:
        return jsonify({"message":"Already applied"
            })
    cmp= Application(
        application_date="12/07/2025",
        student_id=student_id,
        drive_id=drive_id,

    )
    db.session.add(cmp)
    db.session.commit()
    return {"message": "Applied successfully"}, 201


@app.route('/api/student/update_profile', methods=['PUT'])
@auth_required('token')
@roles_required('student')
def update_profile():
    data = request.get_json()
    student=Student.query.filter_by(user_id=current_user.id).first()
    student.name=data.get("name"),
    student.course=data.get("contact"),
    student.branch=data.get("branch"),
    student.cgpa=data.get("cgpa"),
    student.experience_year=data.get("experience_year"),
    student.skills=data.get("skills"),
    db.session.commit()
    return {"message": "Updated"},200





    


