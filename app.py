import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from reportlab.pdfgen import canvas
import io
import json

# API Kulcs - Ide illeszd be a saját sk-... kulcsodat
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Munkalap AI", layout="centered")
st.title("🎤 Munkalap Diktáló")

# 1. Mikrofon rögzítő
audio_bytes = audio_recorder(text="Kattints ide a diktáláshoz", icon_size="3x")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Munkalap generálása"):
        with st.spinner("Feldolgozás folyamatban..."):
            # 2. Hang -> Szöveg (Whisper)
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.wav"
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            szoveg = transcription.text
            
            # 3. Szöveg -> JSON (GPT-4o mini)
            prompt = f"Nyerd ki a munkalap adatait ebből a szövegből: '{szoveg}'. JSON mezők: ugyfel, munka, ora, anyagok."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            adatok = json.loads(response.choices[0].message.content)
            
            st.success("Adatok kinyerve!")
            st.json(adatok)

            # 4. PDF generálás
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            c.drawString(100, 800, "--- MUNKALAP ---")
            c.drawString(100, 780, f"Ügyfél: {adatok.get('ugyfel')}")
            c.drawString(100, 760, f"Munka: {adatok.get('munka')}")
            c.drawString(100, 740, f"Idő: {adatok.get('ora')} óra")
            c.save()
            pdf_data = pdf_buffer.getvalue()

            # Letöltés gomb
            st.download_button("PDF Munkalap letöltése", data=pdf_data, file_name="munkalap.pdf", mime="application/pdf")
