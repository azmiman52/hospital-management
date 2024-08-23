from models import db, EmployeeModel, GenderEnum
from flask import request, jsonify
import hashlib


class EmployeeApi:

    def __init__(self) -> None:
        pass

    def set_gender(self, gender):
        if(gender.upper() == "MALE"):
            return GenderEnum.MALE
        elif (gender.upper() == "FEMALE"):
            return GenderEnum.FEMALE
        else:
            return  GenderEnum.MALE

    def set_password(self, password):
        hashString = hashlib.new('sha256')
        hashString.update(password.encode())
        return hashString.hexdigest()

    def add_employee(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        birthdate = data.get('birthdate')

        if not all([name, username, password, gender, birthdate]):
            return jsonify({"error": "Missing data"}), 400
            
        if EmployeeModel.query.filter_by(username=username).first():
            return jsonify({"error": "Employee with this username is already exist"}), 409

        gender = self.set_gender(gender)

        password = self.set_password(password)

        try:
            employee = EmployeeModel(name=name, username=username, password=password, gender=gender, birthdate=birthdate)
            db.session.add(employee)
            db.session.commit()

            return employee.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def get_employees(self):
        try:
            employees = EmployeeModel.query.all()

            response = {"employees":[employee.to_response() for employee in employees]}

            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def get_employee_by_id(self, employee_id):
        try:
            employee = EmployeeModel.query.get(employee_id)
            if employee is None:
                return jsonify({"error": "Employee not found"}), 404

            return employee.to_response(), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def get_employee_by_username(self, username):
        try:
            employee = EmployeeModel.query.filter_by(username=username).first()
            if employee is None:
                return jsonify({"error": "Employee not found"}), 404

            return employee.to_response()
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def update_employee(self, employee_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data not provided"}), 400

        employee_by_id  = EmployeeModel.query.get(employee_id)
        if employee_by_id is None:
            return jsonify({"error": "Employee not found"}), 404

        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        birthdate = data.get('birthdate')
        work_start_time = data.get('work_start_time')
        work_end_time = data.get('work_end_time')

        employee_by_username = EmployeeModel.query.filter_by(username=username).first() 
        if employee_by_username and employee_by_username.username != employee_by_id.username:
            return jsonify({"error": "Employee with this username is already exist"}), 409

        try:
            employee = EmployeeModel.query.get(employee_id)
            if name is not None:
                employee.name = name
            if username is not None:
                employee.username = username
            if password is not None:
                employee.password = self.set_password(password)
            if gender is not None:
                employee.gender = self.set_gender(gender)
            if birthdate is not None:
                employee.birthdate = birthdate
            if work_start_time is not None:
                employee.work_start_time = work_start_time
            if work_end_time is not None:
                employee.work_end_time = work_end_time
            
            db.session.add(employee)
            db.session.commit()

            return employee.to_response(), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete_employee(self, employee_id):
        try:
            employee = EmployeeModel.query.get(employee_id)
            if employee is None:
                return jsonify({"error": "Employee not found"}), 404

            db.session.delete(employee)
            db.session.commit()

            return jsonify({"message": "Employee is deleted"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500