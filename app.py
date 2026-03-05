import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_tmp_bam(date_recherche):

    url = "https://www.bkam.ma/fr/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire"

    # télécharger la page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    # récupérer le tableau
    table = soup.find("table")

    # transformer en dataframe
    df = pd.read_html(str(table))[0]

    # chercher la date
    ligne = df[df["Date"] == date_recherche]

    if not ligne.empty:
        taux = ligne["Taux Moyen Pondéré"].values[0]
        print("Date :", date_recherche)
        print("Taux moyen pondéré :", taux)
        return taux
    else:
        print("Date non trouvée dans la page")
        return None


# ======================
# entrer la date ici
# ======================

date = input("Entrer la date (jj/mm/aaaa) : ")

get_tmp_bam(date)
