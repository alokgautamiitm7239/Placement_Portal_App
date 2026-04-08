#return student application
def student_applications(applications):
    result = []
    for i in applications:
        result.append({
            "id":i.id,
            "student_id": i.student_id,
            "resume":i.resume,
            "student_name": i.student.name,
            "job_title": i.drive.job_title,
            "company_name":i.drive.company.name,
            "date": i.application_date,
            "status":i.status,
            "branch": i.student.branch,
            "experience_year": i.student.experience_year,
            "cgpa":i.student.cgpa,
            "skills":i.student.skills
        })
    return result


def students(student):
    result = []
    for i in student:
        result.append({
            "id": i.id,
            "active":i.user.active,
            "name": i.name,
            "branch": i.branch,
            "experince_year": i.experience_year,
            "cgpa":i.cgpa,
            "course":i.course,
            "skills":i.skills
        })
    return result

def companies(company):
    result = []
    for i in company:
        result.append({
            "id": i.id,
            "active":i.user.active,
            "website":i.website,
            "company_name": i.name,
            "location":i.location,
            "contact": i.contact,
            "status":i.status,
        })
    return result


def drives(drive):
    result = []
    for i in drive:
        result.append({
            "id": i.id,
            "job_title": i.job_title,
            "branch": i.branch,
            "cgpa":i.cgpa,
            "qualification":i.qualification,
            "experience_year":i.experience_year,
            "deadline":i.deadline,
            "status":i.status,
            "company_name":i.company.name,
            "application_len":len(i.applications)
        })
    return result