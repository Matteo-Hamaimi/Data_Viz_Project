import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px

st.title('Recensement des équipements sportifs, espaces et sites de pratiques')

st.write("**Description**")
st.write("Le recen­se­ment natio­nal de l’inté­gra­lité des équipements spor­tifs, espa­ces et sites de pra­ti­ques cons­ti­tue l’une des actions prio­ri­tai­res conduite par le ministère chargé des sports. La démar­che enga­gée a pour objec­tif de per­met­tre une bonne connais­sance partagée des équipements et sites existants et d’aider à une meilleure perception des inégali­tés ter­ri­to­ria­les dans leur répar­ti­tion. C'est un élément préalable à toute démarche prospective d'aménagement du territoire.")

st.markdown("""
            ### Dataset Column Descriptions:

            - **DepCode**: Department code (e.g., '01' for Ain).
            - **ComLib**: Commune name (e.g., 'Abergement-Clémenciat').
            - **InsNumeroInstall**: Identifier for the installation.
            - **InsNom**: Name of the installation (e.g., 'Stade Municipal').
            - **InsAdresse**: Address of the installation.
            - **InsAccessibiliteHandiMoteur**: Accessibility for motor disabilities (e.g., Yes/No).
            - **InsAccessibiliteHandiSens**: Accessibility for sensory disabilities (e.g., Yes/No).
            - **InsInternat**: Indicates if there is boarding available (e.g., Yes/No).
            - **InsNbLit**: Number of beds available if boarding.
            - **InsNbPlaceParking**: Number of parking spaces available.
            - **InsEmpriseFonciere**: Land area of the installation.
            - **InsTransportMetro**: Accessibility by metro (e.g., Yes/No).
            - **InsTransportBus**: Accessibility by bus (e.g., Yes/No).
            - **InsTransportTram**: Accessibility by tram (e.g., Yes/No).
            - **InsTransportTrain**: Accessibility by train (e.g., Yes/No).
            - **InsTransportBateau**: Accessibility by boat (e.g., Yes/No).
            - **InsTransportAutre**: Other means of transport accessibility.
            - **InsTransportAucun**: No transport accessibility (e.g., Yes/No).
            - **InsDateMaj**: Date of the last update (in YYYY-MM-DD format).
            - **InsDateCreation**: Date of creation (in YYYY-MM-DD format).
            - **Nb_Equipements**: Number of equipment at the installation.

            """)


# Charger les données
path = "2020_Installations.xlsx"
# lire le fichier excel avec pandas
installations = pd.read_excel(path)
# Exploration des données et prétraitement
# Supprimez les colonnes spécifiées
st.write("**Suppresion des colonnes inutiles et suppresion des Valeurs manquantes dans l'ensemble de données des Installations**")
columns_to_drop = ['DepLib', 'ComInsee', 'InsCodePostal', 'InsArrondissement', 'InsPartLibelle', 'InsMultiCommune', 'InsAccessibiliteAucun', 'InsNbPlaceParkingHandi', 'InsGardiennee']
installations = installations.drop(columns_to_drop, axis=1)
installations = installations.dropna()
st.write(installations.head())

# Fusionnez ou joignez les ensembles de données si nécessaire pour combiner des informations pertinentes
# Exemple : data_fusionnee = pd.merge(installations, equipements, on='colonne_commune')

# D'autres étapes de prétraitement des données peuvent inclure des conversions de types de données, un changement de nom de colonne, etc.

# Maintenant, vous pouvez passer à la définition de questions spécifiques que vous souhaitez aborder dans votre application Streamlit.





# Chargez vos données à partir d'un fichier CSV ou utilisez votre DataFrame
# data = pd.read_csv('votre_fichier.csv')

# Créer une liste des 10 plus grandes villes de France avec leurs codes de département
# Titre et sous-titre
st.title('Global analysis')
st.subheader('Plot du nombre d\'Infrastructures par Département')
count_by_dep = installations['DepCode'].value_counts().reset_index()
count_by_dep.columns = ['DepCode', 'Nombre d\'Infrastructures']
plt.figure(figsize=(30,10))
sns.barplot(x='DepCode', y='Nombre d\'Infrastructures', data=count_by_dep)
plt.title('Nombre d\'Infrastructures par Département') 
# Display the Seaborn plot in Streamlit
st.pyplot(plt)
# Titre de la page
st.subheader('Map du nombre d\'Infrastructures par Département')

# Charger les données géographiques des départements d'Île-de-France à partir du fichier GeoJSON
ile_de_france = gpd.read_file("departements.geojson")

# Effectuer une analyse pour obtenir le nombre d'infrastructures par département
departements_data = installations.groupby('DepCode').size().reset_index(name='NombreInfrastructures')

# Renommer la colonne 'DepCode' en 'CodeDepartement'
departements_data = departements_data.rename(columns={'DepCode': 'code'})

# Fusionner les données géographiques et les données sur les infrastructures en utilisant 'DepCode'
ile_de_france = ile_de_france.merge(departements_data, on='code', how='left')

# Créer la carte choroplèthe
fig = px.choropleth(
    ile_de_france,
    geojson=ile_de_france.geometry,
    locations=ile_de_france.index,
    color='NombreInfrastructures',
    hover_name=ile_de_france['code'],  # Utilisez la colonne que vous souhaitez afficher au survol
    center={"lat": 48.8566, "lon": 2.3522},  # Coordonnées pour centrer la carte sur Paris
    color_continuous_scale='Reds'  # Palette de couleurs
)

fig.update_geos(fitbounds="locations", visible=False)

# Afficher la carte dans Streamlit
st.plotly_chart(fig)


st.markdown("""
#### Explanations & Observations:
- The graph illustrates a notable variation in the number of sports facilities across the different French departments.
- Some departments stand out for having a high number of infrastructures, suggesting a greater priority or investment in sport.
- Other departments appear to be under-resourced, indicating territorial inequalities in the distribution of sports facilities.
- Departments hosting the 2024 Olympics may show an upward trend, reflecting preparation for upcoming events.
""")


