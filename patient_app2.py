from flask import Flask, render_template,request,jsonify
from flask.helpers import url_for
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from models import Patient,Medication,Measurement,Allergy
from get_db import db,app

@app.route('/')
def home_page():
    return jsonify(hello='world')

########################### Patients API ####################################

@app.route('/patients', methods=['GET'])
def get_patients():
    result=[Patient.json(patient) for patient in Patient.query.all()]
    return jsonify({"Patients":result})


@app.route('/patients/<int:patient_id>',methods=['GET'])
def get_patient_by_id(patient_id):
    patient=Patient.json(Patient.query.filter_by(patient_id=patient_id).first())
    return jsonify({"Patients":patient})


@app.route('/patients',methods=['POST'])
def add_patient():
    request_data=request.get_json()
    newPatient = Patient(request_data['first_name'],request_data['last_name'],request_data['date_of_birth'])
    db.session.add(newPatient)
    db.session.commit() 
    response={"Msg":"Patient added"}
    return response


@app.route('/patients/<int:patient_id>',methods=['PUT'])
def update_patient(patient_id):
    updated_data=request.get_json()
    patient=Patient.query.filter_by(patient_id=patient_id).first()
    patient.first_name = updated_data['first_name']
    patient.last_name = updated_data['last_name']
    patient.date_of_birth = updated_data['date_of_birth']
    print(patient.first_name," ",patient.last_name," ",patient.date_of_birth)
    db.session.commit()
    return jsonify({"Msg":"Patient updated"})


@app.route('/patients/<int:patient_id>',methods=['DELETE'])
def delete_patient(patient_id):
    Patient.query.filter_by(patient_id=patient_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Patient deleted"})


############################## Medication API ###########################

@app.route('/medications',methods=['GET'])
def medications():
    result=[Medication.json(med) for med in Medication.query.all()]
    return jsonify({"Medications":result})


@app.route('/medications/<int:med_id>',methods=['GET'])
def get_medication_by_id(med_id):
    medication=Medication.json(Medication.query.filter_by(med_id=med_id).first())
    return jsonify({"Medications":medication})


@app.route('/medications',methods=['POST'])
def add_medication():
    request_data=request.get_json()
    newMed = Medication(request_data['med_name'],request_data['dose'],request_data['frequency'],request_data['intake_type'],request_data['patient_id'])
    db.session.add(newMed)
    db.session.commit() 
    response={"Msg":"Medication added"}
    return response


@app.route('/medications/<int:med_id>',methods=['PUT'])
def update_medication(med_id):
    updated_data=request.get_json()
    med=Medication.query.filter_by(med_id=med_id).first()
    med.med_name = updated_data['med_name']
    med.dose = updated_data['dose']
    med.frequency = updated_data['frequency']
    med.intake_type = updated_data['intake_type']
    med.patient_id = updated_data['patient_id']
    db.session.commit()
    return jsonify({"Msg":"Medication updated"})


@app.route('/medications/<int:med_id>',methods=['DELETE'])
def delete_medication(med_id):
    Medication.query.filter_by(med_id=med_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Medication deleted"})


################################ Measurement API ################################


@app.route('/measurements',methods=['GET'])
def measurements():
    result=[Measurement.json(mes) for mes in Measurement.query.all()]
    return jsonify({"Measurements":result})


@app.route('/measurements/<int:measure_id>',methods=['GET'])
def get_measurement_by_id(measure_id):
    measurement=Measurement.json(Measurement.query.filter_by(measure_id=measure_id).first())
    return jsonify({"Measurements":measurement})


@app.route('/measurements',methods=['POST'])
def add_measurement():
    request_data=request.get_json()
    newMes = Measurement(request_data['measure_name'],request_data['unit'],request_data['value'],request_data['patient_id'])
    db.session.add(newMes)
    db.session.commit() 
    response={"Msg":"Measurement added"}
    return response


@app.route('/measurements/<int:measure_id>',methods=['PUT'])
def update_measurement(measure_id):
    updated_data=request.get_json()
    mes=Measurement.query.filter_by(measure_id=measure_id).first()
    mes.measure_name = updated_data['measure_name']
    mes.unit = updated_data['unit']
    mes.value = updated_data['value']
    mes.patient_id = updated_data['patient_id']
    db.session.commit()
    return jsonify({"Msg":"Measurement updated"})


@app.route('/measurements/<int:measure_id>',methods=['DELETE'])
def delete_measurement(measure_id):
    Measurement.query.filter_by(measure_id=measure_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Measurement deleted"})

####################### Allergy API ####################################

####################### Api to fetch all patient data ###################

@app.route('/fetchall',methods=['GET'])  
def fetch_all_data_of_patients():
    result=db.session.query(Patient,Medication,Measurement).select_from(Patient).join(Medication).join(Measurement).all()
    data=[
        {
            "patient_id":patient.patient_id,
            "first_name":patient.first_name,
            "last_name":patient.last_name,
            "date_of_birth":patient.date_of_birth,
            "med_id":medication.med_id,
            "med_name":medication.med_name,
            "dose":medication.dose,
            "frequency":medication.frequency,
            "intake_type":medication.intake_type,
            "measure_id":measurement.measure_id,
            "measure_name":measurement.measure_name,
            "unit":measurement.unit,
            "value":measurement.value
        } 
        for patient,medication,measurement in result
        ]
    return jsonify({"all patient data":data})
    

@app.route('/fetchall/<int:id>',methods=['GET'])  
def fetch_all_data_of_patient_with_id(id):
    result=db.session.query(Patient,Medication,Measurement).select_from(Patient).join(Medication).join(Measurement).filter(Patient.patient_id==id).all()
    data=[
        {
            "patient_id":patient.patient_id,
            "first_name":patient.first_name,
            "last_name":patient.last_name,
            "date_of_birth":patient.date_of_birth,
            "med_id":medication.med_id,
            "med_name":medication.med_name,
            "dose":medication.dose,
            "frequency":medication.frequency,
            "intake_type":medication.intake_type,
            "measure_id":measurement.measure_id,
            "measure_name":measurement.measure_name,
            "unit":measurement.unit,
            "value":measurement.value
        } 
        for patient,medication,measurement in result
        ]
    return jsonify({"all patient data":data})
        

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)