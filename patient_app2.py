from flask import Flask, render_template,request,jsonify
from flask.helpers import url_for
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import BindParameter
from sqlalchemy.sql.sqltypes import Integer
from werkzeug.utils import redirect

from models import Patient,Medication,Measurement,Allergy
from sqlalchemy import text,func,extract 
from get_db import db,app

@app.route('/')
def home_page():
    return jsonify(hello='world')

########################### Patients API ####################################

@app.route('/patients', methods=['GET'])
def get_patients():
    result=db.session.query(Patient.patient_id,Patient.first_name,Patient.last_name,Patient.date_of_birth,extract('year', func.age(Patient.date_of_birth)).label("Age")).all()
    result=[{
        "patient_id":patient.patient_id,
        "first_name":patient.first_name,
        "last_name":patient.last_name,
        "date_of_birth":patient.date_of_birth,
        "Age":patient.Age
    } for patient in result]
    return jsonify({"Patients":result})

@app.route('/patients_sql',methods=['GET'])
def get_patients_sql():
    query=text('SELECT * FROM patient')
    data=db.session.execute(query)
    result=[Patient.json(patient) for patient in data]
    return jsonify({"Patients":result})
#------------------------------------------------------------------------------#

@app.route('/patients/<int:patient_id>',methods=['GET'])
def get_patient_by_id(patient_id):
    patient=Patient.json(Patient.query.filter_by(patient_id=patient_id).first())
    return jsonify({"Patients":patient})

@app.route('/patients_sql/<int:patient_id>',methods=['GET'])
def get_patients_sql_by_id(patient_id):
    query=text('SELECT * FROM patient where patient_id = :id')
    data=db.session.execute(query,{"id":patient_id})
    result=[Patient.json(patient) for patient in data]
    return jsonify({"Patients":result})
#------------------------------------------------------------------------------#

@app.route('/patients',methods=['POST'])
def add_patient():
    request_data=request.get_json()
    newPatient = Patient(request_data['first_name'],request_data['last_name'],request_data['date_of_birth'])
    db.session.add(newPatient)
    db.session.commit() 
    response={"Msg":"Patient added"}
    return response

@app.route('/patients_sql',methods=['POST'])
def add_patient_sql():
    request_data=request.get_json()
    query=text('INSERT INTO patient(first_name,last_name,date_of_birth) VALUES(:fname,:lname,:dob)')
    db.session.execute(query,{"fname":request_data['first_name'],"lname":request_data['last_name'],"dob":request_data['date_of_birth']})
    db.session.commit() 
    response={"Msg":"Patient added"}
    return response

#-------------------------------------------------------------------------------------#

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

@app.route('/patients_sql/<int:patient_id>',methods=['PUT'])
def update_patient_sql(patient_id):
    updated_data=request.get_json()
    val={"fname":updated_data['first_name'],"lname":updated_data['last_name'],
        "dob":updated_data['date_of_birth'],"id":patient_id}
    query=text('UPDATE patient SET first_name=:fname,last_name=:lname,date_of_birth=:dob WHERE patient_id=:id')
    db.session.execute(query,val)
    db.session.commit()
    return jsonify({"Msg":"Patient updated"})

