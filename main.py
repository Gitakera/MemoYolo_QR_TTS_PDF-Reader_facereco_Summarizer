import streamlit as st
import os
import sys
import cv2
import json
import pandas as pd
import threading
import smtplib
import numpy as np
import PyPDF2
import sqlite3

folder_path = os.path.abspath("objectreco/")
sys.path.append(folder_path)
from server import get_db_connection, fetch_plates, send_email_alert
from datetime import datetime
from ultralytics import YOLO
from p_ocr import paddle_ocr
from s_db import save_to_database
from streamlit_option_menu import option_menu
from gtts import gTTS
from gtts.lang import tts_langs
from io import BytesIO
from PIL import Image


from init_db import init_db
from user_request import save_user_to_db, load_users_from_db
from facereco import encode_face, match_face
from qrcode_gen import generate_qr_code
from opencv_run import get_video_frame
from pdf_player import read_pdf
from sumaa import summar_txt



def apply_custom_css():
    st.markdown("""
        <style>
        .css-18e3th9 {padding: 2rem 1rem;}
        .stButton>button {background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;}
        .stButton>button:hover {background-color: #45a049;}
        </style>
    """, unsafe_allow_html=True)


def main():
    apply_custom_css()

    st.title("IA IS-INFO M2 FC année 2024-2025")
    
    with st.sidebar:
        choice = option_menu("Andoniaina 1760 GL", ["Register", "Login", "TP integration (3)", "MiniProjet 1"], 
        icons=['person-bounding-box', 'door-open', 'app', 'bi-camera-video'], menu_icon="cast", default_index=1)
        # choice
        if st.session_state.get("authenticated"):   
            st.subheader(f"Logged in as , {st.session_state['username']}!")
            st.button("Logout", on_click=lambda: st.session_state.clear())
    init_db()

    if choice == "Register":
        st.subheader("Register")
        username = st.text_input("Enter your username")
        # On capture button, do
        if st.button("Capture Face"):
            frame = get_video_frame()
            if frame is not None:
                st.image(frame, channels="BGR", caption="Captured Frame")
                encoding = encode_face(frame)

                if encoding is not None:
                    # Convert encoding to a binary format for storage
                    encoding_blob = encoding.tobytes()
                    save_user_to_db(username, encoding_blob)
                else:
                    st.error("No face detected. Please try again.")
            else:
                st.error("Unable to access the webcam. Make sure it is connected.")

    elif choice == "Login":
        st.subheader("Login")
        users = load_users_from_db()
        known_usernames = [user[0] for user in users]
        known_encodings = [np.frombuffer(user[1]) for user in users]

        if st.button("Capture Face"):
            frame = get_video_frame()
            if frame is not None:
                st.image(frame, channels="BGR", caption="Captured Frame")
                encoding = encode_face(frame)

                if encoding is not None:
                    match_index = match_face(encoding, known_encodings)
                    if match_index >= 0:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = known_usernames[match_index]
                        st.success(f"Welcome back, {st.session_state['username']}!")
                    else:
                        st.error("Face not recognized. Please try again or register.")
                else:
                    st.error("No face detected. Please try again.")
            else:
                st.error("Unable to access the webcam. Make sure it is connected.")

    elif choice == "TP integration (3)":
        if st.session_state.get("authenticated"):
            
            st.write("Generate a customized QR Code by entering text and adjusting the settings below.")
            text = st.text_input("Enter text for QR code")
            box_size = st.slider("Box Size", min_value=5, max_value=20, value=10)
            border = st.slider("Border", min_value=1, max_value=10, value=4)
            fill_color = st.color_picker("QR Code Color", "#000000")
            back_color = st.color_picker("Background Color", "#FFFFFF")
            logo_file = st.file_uploader("Upload a Logo (optional)", type=["png", "jpg", "jpeg"])

            logo = None
            if logo_file:
                logo = Image.open(logo_file)

            if st.button("Generate QR Code"):
                if text.strip():
                    qr_image = generate_qr_code(
                        text,
                        box_size=box_size,
                        border=border,
                        fill_color=fill_color,
                        back_color=back_color,
                        logo=logo,
                    )
                    buffer = BytesIO()
                    qr_image.save(buffer, format="PNG")
                    st.image(buffer.getvalue(), caption="Generate QR Code", use_container_width=True)
                    st.download_button("Download QR Code", buffer, file_name="qrcode.png")
                else:
                    st.error("Please enter some text to generate a QR code.")
         
            st.title("PDF Reader - gTTS ")
            # Upload PDF file to tts
            pdf_file = st.file_uploader("Upload PDF", type="pdf")
            # when upload is done
            textofpdf = ""
            if pdf_file:
                option = st.selectbox(
                    "Select PDF language?",
                    ("fr", "en", "other"),
                    index=None,
                    placeholder="Select speech language...",
                )
                usedlanguage = option
                
                if option == "other":
                    # Display supported languages
                    supported_languages = tts_langs()
                    st.write("Supported languages: ", ", ".join(f"{k} ({v})" for k, v in supported_languages.items()))
                    usedlanguage = st.text_input("Your language here")
                    
                st.write("You selected:", usedlanguage)
                
                textofpdf = read_pdf(pdf_file,usedlanguage)
                
            summar_txt(textofpdf)
            
            
        else:
            st.warning("Please log in (or register before) to access this feature.")
    elif choice == "MiniProjet 1":
        if st.session_state.get("authenticated"):
            st.write("TImplementation of object detection system to control car parking access")
         
            # Navigation menu
            menu = st.sidebar.radio("Platereco Menu", ["Detect", "Admin", "Reports", "SMTP Configuration"])

            # Admin Page
            if menu == "Admin":
                st.subheader("Admin Panel")

                with st.form("add_plate_form"):
                    plate_number = st.text_input("License Plate Number")
                    list_type = st.radio("List Type", ("authorized", "blacklisted"))
                    submitted = st.form_submit_button("Add Plate")

                    if submitted and plate_number:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT OR IGNORE INTO plates (plate_number, list_type) VALUES (?, ?)",
                            (plate_number, list_type)
                        )
                        conn.commit()
                        conn.close()
                        st.success(f"Plate '{plate_number}' added to {list_type} list.")

                search_query = st.text_input("Search Plates (leave empty to view all):")
                conn = get_db_connection()
                cursor = conn.cursor()
                if search_query:
                    cursor.execute(
                        "SELECT plate_number, list_type FROM plates WHERE plate_number LIKE ? OR list_type LIKE ?",
                        (f"%{search_query}%", f"%{search_query}%")
                    )
                else:
                    cursor.execute("SELECT plate_number, list_type FROM plates")
                records = cursor.fetchall()
                conn.close()
                st.table(records)

                for plate_number, _ in records:
                    if st.button(f"Delete Plate {plate_number}"):
                        conn = get_db_connection()
                        cursor.execute("DELETE FROM plates WHERE plate_number = ?", (plate_number,))
                        conn.commit()
                        conn.close()
                        st.success(f"Plate '{plate_number}' deleted.")

            # Configuration Page
            elif menu == "Configuration":
                st.subheader("Email Settings")
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT smtp_server, smtp_port, email_address, email_password FROM email_settings")
                settings = cursor.fetchone()
                conn.close()

                with st.form("email_settings_form"):
                    smtp_server = st.text_input("SMTP Server", value=settings[0] if settings else "")
                    smtp_port = st.number_input("SMTP Port", value=settings[1] if settings else 587)
                    email_address = st.text_input("Email Address", value=settings[2] if settings else "")
                    email_password = st.text_input("Email Password", value=settings[3] if settings else "", type="password")
                    submitted = st.form_submit_button("Save Settings")

                    if submitted:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM email_settings")
                        cursor.execute(
                            "INSERT INTO email_settings (smtp_server, smtp_port, email_address, email_password) VALUES (?, ?, ?, ?)",
                            (smtp_server, smtp_port, email_address, email_password)
                        )
                        conn.commit()
                        conn.close()
                        st.success("Email settings saved.")

            # Reports Page
            elif menu == "Reports":
                st.subheader("Generate Reports")
                conn = get_db_connection()
                df = pd.read_sql_query("SELECT * FROM LicensePlates", conn)
                conn.close()

                st.dataframe(df)  # Display the report in a table format

                if st.button("Download Report"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="license_plate_report.csv",
                        mime="text/csv"
                    )

            # Detection Page
            elif menu == "Detect":
                st.write("Choose a video source for license plate detection.")

                # Video source options
                video_source = st.radio("Select video source", ("Webcam", "IP Camera", "File"))

                video_path = None
                if video_source == "File":
                    video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
                    if video_file:
                        video_path = os.path.join("temp_video.mp4")
                        with open(video_path, "wb") as f:
                            f.write(video_file.read())
                elif video_source == "IP Camera":
                    ip_url = st.text_input("Enter IP camera URL")
                    if ip_url:
                        video_path = ip_url
                elif video_source == "Webcam":
                    video_path = 0

                # Processing button
                if st.button("Start Processing"):
                    if video_path is None and video_source != "Webcam":
                        st.error("Please provide a valid video source.")
                    else:
                        # Load YOLO model
                        model = YOLO("objectreco/weigths/yolo.pt")

                        # Fetch authorized and blacklisted plates from the database
                        authorized, blacklisted = fetch_plates()

                        # Attempt to open the video source
                        cap = cv2.VideoCapture(video_path)
                        if not cap.isOpened():
                            st.error(f"Could not open video source '{video_path}'.")
                            st.stop()

                        # Create a folder to save frames
                        frames_dir = "frames"
                        os.makedirs(frames_dir, exist_ok=True)

                        # Track processed license plates and batch database writes
                        processed_plates = set()
                        data_batch = []
                        BATCH_SIZE = 1
                        SAVE_INTERVAL = 3  # Save interval in seconds
                        last_saved_time = {}

                        # Streamlit display for video frames
                        stframe = st.empty()

                        while True:
                            ret, frame = cap.read()
                            if not ret:
                                break

                            # Run YOLO detection on the frame
                            results = model.predict(frame, conf=0.45)

                            for result in results[0].boxes:
                                x1, y1, x2, y2 = map(int, result.xyxy[0])
                                confidence = result.conf[0]

                                # Only process high-confidence detections
                                if confidence >= 0.6:
                                    cropped = frame[y1:y2, x1:x2]  # Crop the detected region
                                    label = paddle_ocr(cropped)  # Run OCR on the cropped region

                                    if label:
                                        current_time = datetime.now()

                                        # Save only if interval has passed
                                        if label not in processed_plates or (datetime.now() - last_saved_time.get(label, current_time)).seconds >= SAVE_INTERVAL:
                                            last_saved_time[label] = current_time
                                            processed_plates.add(label)

                                            # Check plate status
                                            if label in authorized:
                                                alert = "Access Granted"
                                            elif label in blacklisted:
                                                alert = "Access Denied"
                                                send_email_alert(label, alert)
                                            else:
                                                alert = "Unknown Plate"

                                            # Save the frame
                                            timestamp = current_time.strftime("%Y%m%d%H%M%S%f")
                                            frame_path = os.path.join(frames_dir, f"{label}_{timestamp}.jpg")
                                            cv2.imwrite(frame_path, frame)

                                            # Add to batch for database writing
                                            entry = {
                                                "start_time": current_time.isoformat(),
                                                "end_time": current_time.isoformat(),
                                                "license_plate": label,
                                                "frame_path": frame_path,
                                                "alert": alert,
                                            }
                                            data_batch.append(entry)

                                            # Display alert in Streamlit
                                            st.warning(alert)

                                            # Write batch to database
                                            if len(data_batch) >= BATCH_SIZE:
                                                save_to_database(data_batch)
                                                st.json(data_batch)  # Display batch as JSON in Streamlit
                                                data_batch.clear()

                                        # Draw bounding box and label
                                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                                        cv2.putText(
                                            frame, label, (x1, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                                        )

                            # Display the frame in Streamlit
                            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

                            # Stop the video if 'q' is pressed
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        # Save any remaining data to the database
                        if data_batch:
                            save_to_database(data_batch)
                            st.json(data_batch)

                        cap.release()
                        st.success("Processing complete.")

        else:
            st.warning("Please log in (or register before) to access this feature.")

if __name__ == "__main__":
    main()