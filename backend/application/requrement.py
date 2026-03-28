#return student application
def student_applications(applications):
    result = []
    for i in applications:
        result.append({
            "id": i.id,
            "student_name": i.student.name,
            "drive_title": i.drive.job_title,
            "company_name": i.drive.company.name,
            "date": i.application_date,
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