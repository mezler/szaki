import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# EZT A RÉSZT TEDD BE A KÓDBA IDEIGLENESEN:
st.subheader("Elérhető modellek:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        st.write(f"Modell neve: {m.name}")



# import streamlit as st
# import google.generativeai as genai

# # 1. Konfiguráció (A Secrets-ből olvassa)
# api_key = st.secrets["GEMINI_API_KEY"]
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('gemini-1.5-pro')

# st.title("🎤 Munkalap Generáló")

# # 2. Szövegbeviteli mező (Ide diktál a telefonod billentyűzetével)
# st.subheader("Diktáld vagy írd be a munkát:")
# szoveg = st.text_area("Munka részletei:", height=150, placeholder="Példa: Kovács Jánosnál klímatisztítást végeztem, 2 óra, szűrőcsere.")

# # 3. Generálás gomb (Kint van az if-en kívül, így mindig látszik)
# if st.button("Munkalap generálása"):
#     if szoveg:
#         with st.spinner("Elemzés..."):
#             # A prompt kényszeríti a magyar nyelvet és a JSON formátumot
#             prompt = f"""
#             Feladat: Nyerj ki adatokat a következő magyar szövegből.
#             Válaszod SZIGORÚAN csak JSON formátum legyen az alábbi kulcsokkal:
#             'ugyfel', 'munka', 'ido_ora', 'anyagok'.
            
#             Szöveg: {szoveg}
#             """
            
#             response = model.generate_content(prompt)
            
#             # Eredmény megjelenítése
#             st.success("Munkalap kész!")
#             st.code(response.text, language='json')
#     else:
#         st.warning("Kérlek, diktálj vagy írj be valamit először!")
