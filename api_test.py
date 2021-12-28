import unittest
import requests
import json
from get_db import app
class PatientApiTest(unittest.TestCase):
    API_URL="http://127.0.0.1:5000/patients"

    def test_get_patients(self):
        req = requests.get(PatientApiTest.API_URL)
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(len(data['Patients']),9)

    def test_get_patients_sql(self):
        req = requests.get("http://127.0.0.1:5000/patients_sql")
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(len(data['Patients']),9)

    def test_get_patient_by_id(self):
        req = requests.get("http://127.0.0.1:5000/patients/1")
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(len(data['Patients']),1)

    def test_get_patient_by_id_not_exist(self):
        req = requests.get("http://127.0.0.1:5000/patients/3")
        data=req.json()
        self.assertEqual(req.status_code,404)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(data['Error'],"Requested data not found")

    def test_get_patients_sql_by_id(self):
        req = requests.get("http://127.0.0.1:5000/patients_sql/1")
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(len(data['Patients']),1)

    def test_add_patient(self):
        _data={
            "date_of_birth": "Tue, 28 Oct 1999 00:00:00 GMT",
            "first_name": "Merry",
            "last_name": "Dowsan",
        }
        req = requests.post("http://127.0.0.1:5000/patients",json=_data)
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(data['Msg'],"Patient added")

    def test_update_patient(self):
        _data={
            "date_of_birth": "Tue, 25 Oct 1999 00:00:00 GMT",
            "first_name": "Merry",
            "last_name": "Dowsan",
        }
        req = requests.put("http://127.0.0.1:5000/patients/14",json=_data)
        data=req.json()
        self.assertEqual(req.status_code,200)
        assert req.headers["Content-Type"] == "application/json"
        self.assertEqual(data['Msg'],"Patient updated")


if __name__=="__main__":
    unittest.main()