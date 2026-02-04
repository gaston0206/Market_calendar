import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import io  # Pour gérer le fichier Excel en mémoire

# Configuration
st.set_page_config(page_title="Calendrier des Marchés", page_icon="🛒")

# Dictionnaires de traduction
JOURS_FR = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
}
MOIS_FR = {
    "January": "Janvier", "February": "Février", "March": "Mars", "April": "Avril",
    "May": "Mai", "June": "Juin", "July": "Juillet", "August": "Août",
    "September": "Septembre", "October": "Octobre", "November": "Novembre", "December": "Décembre"
}

st.title("🛒 Calendrier du Marché")
st.write("Générez les jours du marché.")

# --- FORMULAIRE ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        date_depart = st.date_input("Entrez une date d'animation du marché :", datetime.now())
    with col2:
        frequence = st.number_input("Période du marché (en jours) :", min_value=1, value=4)
    
    nb_occurrences = st.slider("Nombre de dates à générer :", 1, 50, 20)

st.write("---")

if st.button("🚀 GÉNÉRER LE CALENDRIER"):
    resultats = []
    date_courante = date_depart

    for i in range(nb_occurrences):
        j_en = date_courante.strftime("%A")
        m_en = date_courante.strftime("%B")
        date_formatee = f"{date_courante.day} {MOIS_FR.get(m_en, m_en)} {date_courante.year}"
        
        resultats.append({
            "N°": i + 1,
            "Jour": JOURS_FR.get(j_en, j_en),
            "Date": date_formatee
        })
        date_courante += timedelta(days=frequence)

    df = pd.DataFrame(resultats)

    # Affichage
    st.subheader("📌 Vos dates de marché :")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- CRÉATION DU FICHIER EXCEL ---
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Calendrier')
    
    # Préparation du bouton de téléchargement Excel
    st.download_button(
        label="📥 Télécharger le calendrier (EXCEL)",
        data=buffer.getvalue(),
        file_name=f"calendrier_marche_{frequence}j.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Cliquez sur le bouton pour calculer les dates.")