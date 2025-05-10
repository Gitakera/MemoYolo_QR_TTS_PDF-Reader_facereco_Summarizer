import streamlit as st
import os
import cv2
import json
import pandas as pd
import threading
import smtplib
from datetime import datetime
from ultralytics import YOLO
from p_ocr import paddle_ocr
from s_db import save_to_database
from init_db import init_db
import sqlite3

# Initialize the database and tables
init_db()



# SQLite connection setup
def get_db_connection():
    return sqlite3.connect('licensePlatesDatabase.db')

def fetch_plates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plate_number, list_type FROM plates")
    records = cursor.fetchall()
    conn.close()

    authorized = {record[0] for record in records if record[1] == 'authorized'}
    blacklisted = {record[0] for record in records if record[1] == 'blacklisted'}
    return authorized, blacklisted

def send_email_alert(plate_number, alert):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT smtp_server, smtp_port, email_address, email_password FROM email_settings")
    settings = cursor.fetchone()
    conn.close()

    if not settings:
        st.error("Email settings not configured.")
        return

    smtp_server, smtp_port, email_address, email_password = settings

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            message = f"Subject: License Plate Alert\n\nAlert: {alert} for plate {plate_number}"
            server.sendmail(email_address, email_address, message)
    except Exception as e:
        st.error(f"Failed to send email: {e}")



