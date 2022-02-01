from get_db import db

class Patient(db.Model):

    __tablename__="patient"
    patient_id = db.Column('patient_id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)  
    date_of_birth = db.Column(db.Date,nullable=False)
    
    def __init__(self, first_name, last_name, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

    #this method will convert output to json
    def json(self):
        return {"patient_id":self.patient_id , "first_name":self.first_name ,
        "last_name":self.last_name , "date_of_birth":self.date_of_birth}

class Medication(db.Model):
    __tablename__="medication"
    med_id=db.Column("med_id",db.Integer,primary_key=True)
    med_name=db.Column(db.String(200),nullable=False)
    dose=db.Column(db.String(50),nullable=False)
    frequency=db.Column(db.Integer,nullable=False)
    intake_type=db.Column(db.String(100),nullable=False)
    patient_id=db.Column(db.Integer,db.ForeignKey("patient.patient_id"),nullable=False)

    def __init__(self,med_name,dose,frequency,intake_type,patient_id):
        self.med_name=med_name
        self.dose=dose
        self.frequency=frequency
        self.intake_type=intake_type
        self.patient_id=patient_id

    def json(self):
        return {"med_id":self.med_id,"med_name":self.med_name,
        "dose":self.dose,"frequency":self.frequency,
        "intake_type":self.intake_type,"patient_id":self.patient_id}

class Measurement(db.Model):
    __tablename__="measurement"
    measure_id=db.Column("measure_id",db.Integer,primary_key=True)
    measure_name=db.Column(db.String(100),nullable=False)
    unit=db.Column(db.String(50),nullable=False)
    value=db.Column(db.String(50),nullable=False)
    patient_id=db.Column(db.Integer,db.ForeignKey("patient.patient_id"),nullable=False)

    def __init__(self,measure_name,unit,value,patient_id):
        self.measure_name=measure_name
        self.unit=unit
        self.value=value
        self.patient_id=patient_id

    def json(self):
        return {"measure_id":self.measure_id,"measure_name":self.measure_name,
        "unit":self.unit,"value":self.value,"patient_id":self.patient_id}


class Allergy(db.Model):
    __tablename__="allergy"
    allergy_id=db.Column("allergy_id",db.Integer,primary_key=True)
    allergy_name=db.Column(db.String(100),nullable=False)
    type=db.Column(db.String(100),nullable=False)
    patient_id=db.Column(db.Integer,db.ForeignKey("patient.patient_id"),nullable=False)
    ref_id=db.Column(db.Integer,db.ForeignKey("medication.med_id") or db.ForeignKey("measurement.measure_id"),nullable=False)
