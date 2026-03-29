#return student application
def student_applications(applications):
    result = []
    for i in applications:
        result.append({
            "student_id": i.student_id,
            "student_name": i.student.name,
            "job_title": i.drive.job_title,
            "date": i.application_date,
            "status":i.status,
        })
    return result

def students(student):
    result = []
    for i in student:
        result.append({
            "id": i.id,
            "name": i.name,
            "branch": i.branch,
            "year": i.year,
            "cgpa":i.cgpa,
        })
    return result

def companies(company):
    result = []
    for i in company:
        result.append({
            "id": i.id,
            "company_name": i.name,
            # "location":i.location,
            "contact": i.contact,
            "status":i.status,
        })
    return result


#return list of drive JSON
def drives(drive):
    result = []
    for i in drive:
        result.append({
            "id": i.id,
            "job_title": i.job_title,
            "branch": i.branch,
            "cgpa":i.cgpa,
            "year":i.year,
            "deadline":i.deadline,
            "status":i.status,
        })
    return result