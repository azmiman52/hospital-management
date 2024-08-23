from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class GenderEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    

class AppointmentStatus(enum.Enum):
    IN_QUEUE = "IN_QUEUE"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class EmployeeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def to_response(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "gender": self.gender.value,
            "birthdate": self.birthdate
        }
    
    def __repr__(self):
        return f'Name: {self.name}, Username: {self.username}, Gender: {self.gender}, Birthdate: {self.birthdate}'

class PatientModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.Enum(GenderEnum))
    birthdate = db.Column(db.DateTime)
    no_ktp = db.Column(db.String(50))
    address = db.Column(db.String(100))
    vaccine_type = db.Column(db.String(100))
    vaccine_count = db.Column(db.Integer)

    appointments = db.relationship('AppointmentsModel', backref='patient')

    def to_response(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender.value,
            "birthdate": self.birthdate,
            "no_ktp": self.no_ktp,
            "address": self.address,
            "vaccine_type": self.vaccine_type,
            "vaccine_count": self.vaccine_count,
        }

    def __repr__(self):
        return f'Name: {self.name}, Gender: {self.gender}, Birthdate: {self.birthdate}'
    
class DoctorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    work_start_time = db.Column(db.Time)
    work_end_time = db.Column(db.Time)

    appointments = db.relationship('AppointmentsModel', backref='doctor')

    def to_response(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "gender": self.gender.value,
            "birthdate": self.birthdate.strftime('%Y-%m-%d'),
            "work_start_time": self.work_start_time.strftime('%H:%M'),
            "work_end_time": self.work_end_time.strftime('%H:%M')
        }
    
    def __repr__(self):
        return f'Name: {self.name}, Username: {self.username}, Gender: {self.gender}, Birthdate: {self.birthdate}'
    
class AppointmentsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_model.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_model.id'), nullable=False)
    datetime = db.Column(db.DateTime)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False)
    diagnose = db.Column(db.Text)
    notes = db.Column(db.Text)

    def to_response(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "datetime": self.datetime.isoformat(),
            "status": self.status.name,
            "diagnose": self.diagnose,
            "notes": self.notes
        }


    def __repr__(self):
        return f'Patient ID: {self.patient_id}, Doctor ID: {self.doctor_id}, DateTime: {self.datetime}, Status: {self.status}'