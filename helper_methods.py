
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("notable_app.db")
    conn.row_factory = sqlite3.Row
    return conn

def seed_database():
    # create seed data

    # first, seed the doctor information
    conn = get_db_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
    doctors = conn.execute("SELECT * FROM doctors").fetchall()

    if len(doctors) < 1:
        conn.execute("INSERT into doctors (first_name, last_name) VALUES(?, ?)", ["Purple", "Flower"])
        conn.execute("INSERT into doctors (first_name, last_name) VALUES(?, ?)", ["Orange", "Flower"])
        conn.execute("INSERT into doctors (first_name, last_name) VALUES(?, ?)", ["Yellow", "Flower"])
        conn.commit()
        conn.close()

    # then, seed patient information
    conn = get_db_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL)")
    patients = conn.execute("SELECT * FROM patients").fetchall()

    if len(patients) < 1:
        conn.execute("INSERT into patients (first_name, last_name) VALUES(?, ?)", ["Aqua", "Turtle"])
        conn.execute("INSERT into patients (first_name, last_name) VALUES(?, ?)", ["Chartreuse", "Octopus"])
        conn.execute("INSERT into patients (first_name, last_name) VALUES(?, ?)", ["Pink", "Cat"])
        conn.commit()
        conn.close()

    # then, seed the appointment information

    conn = get_db_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, patient_id INTEGER, doctor_id INTEGER, date TEXT, time TEXT, kind TEXT)")
    appointments = conn.execute("SELECT * FROM appointments").fetchall()

    patient_1_id = conn.execute("SELECT * FROM patients WHERE first_name = ?", ['Aqua']).fetchall()[0]["id"]
    patient_2_id = conn.execute("SELECT * FROM patients WHERE first_name = ?", ['Chartreuse']).fetchall()[0]["id"]
    patient_3_id = conn.execute("SELECT * FROM patients WHERE first_name = ?", ['Pink']).fetchall()[0]["id"]

    doctor_id = conn.execute("SELECT * FROM doctors").fetchall()[0]["id"]

    if len(appointments) < 1:
        conn.execute("INSERT into appointments (patient_id, doctor_id, date, time, kind) VALUES(?, ?, ?, ?, ?)", [patient_1_id, doctor_id, "20231104", "0815", "new patient"])
        conn.execute("INSERT into appointments (patient_id, doctor_id, date, time, kind) VALUES(?, ?, ?, ?, ?)", [patient_2_id, doctor_id, "20221108", "1045", "new patient"])
        conn.execute("INSERT into appointments (patient_id, doctor_id, date, time, kind) VALUES(?, ?, ?, ?, ?)", [patient_3_id, doctor_id, "20240315", "0915", "new patient"])
        conn.commit()
        conn.close()


      

