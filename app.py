import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("TMP Marché Interbancaire BAM")

url = "https://www.bkam.ma/fr/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire"

# Récupération de la page et parsing
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
table = soup.find("table")

# Lecture du tableau
df = pd.read_html(str(table))[0]

# Nettoyage colonnes
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Taux Moyen Pondéré"] = df["Taux Moyen Pondéré"].astype(str).str.replace("%","").str.replace(",",".")
df["Taux Moyen Pondéré"] = pd.to_numeric(df["Taux Moyen Pondéré"], errors='coerce')
df = df.dropna(subset=["Date","Taux Moyen Pondéré"])

# Sélection des dates
date_debut = st.date_input("Date début", value=pd.to_datetime("2020-01-01"))
date_fin = st.date_input("Date fin", value=pd.to_datetime("2023-12-31"))

if st.button("Afficher les données"):

    # TMP filtré par période
    df_filtre = df[
        (df["Date"] >= pd.to_datetime(date_debut)) &
        (df["Date"] <= pd.to_datetime(date_fin))
    ].sort_values("Date")

    if df_filtre.empty:
        st.warning("⚠️ Aucun TMP trouvé pour la période sélectionnée.")
    else:
        # Afficher TMP journalier
        st.subheader("TMP journalier")
        st.dataframe(df_filtre)

        # TMP agrégé par mois
        df_mensuel = df_filtre.groupby(df_filtre["Date"].dt.to_period("M"))["Taux Moyen Pondéré"].mean().reset_index()
        df_mensuel["Date"] = df_mensuel["Date"].dt.to_timestamp()

        st.subheader("TMP agrégé par mois")
        st.dataframe(df_mensuel)

        # Graphiques
        st.subheader("Graphique TMP journalier")
        st.line_chart(df_filtre.set_index("Date")["Taux Moyen Pondéré"])

        st.subheader("Graphique TMP mensuel")
        st.line_chart(df_mensuel.set_index("Date")["Taux Moyen Pondéré"])
