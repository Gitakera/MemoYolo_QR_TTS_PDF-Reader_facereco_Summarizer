import streamlit as st
import PyPDF2
import pyttsx3
import playsound
from gtts import gTTS


def read_pdf(pdf_file, usedlanguage):
  

  # Open the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    # Iterate through the pages and extract text
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Display the text content from the PDF
    if text:
        final_text = st.text_area("PDF Content", text, 300)
        
        # Add a button to trigger TTS
        if st.button("Convert to audio") and usedlanguage != None and usedlanguage!= "other" and len(usedlanguage) > 1 :
            with st.spinner("Generating audio..."):
                tts = gTTS(text=final_text, lang=usedlanguage)
                tts.save("reading.mp3")
                st.audio("reading.mp3", format="audio/mpeg", loop=True)
                file = open("reading.mp3", "rb")
                st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name="reading.mp3",
                        mime="audio/mpeg"
                    )
        elif usedlanguage == None or usedlanguage == "other" or len(usedlanguage) <= 1 or len(usedlanguage) >= 3:
            st.error("Please provide a correct language value before converting to audio.")
            st.toast(" Put a valid language value before converting to audio.", icon="🚨")
    else:
        st.write("Could not extract text from this PDF.")
    return final_text