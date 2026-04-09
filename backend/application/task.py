from celery import shared_task
from .models import Student, Application,PlacementDrive
from jinja2 import Template
from .mail import send_email
from datetime import datetime, timedelta ,date
import csv
import requests


@shared_task(ignore_results = False, name = "download_csv_report")
def csv_report(id):
    applications = Application.query.filter_by(student_id=id).all()
    print(applications)
    csv_file_name = f"application_{datetime.now().strftime("%f")}.csv" 
    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:
        sr_no = 1
        applic_csv = csv.writer(csvfile, delimiter = ',')
        applic_csv.writerow(['Sr No.', 'Student ID', 'Company Name', 'Drive Title', 'Application Status','Apply Date'])
        for a in applications:
            this_applic = [sr_no, a.student_id, a.drive.company.name, a.drive.job_title, a.status, a.application_date]
            applic_csv.writerow(this_applic)
            sr_no += 1

    return csv_file_name


@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    admin={}
    admin["email"]="user0@admin.com"
    today = date.today()
    first_day_last_month = date(today.year, today.month - 1, 1)
    last_day_last_month = date(today.year, today.month, 1) - timedelta(days=1)

    drives = PlacementDrive.query.filter(
        PlacementDrive.deadline >= first_day_last_month,
        PlacementDrive.deadline <= last_day_last_month
    ).all()

    report_drives = []
    total_applied = 0
    total_selected = 0

    for drive in drives:
        drive_info = {}
        drive_info['job_title'] = drive.job_title
        applications = Application.query.filter_by(drive_id=drive.id).all()
        drive_info['applied'] = len(applications)
        drive_info['selected'] = sum(1 for app in applications if app.selected)
        total_applied += drive_info['applied']
        total_selected += drive_info['selected']
        report_drives.append(drive_info)

    admin['month'] = first_day_last_month.strftime("%B %Y")
    admin['num_drives'] = len(drives)
    admin['total_applied'] = total_applied
    admin['total_selected'] = total_selected
    admin['drives'] = report_drives
    admin['generated_on'] = today.strftime("%d %B %Y")

    mail_template = """
    <h3>Dear Admin,</h3>
    <p>Please find the placement activity report for {{admin_data.month}} below:</p>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Drive Name</th>
            <th>Students Applied</th>
            <th>Students Selected</th>
        </tr>
        {% for drive in admin_data.drives %}
        <tr>
            <td>{{drive.name}}</td>
            <td>{{drive.applied}}</td>
            <td>{{drive.selected}}</td>
        </tr>
        {% endfor %}
        <tr>
            <th>Total</th>
            <th>{{admin_data.total_applied}}</th>
            <th>{{admin_data.total_selected}}</th>
        </tr>
    </table>
    <p>Report generated on: {{admin_data.generated_on}}</p>
    <h5>Regards,<br>
    Placement Cell<br>
</h5>
    """
    message = Template(mail_template).render(admin_data=admin)

    send_email(admin['email'], subject=f"Monthly Placement Activity Report - {admin['month']}", message=message)

    return f"Monthly placement report sent for {admin['month']}"




@shared_task(ignore_results = False, name = "deadline_update")
def deadline_update():

    students = Student.query.all()
    today = datetime.today()
    upcoming_day = today + timedelta(days=1)

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.deadline >= today,
        PlacementDrive.deadline <= upcoming_day
    ).all()

    for student in students:
        reminders = []

        for drive in drives:
            reminder = f"{drive.job_title}"
            reminders.append(reminder)

        if reminders:
            text = f"Hi {student.name}, you have upcoming deadlines:\n"

            for r in reminders:
                text += f"• {r}\n"

            text += "\nPlease apply before the deadline. Check the app at http://localhost:5173/"

            response = requests.post(
                "https://chat.googleapis.com/v1/spaces/AAQAxhN-eeM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=OYkASnUhVLRZnyyzzAdjfa2FD405g0TQ2Tefy8H-iuA",
                json={"text": text}
            )

            print(f"{student.name}: {response.status_code}")

    return "Notifications sent successfully"