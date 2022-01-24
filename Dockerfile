
FROM python:3.8
#ADD . /python-flask
WORKDIR /Flask_applications/Patient_app
COPY . ./ 
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ./patient_app2.py
CMD ["python3", "./patient_app2.py"]
#FROM python:3 

#WORKDIR /Flask_applications/patient_app 

#COPY . ./ 
#EXPOSE 5000
#RUN test ! -e requirements.txt || pip install --no-cache-dir -r requirements.txt 

#ENTRYPOINT patient_app2.py
#CMD ["python3", "patient_app2.py"]
#CMD gunicorn --workers=10 --bind=127.0.0.0:5000 patient_app2:app
