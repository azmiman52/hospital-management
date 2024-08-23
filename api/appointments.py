from models import db, AppointmentsModel, AppointmentStatus, DoctorModel, PatientModel
from flask import request, jsonify
from datetime import datetime

class AppointmentApi:
    def __init__(self) -> None:
        pass

    def set_status(self, status):
        if(status.upper() == "IN_QUEUE"):
            return AppointmentStatus.IN_QUEUE
        elif (status.upper() == "DONE"):
            return AppointmentStatus.DONE
        elif (status.upper() == "CANCELLED"):
            return AppointmentStatus.CANCELLED
        else:
            return jsonify({"error": "Provided appointment status is incorrect"}), 400
        
    def validate_time_appointment(self, doctor, current_datetime, issued_datetime):
        issued_time = datetime.strptime(issued_datetime, '%Y-%m-%d %H:%M:%S').time()

        if current_datetime != None:
            if(issued_time == current_datetime.time()):
                return True

        if(issued_time < doctor.work_start_time or issued_time >= doctor.work_end_time):
            return False
        
        for appointment in doctor.appointments:
            if appointment.datetime.time() == issued_time:
                return False
        
        return issued_datetime
            
    
    def add_appointments(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        issued_datetime = data.get('datetime')
        status = data.get('status')
        diagnose = data.get('diagnose')
        notes = data.get('notes')

        if not all([patient_id, doctor_id, datetime, status, status]):
            return jsonify({"error": "Missing data"}), 400
        
        status = self.set_status(status)

        try:
            if PatientModel.query.get(patient_id) is None:
                return jsonify({"error": "Patient not found"}), 404
                
                
            doctor = DoctorModel.query.get(doctor_id)
            if doctor is None:
                return jsonify({"error": "Doctor not found"}), 404

            appointment = AppointmentsModel(patient_id=patient_id, doctor_id=doctor_id, datetime=issued_datetime, status=status, diagnose=diagnose, notes=notes)
            
            if self.validate_time_appointment(doctor, None, issued_datetime) == False:
                return jsonify({"error": "Time choosen is not valid"}), 404
            
            db.session.add(appointment)
            db.session.commit()

            return appointment.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def get_appointments(self):
        try:
            appointments = AppointmentsModel.query.all()
            
            response = {"appointment":[appointment.to_response() for appointment in appointments]}

            return response, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_appointment_by_id(self, appointment_id):
        try:
            appointment = AppointmentsModel.query.get(appointment_id)
            if appointment is None:
                return jsonify({"error": "Appointment not found"}), 404

            return appointment.to_response(), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def update_appointment(self, appointment_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        appointment_by_id = AppointmentsModel.query.get(appointment_id)
        if appointment_by_id is None:
            return jsonify({"error": "Appointment not found"}), 404

        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        issued_datetime = data.get('datetime')
        status = data.get('status')
        diagnose = data.get('diagnose')
        notes = data.get('notes')
        
        try:
            appointment = AppointmentsModel.query.get(appointment_id)
            if patient_id is not None:
                if PatientModel.query.get(patient_id) is None:
                    return jsonify({"error": "Patient not found"}), 404
                appointment.patient_id = patient_id
                
            if doctor_id is not None:
                doctor = DoctorModel.query.get(doctor_id)
                if doctor is None:
                    return jsonify({"error": "Doctor not found"}), 404
                appointment.doctor_id = doctor_id

            if issued_datetime is not None:
                if self.validate_time_appointment(doctor, appointment.datetime, issued_datetime) == False:
                    return jsonify({"error": "Time choosen is not valid"}), 404
                else:
                    appointment.datetime = issued_datetime

            if status is not None:
                appointment.status = self.set_status(status)
            if diagnose is not None:
                appointment.diagnose = diagnose
            if notes is not None:
                appointment.notes = notes
                
            db.session.add(appointment)
            db.session.commit()

            return appointment.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete_appointment(self, appointment_id):
        try:
            appointment = AppointmentsModel.query.get(appointment_id)
            if appointment is None:
                return jsonify({"error": "Appointment not found"}), 404
            
            db.session.delete(appointment)
            db.session.commit()

            return jsonify({"message": "Appointment is deleted"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500