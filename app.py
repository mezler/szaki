import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder
import io


api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Most már használhatod a modellt:
model = genai.GenerativeModel('gemini-1.5-flash')


st.title("🎤 Munkalap Diktáló (Google Gemini)")

audio_bytes = audio_recorder(text="Nyomd meg és diktálj!", icon_size="3x")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Munkalap generálása"):
        with st.spinner("Elemzés..."):
            # Mivel a Gemini API közvetlenül nem dolgozza fel az audió fájlt ilyen egyszerűen, 
            # a legegyszerűbb, ha a diktált szöveget kézzel írod be, VAGY
            # használod a Google saját "speech-to-text" megoldását.
            
            st.info("Megjegyzés: A Google Gemini API ingyenes, de a hangfájlokat külön kell szöveggé alakítani.")
            st.write("Ide írd be a munkát, amit diktáltál:")
            szoveg = st.text_area("Diktált szöveg:")
            
            if st.button("Generálás szövegből"):
                prompt = f"Nyerd ki a munkalap adatait ebből: {szoveg}. Válasz JSON formátumban legyen."
                response = model.generate_content(prompt)
                st.write(response.text)