#-----------------------------------------------------------------------------------#
@app.route('/patients/<int:patient_id>',methods=['DELETE'])
def delete_patient(patient_id):
    Patient.query.filter_by(patient_id=patient_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Patient deleted"})

@app.route('/patients_sql/<int:patient_id>',methods=['DELETE'])
def delete_patient_sql(patient_id):
    query=text('DELETE FROM patient WHERE patient_id=:id')
    db.session.execute(query,{"id":patient_id})
    db.session.commit()
    return jsonify({"Msg":"Patient deleted"})

############################## Medication API ###########################

@app.route('/medications',methods=['GET'])
def medications():
    result=[Medication.json(med) for med in Medication.query.all()]
    return jsonify({"Medications":result})

@app.route('/medications_sql',methods=['GET'])
def medications_sql():
    query=text('SELECT * FROM medication')
    data=db.session.execute(query)
    result=[Medication.json(med) for med in data]
    return jsonify({"Medications":result})
#----------------------------------------------------------------------#

@app.route('/medications/<int:med_id>',methods=['GET'])
def get_medication_by_id(med_id):
    medication=Medication.json(Medication.query.filter_by(med_id=med_id).first())
    return jsonify({"Medications":medication})

@app.route('/medications_sql/<int:med_id>',methods=['GET'])
def get_medication_sql_by_id(med_id):
    query=text('SELECT * FROM medication where med_id = :id')
    data=db.session.execute(query,{"id":med_id})
    result=[Medication.json(patient) for patient in data]
    return jsonify({"Medications":result})

#-----------------------------------------------------------------------#
@app.route('/medications',methods=['POST'])
def add_medication():
    request_data=request.get_json()
    newMed = Medication(request_data['med_name'],request_data['dose'],request_data['frequency'],request_data['intake_type'],request_data['patient_id'])
    db.session.add(newMed)
    db.session.commit() 
    response={"Msg":"Medication added"}
    return response

@app.route('/medications_sql',methods=['POST'])
def add_medication_sql():
    request_data=request.get_json()
    query=text('INSERT INTO medication(med_name,dose,frequency,intake_type,patient_id) VALUES(:mname,:dose,:frq,:intake,:pid)')
    val={"mname":request_data['med_name'],
        "dose":request_data['dose'],
        "frq":request_data['frequency'],
        "intake":request_data['intake_type'],
        "pid":request_data['patient_id']}
    db.session.execute(query,val)
    db.session.commit() 
    response={"Msg":"Medication added"}
    return response
#-----------------------------------------------------------------------#
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

@app.route('/medications_sql/<int:med_id>',methods=['PUT'])
def update_medication_sql(med_id):
    updated_data=request.get_json()
    val={"mname":updated_data['med_name'],"dose":updated_data['dose'],
        "frq":updated_data['frequency'],"pid":updated_data['patient_id'],"mid":med_id}
    query=text('UPDATE medication SET med_name=:mname,dose=:dose,frequency=:frq,patient_id=:pid WHERE med_id=:mid')
    db.session.execute(query,val)
    db.session.commit()
    return jsonify({"Msg":"Medication updated"})
#-------------------------------------------------------------------------------------------#
@app.route('/medications/<int:med_id>',methods=['DELETE'])
def delete_medication(med_id):
    Medication.query.filter_by(med_id=med_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Medication deleted"})

@app.route('/medications_sql/<int:med_id>',methods=['DELETE'])
def delete_medication_sql(med_id):
    query=text('DELETE FROM medication WHERE med_id=:id')
    db.session.execute(query,{"id":med_id})
    db.session.commit()
    return jsonify({"Msg":"Medication deleted"})
################################ Measurement API ################################


@app.route('/measurements',methods=['GET'])
def measurements():
    result=[Measurement.json(mes) for mes in Measurement.query.all()]
    return jsonify({"Measurements":result})

@app.route('/measurements_sql',methods=['GET'])
def measurements_sql():
    query=text('SELECT * FROM measurement')
    data=db.session.execute(query)
    result=[Measurement.json(mes) for mes in data]
    return jsonify({"Measurements":result})

#------------------------------------------------------------------------------------#

@app.route('/measurements/<int:measure_id>',methods=['GET'])
def get_measurement_by_id(measure_id):
    measurement=Measurement.json(Measurement.query.filter_by(measure_id=measure_id).first())
    return jsonify({"Measurements":measurement})

@app.route('/measurements_sql/<int:measure_id>',methods=['GET'])
def get_measurement_sql_by_id(measure_id):
    query=text('SELECT * FROM measurement where measure_id = :id')
    data=db.session.execute(query,{"id":measure_id})
    result=[Measurement.json(patient) for patient in data]
    return jsonify({"Measurements":result})

#-----------------------------------------------------------------------------#
@app.route('/measurements',methods=['POST'])
def add_measurement():
    request_data=request.get_json()
    newMes = Measurement(request_data['measure_name'],request_data['unit'],request_data['value'],request_data['patient_id'])
    db.session.add(newMes)
    db.session.commit() 
    response={"Msg":"Measurement added"}
    return response

@app.route('/measurements_sql',methods=['POST'])
def add_measurement_sql():
    request_data=request.get_json()
    query=text('INSERT INTO measurement(measure_name,unit,value,patient_id) VALUES(:mname,:unit,:value,:pid)')
    db.session.execute(query,{"mname":request_data['measure_name'],"unit":request_data['unit'],"value":request_data['value'],"pid":request_data['patient_id']})
    db.session.commit() 
    response={"Msg":"Measurement added"}
    return response

#-----------------------------------------------------------------------------#
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

@app.route('/measurements_sql/<int:measure_id>',methods=['PUT'])
def update_measurement_sql(measure_id):
    updated_data=request.get_json()
    val={"mname":updated_data['measure_name'],
        "unit":updated_data['unit'],
        "value":updated_data['value'],
        "pid":updated_data['patient_id'],
        "mid":measure_id}
    query=text('UPDATE measurement SET measure_name=:mname,unit=:unit,value=:value,patient_id=:pid WHERE measure_id=:mid')
    db.session.execute(query,val)
    db.session.commit()
    return jsonify({"Msg":"Measurement updated"})

#-----------------------------------------------------------------------------------#

@app.route('/measurements/<int:measure_id>',methods=['DELETE'])
def delete_measurement(measure_id):
    Measurement.query.filter_by(measure_id=measure_id).delete()
    db.session.commit()
    return jsonify({"Msg":"Measurement deleted"})

@app.route('/measurements_sql/<int:measure_id>',methods=['DELETE'])
def delete_measurement_sql(measure_id):
    query=text('DELETE FROM measurement WHERE med_id=:id')
    db.session.execute(query,{"id":measure_id})
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

@app.route('/fetchall_sql',methods=['GET'])  
def fetch_all_sql_data_of_patients():
    query=text('SELECT patient.patient_id,patient.first_name,patient.last_name,medication.med_id,medication.med_name,measurement.measure_name FROM patient INNER JOIN medication ON patient.patient_id=medication.patient_id INNER JOIN measurement ON patient.patient_id=measurement.patient_id')   
    result=db.session.execute(query)
    data=[
        {
            "patient_id":row.patient_id,
            "first_name":row.first_name,
            "last_name":row.last_name,
            "med_id":row.med_id,
            "med_name":row.med_name,
            "measure_name":row.measure_name,
            
        } 
        for row in result
        ]
        
    return jsonify({"all patient data":data})
    
#---------------------------------------------------------------------------------------#
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
        
@app.route('/fetchall_sql/<int:id>',methods=['GET'])  
def fetch_all_sql_data_of_patients_with_id(id):
    query=text('SELECT patient.patient_id,patient.first_name,patient.last_name,medication.med_id,medication.med_name,measurement.measure_name FROM patient INNER JOIN medication ON patient.patient_id=medication.patient_id INNER JOIN measurement ON patient.patient_id=measurement.patient_id WHERE patient.patient_id=:id')   
    result=db.session.execute(query,{"id":id})
    data=[
        {
            "patient_id":row.patient_id,
            "first_name":row.first_name,
            "last_name":row.last_name,
            "med_id":row.med_id,
            "med_name":row.med_name,
            "measure_name":row.measure_name,
            
        } 
        for row in result
        ]
        
    return jsonify({"all patient data":data})

#----------------------------------------------------------------------------------#
#search patient by first_name
@app.route('/search/<string:fname>',methods=['GET'])  
def fetch_all_sql_data_of_patients_with_fname(fname):
    query=text('SELECT patient.patient_id,patient.first_name,patient.last_name,medication.med_id,medication.med_name,measurement.measure_name FROM patient INNER JOIN medication ON patient.patient_id=medication.patient_id INNER JOIN measurement ON patient.patient_id=measurement.patient_id WHERE patient.first_name=:fname')   
    result=db.session.execute(query,{"fname":fname})
    data=[
        {
            "patient_id":row.patient_id,
            "first_name":row.first_name,
            "last_name":row.last_name,
            "med_id":row.med_id,
            "med_name":row.med_name,
            "measure_name":row.measure_name,
            
        } 
        for row in result
        ]
        
    return jsonify({"all patient data with name %s"%fname:data})

#search patient by med_name
@app.route('/search_medication/<string:med_name>',methods=['GET'])  
def fetch_all_sql_data_of_patients_with_med_name(med_name):
    query=text('SELECT patient.patient_id,patient.first_name,patient.last_name,patient.date_of_birth,medication.med_id,medication.med_name,measurement.measure_name FROM patient INNER JOIN medication ON patient.patient_id=medication.patient_id INNER JOIN measurement ON patient.patient_id=measurement.patient_id WHERE medication.med_name=:mname')   
    result=db.session.execute(query,{"mname":med_name})
    data=[
        {
            "patient_id":row.patient_id,
            "first_name":row.first_name,
            "last_name":row.last_name,
            "date_of_birth":row.date_of_birth,
            "med_id":row.med_id,
            "med_name":row.med_name,
            "measure_name":row.measure_name,
            
        } 
        for row in result
        ]
        
    return jsonify({"all patient data using medication  %s"%med_name:data}) 

#list all patients with their age in asending order
@app.route('/list_age',methods=['GET'])  
def fetch_all_sql_data_of_patients_with_age():
    result=db.session.query(Patient.patient_id,Patient.first_name,Patient.last_name,Patient.date_of_birth,Medication.med_id,Medication.med_name,Measurement.measure_name,extract('year', func.age(Patient.date_of_birth)).label("Age")).select_from(Patient).join(Medication).join(Measurement).all()
    data=[
        {
            "patient_id":row.patient_id,
            "first_name":row.first_name,
            "last_name":row.last_name,
            "Age":row.Age,
            "med_id":row.med_id,
            "med_name":row.med_name,
            "measure_name":row.measure_name,
            
        } 
        for row in result
        ]
        
    return jsonify({"all patient data in ascending order of age":data}) 

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)