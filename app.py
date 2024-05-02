from flask import Flask, redirect, render_template, request, jsonify
from helper_methods import get_db_connection, seed_database
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE"])
def index():
    return redirect('/doctors')


@app.route("/doctors", methods=["GET", "POST", "DELETE"])
def doctors():
    if request.method == "GET":
        conn = get_db_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
        doctors = conn.execute("SELECT * FROM doctors").fetchall()

        if len(doctors) < 1:
            seed_database()

        doctors = conn.execute("SELECT * FROM doctors").fetchall()

        # uncomment this code to render a bare bones display of doctor information

        doctorList = []

        for doctor in doctors:
            doctorList.append([
                {"id": doctor["id"]}, 
                {"first_name": doctor["first_name"]}, 
                {"last_name": doctor["last_name"]}
            ])

        # uncomment below to render a basic display of doctor information
        # return render_template("doctors.html", doctors=doctors)

        return jsonify(doctorList), 200

@app.route("/appointments", methods=["GET", "POST", "DELETE"])
def appointments():
    if request.method == "GET":
        conn = get_db_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, patient_id INTEGER, doctor_id INTEGER, kind TEXT, date TEXT, time TEXT)")
        appointments = conn.execute("SELECT * FROM appointments").fetchall()

        if len(appointments) < 1:
            seed_database()

        appointments = conn.execute("SELECT * FROM appointments").fetchall()

        # uncomment this code to render a bare bones display of doctor information

        appointmentList = []

        for appointment in appointments:
            # add query for doctor information

            patient_id = appointment["patient_id"]

            patient_first_name = conn.execute("SELECT * FROM patients WHERE id = ?", [patient_id]).fetchall()[0]["first_name"]
            patient_last_name = conn.execute("SELECT * FROM patients WHERE id = ?", [patient_id]).fetchall()[0]["last_name"]

            appointmentList.append([
                {"id": appointment["id"]}, 
                {"kind": appointment["kind"]}, 
                {"date": appointment["date"]},
                {"time": appointment["time"]},
                {"patient_first_name": patient_first_name},
                {"patient_last_name": patient_last_name},
                {"doctor_id": appointment["doctor_id"]},
            ])

        # uncomment below to render a basic display of appointment information
        # return render_template("appointments.html", appointments=appointments)

        return jsonify(appointmentList), 200
    
    if request.method == "POST":
        appointment_id = request.form.get('appointment_id')
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        time = request.form.get('time')
        date = request.form.get('date')
        kind = request.form.get('kind')
        conn = get_db_connection()

        conn.execute("INSERT INTO appointments (patient_id, doctor_id, time, date, kind) VALUES(?, ?, ?, ?, ?)", [patient_id, doctor_id, time, date, kind])
        conn.commit()
        conn.close()

        # in the future I would build this out more to only allow appointments if the time, etc. is acceptable
        return 200

    
    if request.method == "DELETE":
        appointment_id = request.form.get('id')
        conn = get_db_connection()
        conn.execute("SELECT * FROM appointments WHERE id = ?", [appointment_id])

        return 200 


@app.route("/patients", methods=["GET"])
def patients():
    if request.method == "GET":
        conn = get_db_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
        patients = conn.execute("SELECT * FROM patients").fetchall()

        if len(patients) < 1:
            seed_database()

        patients = conn.execute("SELECT * FROM patients").fetchall()

        print(patients)

        patientList = []

        for patient in patients:
            print(patient)
            patientList.append([
                {"id": patient["id"]}, 
                {"first_name": patient["first_name"]}, 
                {"last_name": patient["last_name"]}
            ])

        # uncomment below to render a basic display of patient information
        # return render_template("patients.html", patients=patients)

        return jsonify(patientList), 200
