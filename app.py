import os, jwt, pytz
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response, render_template, session
from models import db
from datetime import datetime, timedelta
from functools import wraps

from api.patients import PatientApi
from api.doctors import DoctorApi
from api.employees import EmployeeApi
from api.appointments import AppointmentApi

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables in the database
with app.app_context():
    db.create_all()

patientApi = PatientApi()
doctorApi = DoctorApi()
employeeApi = EmployeeApi()
appointmentApi = AppointmentApi()

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token and automatically check for expiration
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data not provided"}), 400

    username = data.get('username')
    password = data.get('password')

    employee = employeeApi.get_employee_by_username(username)

    if employee.get('username') == username and employee.get('password') == employeeApi.set_password(password):
        indonesia_tz = pytz.timezone('Asia/Jakarta')
        expiration_time = datetime.now(indonesia_tz) + timedelta(seconds=1800)

        token = jwt.encode({
            'user': username,
            'exp': expiration_time
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'expiration': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
            }), 200
    else:
        return jsonify({'message': "Authentication Failed "})

@app.route('/')
def index():
    return "Hospital Management API Collection"

### EMPLOYEE ###

@app.route('/employees', methods=['POST'])
@token_required
def add_employee():
    return employeeApi.add_employee()

@app.route('/employees', methods=['GET'])
@token_required
def get_employee():
    return employeeApi.get_employees()

@app.route('/employees/<int:employee_id>', methods=['GET'])
@token_required
def get_employee_by_id(employee_id):
    return employeeApi.get_employee_by_id(employee_id)

@app.route('/employees/<int:employee_id>', methods=['PUT'])
@token_required
def update_employeet(employee_id):
    return employeeApi.update_employee(employee_id)

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@token_required
def delete_employee(employee_id):
    return employeeApi.delete_employee(employee_id)

### PATIENT ###

@app.route('/patients', methods=['POST'])
@token_required
def add_patient():
    return patientApi.add_patient()

@app.route('/patients', methods=['GET'])
@token_required
def get_patients():
    return patientApi.get_patients()

@app.route('/patients/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_by_id(patient_id):
    return patientApi.get_patient_by_id(patient_id)

@app.route('/patients/<int:patient_id>', methods=['PUT'])
@token_required
def update_patient(patient_id):
    return patientApi.update_patient(patient_id)

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
@token_required
def delete_patient(patient_id):
    return patientApi.delete_patient(patient_id)

### DOCTOR ###

@app.route('/doctors', methods=['POST'])
@token_required
def add_doctor():
    return doctorApi.add_doctor()

@app.route('/doctors', methods=['GET'])
@token_required
def get_doctors():
    return doctorApi.get_doctors()

@app.route('/doctors/<int:doctor_id>', methods=['GET'])
@token_required
def get_doctor_by_id(doctor_id):
    return doctorApi.get_doctor_by_id(doctor_id)


@app.route('/doctors/<int:doctor_id>', methods=['PUT'])
@token_required
def update_doctor(doctor_id):
    return doctorApi.update_doctor(doctor_id)

@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@token_required
def delete_doctor(doctor_id):
    return doctorApi.delete_doctor(doctor_id)

### APPOINTMENT ###

@app.route('/appointments', methods=['POST'])
@token_required
def add_appointment():
    return appointmentApi.add_appointments()

@app.route('/appointments', methods=['GET'])
@token_required
def get_appointments():
    return appointmentApi.get_appointments()

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
@token_required
def get_appointment_by_id(appointment_id):
    return appointmentApi.get_appointment_by_id(appointment_id)


@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
@token_required
def update_appointment(appointment_id):
    return appointmentApi.update_appointment(appointment_id)

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@token_required
def delete_appointment(appointment_id):
    return appointmentApi.delete_appointment(appointment_id)


if __name__ == "__main__":
    app.run(debug=True)
