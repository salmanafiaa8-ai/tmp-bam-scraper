import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("TMP Marché Interbancaire BAM")

url = "https://www.bkam.ma/fr/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

table = soup.find("table")

df = pd.read_html(str(table))[0]

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

date_debut = st.date_input("Date début")
date_fin = st.date_input("Date fin")

if st.button("Afficher les données"):

    df_filtre = df[
        (df["Date"] >= str(date_debut)) &
        (df["Date"] <= str(date_fin))
    ]

    st.dataframe(df_filtre)

    st.line_chart(df_filtre.set_index("Date")["Taux Moyen Pondéré"])
