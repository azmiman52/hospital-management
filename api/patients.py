from models import db, PatientModel, GenderEnum
from flask import request, jsonify

class PatientApi:
    def __init__(self) -> None:
        pass

    def set_gender(self, gender):
        if(gender.upper() == "MALE"):
            return GenderEnum.MALE
        elif (gender.upper() == "FEMALE"):
            return GenderEnum.FEMALE
        return  GenderEnum.MALE
    
    def add_patient(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        name = data.get('name')
        gender = data.get('gender')
        birthdate = data.get('birthdate')
        no_ktp = data.get('no_ktp')
        address = data.get('address')
        vaccine_type = data.get('vaccine_type')
        vaccine_count = data.get('vaccine_count')

        if not all([name, gender, birthdate, no_ktp, address, vaccine_type, vaccine_count]):
            return jsonify({"error": "Missing data"}), 400
        
        if PatientModel.query.filter_by(no_ktp=no_ktp).first():
                return jsonify({"error": "Patient with this no_ktp is already exist"}), 404

        gender = self.set_gender(gender)
        try:
            patient = PatientModel(name=name, gender=gender, birthdate=birthdate, no_ktp=no_ktp, address=address, vaccine_type=vaccine_type, vaccine_count=vaccine_count)
            db.session.add(patient)
            db.session.commit()

            return patient.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def get_patients(self):
        try:
            patients = PatientModel.query.all()

            response = {"patients":[patient.to_response() for patient in patients]}

            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_patient_by_id(self, patient_id):
        try:
            patient = PatientModel.query.get(patient_id)
            if patient is None:
                return jsonify({"error": "Patient not found"}), 404

            response = patient.to_response()

            response['medical_history'] = [appointment.to_response() for appointment in patient.appointments]
            
            return response, 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def update_patient(self, patient_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        patient_by_id = PatientModel.query.get(patient_id)
        if patient_by_id is None:
            return jsonify({"error": "Patient not found"}), 404

        name = data.get('name')
        gender = data.get('gender')
        birthdate = data.get('birthdate')
        no_ktp = data.get('no_ktp')
        address = data.get('address')
        vaccine_type = data.get('vaccine_type')
        vaccine_count = data.get('vaccine_count')
        
        patient_by_no_ktp = PatientModel.query.filter_by(no_ktp=no_ktp).first() 
        if patient_by_no_ktp and patient_by_no_ktp.no_ktp != patient_by_id.no_ktp:
            return jsonify({"error": "Patient with this no_ktp is already exist"}), 409
        
        try:
            patient = PatientModel.query.get(patient_id)
            if name is not None:
                patient.name = name
            if gender is not None:
                patient.gender = self.set_gender(gender)
            if birthdate is not None:
                patient.birthdate = birthdate
            if no_ktp is not None and patient_by_id.no_ktp != no_ktp:
                patient.no_ktp = no_ktp
            if address is not None:
                patient.address = address
            if vaccine_type is not None:
                patient.vaccine_type = vaccine_type
            if vaccine_count is not None:
                patient.vaccine_count = vaccine_count
                
            db.session.add(patient)
            db.session.commit()

            return patient.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete_patient(self, patient_id):
        try:
            patient = PatientModel.query.get(patient_id)
            if patient is None:
                return jsonify({"error": "Patient not found"}), 404
            
            db.session.delete(patient)
            db.session.commit()

            return jsonify({"message": "Patient is deleted"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500