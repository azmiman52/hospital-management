from models import db, DoctorModel, GenderEnum
from flask import request, jsonify
import hashlib


class DoctorApi:

    def __init__(self) -> None:
        pass

    def set_gender(self, gender):
        if(gender.upper() == "MALE"):
            return GenderEnum.MALE
        elif (gender.upper() == "FEMALE"):
            return GenderEnum.FEMALE
        return  GenderEnum.MALE

    def set_password(self, password):
        hashString = hashlib.new('sha256')
        hashString.update(password.encode())
        return hashString.hexdigest()

    def add_doctor(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        birthdate = data.get('birthdate')
        work_start_time = data.get('work_start_time')
        work_end_time = data.get('work_end_time')

        if not all([name, username, password, gender, birthdate]):
            return jsonify({"error": "Missing data"}), 400
            
        if DoctorModel.query.filter_by(username=username).first():
            return jsonify({"error": "Doctor with this username is already exist"}), 409

        gender = self.set_gender(gender)

        password = self.set_password(password)

        try:
            doctor = DoctorModel(name=name, username=username, password=password, gender=gender, birthdate=birthdate, work_start_time=work_start_time, work_end_time=work_end_time)
            db.session.add(doctor)
            db.session.commit()

            return doctor.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def get_doctors(self):
        try:
            doctors = DoctorModel.query.all()

            response = {"doctors":[doctor.to_response() for doctor in doctors]}

            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def get_doctor_by_id(self, doctor_id):
        try:
            doctor = DoctorModel.query.get(doctor_id)
            if doctor is None:
                return jsonify({"error": "Doctor not found"}), 404

            return doctor.to_response(), 201
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def update_doctor(self, doctor_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        doctor_by_id  = DoctorModel.query.get(doctor_id)
        if doctor_by_id is None:
            return jsonify({"error": "Doctor not found"}), 404

        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        birthdate = data.get('birthdate')
        work_start_time = data.get('work_start_time')
        work_end_time = data.get('work_end_time')

        doctor_by_username = DoctorModel.query.filter_by(username=username).first() 
        if doctor_by_username and doctor_by_username.username != doctor_by_id.username:
            return jsonify({"error": "Doctor with this username is already exist"}), 409

        try:
            doctor = DoctorModel.query.get(doctor_id)
            if name is not None:
                doctor.name = name
            if username is not None:
                doctor.username = username
            if password is not None:
                doctor.password = self.set_password(password)
            if gender is not None:
                doctor.gender = self.set_gender(gender)
            if birthdate is not None:
                doctor.birthdate = birthdate
            if work_start_time is not None:
                doctor.work_start_time = work_start_time
            if work_end_time is not None:
                doctor.work_end_time = work_end_time
            
            db.session.add(doctor)
            db.session.commit()
            
            return  doctor.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete_doctor(self, doctor_id):
        try:
            doctor = DoctorModel.query.get(doctor_id)
            if doctor is None:
                return jsonify({"error": "Doctor not found"}), 404
            
            db.session.delete(doctor)
            db.session.commit()

            return jsonify({"message": "Doctor is deleted"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500