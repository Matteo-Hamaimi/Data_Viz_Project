import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px


with st.sidebar:
    # mettre le logo de l'équipe de France
    #centre le logo
    st.image("https://tse2.mm.bing.net/th?id=OIP.GoxZaGF05VIHSAc2qpfnygHaLd&pid=Api&P=0&h=220", width=100)

    st.write("## Menu")
    st.write("**French sports facilities**")
    st.write("What are the challenges and objectives of the facilities for the 2024 Olympic Games?")
    st.write("This app will help you understand the challenges of the installations for the Olympic Games 2024 and their environmental impact.")
    st.write("## About the author")
    st.write("Matteo Hamaimi - 20200763")
    st.write("#datavz2023efrei")
    st.write("Supervised by [MATHEW Mano Joseph](https://www.linkedin.com/in/manomathew/)")
    # mettre le lien linkedin
    st.write("## Contact : Follow me on LinkedIn and Github")
    st.write("[Linkedin](https://www.linkedin.com/in/matteo-hamaimi-a315391b7/)")
    # mettre le lien github
    st.write("[Github](https://github.com/Matteo-Hamaimi)")
    # mettre le lien du logo de EFREI
    st.image("https://www.efrei.fr/wp-content/uploads/2022/01/LOGO_EFREI-PRINT_EFREI-WEB.png", width=100)


# Charger les données
path = "2020_Installations.xlsx"
# lire le fichier excel avec pandas
installations = pd.read_excel(path)
# Supprimez les colonnes spécifiées
columns_to_drop = ['DepLib', 'ComInsee', 'InsCodePostal', 'InsArrondissement', 'InsPartLibelle', 'InsMultiCommune', 'InsGardiennee']
installations = installations.drop(columns_to_drop, axis=1)
# Supprimer les lignes avec des valeurs manquantes
installations = installations.dropna()
installations['InsNbPlaceParking'] = installations['InsNbPlaceParking'].astype(int)
# Remove DepCode 2A and 2B
installations = installations[~installations['DepCode'].isin(['2A', '2B'])]


st.title('Census of sports equipment, spaces and practice sites')

st.subheader("Description")

st.write("The national census of all sports facilities, spaces and practice sites constitutes one of the priority actions carried out by the ministry responsible for sports. The approach undertaken aims to enable good shared knowledge of existing facilities and sites and to help achieve a better perception of territorial inequalities in their distribution. This is a prerequisite for any prospective land-use planning approach.")

st.markdown("""
            ### Dataset Column Descriptions:

            - **DepCode**: Department code (e.g., '01' for Ain).
            - **ComLib**: Commune name (e.g., 'Abergement-Clémenciat').
            - **InsNumeroInstall**: Identifier for the installation.
            - **InsNom**: Name of the installation (e.g., 'Stade Municipal').
            - **InsAdresse**: Address of the installation.
            - **InsAccessibiliteHandiMoteur**: Accessibility for motor disabilities (e.g., Yes/No).
            - **InsAccessibiliteHandiSens**: Accessibility for sensory disabilities (e.g., Yes/No).
            - **InsAccessibiliteAucun**: No accessibility provisions (e.g., Yes/No).
            - **InsInternat**: Indicates if there is boarding available (e.g., Yes/No).
            - **InsNbLit**: Number of beds available if boarding.
            - **InsNbPlaceParking**: Number of parking spaces available.
            - **InsNbPlaceParkingHandi**: Number of parking spaces available for the handicapped.
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


st.write(installations.head())

# Create a checkbox to show the columns dropped
if st.button('Show the columns dropped'):
    st.markdown("""
        - **DepLib**: Name of the department (e.g., 'Ain').
        - **ComInsee**: INSEE code of the commune.
        - **InsCodePostal**: Postal code of the installation.
        - **InsArrondissement**: Arrondissement of the installation.
        - **InsPartLibelle**: Partial name or label of the installation.
        - **InsMultiCommune**: Indicates if the installation spans multiple communes (e.g., Yes/No).
        - **InsEmpriseFonciere**: Land area of the installation.
        - **InsGardiennee**: Indicates if the installation is guarded or supervised (e.g., Yes/No).
    """)


# Titre
st.title('Analysis of number of infrastructures by department')

st.subheader("Number of Infrastructures by Department")
# Compter le nombre d'infrastructures par département
count_by_dep = installations['DepCode'].value_counts().reset_index()
count_by_dep.columns = ['DepCode', 'Number of Infrastructures']

# Create a temporary dataframe for plotting
temp_count_by_dep = count_by_dep.copy()
# Convert 'DepCode' in the temporary dataframe to string type
temp_count_by_dep['DepCode'] = temp_count_by_dep['DepCode'].astype(str)

# Sidebar selection
range_option = st.selectbox(
    'Choose the department range:',
    ('Metropolitan France', 'France overseas')
)

# Filter data based on selection using the temporary dataframe
if range_option == 'Metropolitan France':
    filtered_data = temp_count_by_dep[(temp_count_by_dep['DepCode'].astype(int) >= 0) & (temp_count_by_dep['DepCode'].astype(int) <= 100)]
else:
    filtered_data = temp_count_by_dep[(temp_count_by_dep['DepCode'].astype(int) >= 970) & (temp_count_by_dep['DepCode'].astype(int) <= 1000)]

# Sort departments by number of infrastructures
sorted_data = filtered_data.sort_values(by="Number of Infrastructures", ascending=True)

# Create a horizontal bar chart
fig = px.bar(sorted_data,
             x='Number of Infrastructures',
             y='DepCode',
             orientation='h',
             title=f'Number of Infrastructures by Department ({range_option})',
             labels={'DepCode': 'Department Code', 'Number of Infrastructures': 'Count'},
             color='Number of Infrastructures',
             color_continuous_scale=px.colors.sequential.Viridis,
             height=800)

# Remove y-axis numerical ticks
fig.update_yaxes(showticklabels=True, ticks="")

# Display the plotly chart in Streamlit
st.plotly_chart(fig)




# Titre de la page
st.subheader('Map of the number of Infrastructures by Department')

# Charger les données géographiques des départements d'Île-de-France à partir du fichier GeoJSON
ile_de_france = gpd.read_file("departements.geojson")

# Effectuer une analyse pour obtenir le nombre d'infrastructures par département
departements_data = installations.groupby('DepCode').size().reset_index(name='NumberOfInfrastructures')

# Renommer la colonne 'DepCode' en 'CodeDepartement'
departements_data = departements_data.rename(columns={'DepCode': 'code'})

# Fusionner les données géographiques et les données sur les infrastructures en utilisant 'DepCode'
ile_de_france = ile_de_france.merge(departements_data, on='code', how='left')

# Créer la carte choroplèthe
fig = px.choropleth(
    ile_de_france, # Utilisez le GeoDataFrame en tant que source de données
    geojson=ile_de_france.geometry, # Utilisez la colonne 'geometry' pour définir la géométrie des polygones
    locations=ile_de_france.index, # Utilisez l'index du GeoDataFrame pour définir les emplacements
    color='NumberOfInfrastructures', # Utilisez la colonne que vous souhaitez visualiser
    hover_name=ile_de_france['code'],  # Utilisez la colonne que vous souhaitez afficher au survol
    center={"lat": 48.8566, "lon": 2.3522},  # Coordonnées pour centrer la carte sur Paris
    color_continuous_scale='Reds'  # Palette de couleurs
)

# Ajuster la carte aux limites de la France
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

st.title('Analysis of number of transport')

st.subheader("Average Means of Transport Available")

# Sélectionner uniquement les colonnes liées au transport
columns_transport = [
    'InsTransportMetro', 'InsTransportBus', 'InsTransportTram',
    'InsTransportTrain', 'InsTransportBateau', 'InsTransportAutre', 'InsTransportAucun'
]

# Calculer la moyenne des colonnes de transport
transport_means = installations[columns_transport].mean()

# Noms des différents modes de transport
transport_labels = ['Métro', 'Bus', 'Tram', 'Train', 'Bateau', 'Autre', 'Aucun']

# Créer un graphique à barres pour représenter les moyennes des moyens de transport
plt.figure(figsize=(10, 6))
plt.bar(transport_labels, transport_means, color='seagreen')
plt.title("Average Means of Transport Available")
plt.xlabel("Means of Transport")
plt.ylabel("Average")
plt.xticks(rotation=45)  # Rotation des étiquettes pour une meilleure lisibilité
plt.tight_layout()

# Afficher le graphique Matplotlib dans Streamlit
st.pyplot(plt)

st.subheader("Number of Infrastructures by Means of Transport")

transport_count = installations.groupby(['DepCode', 'InsTransportAucun']).size().unstack().fillna(0)
st.bar_chart(transport_count)

st.markdown("""
#### Explanations & Observations:
- We see that the most available means of transport are the bus and the train.
- The least available means of transport are the tram but especially the boat.
- This is normal because it is not common to do your sport by boat.
- But we see that a large part of the population travels without transport or on foot.
""")

st.title('Global Analysis of Sports Facilities in France')

st.subheader("Evolution of the Number of Infrastructures Created per Year")

# Assurez-vous que la colonne "InsDateCreation" est au format datetime
installations['InsDateCreation'] = pd.to_datetime(installations['InsDateCreation'])

# Extraire l'année à partir de la date de création
installations['CreationYear'] = installations['InsDateCreation'].dt.year

# Grouper les données par année et compter le nombre d'infrastructures créées
infrastructures_per_year = installations.groupby('CreationYear').size().reset_index(name='NombreInfrastructures')

# Créer un graphique pour visualiser l'évolution du nombre d'infrastructures créées par année
plt.figure(figsize=(14, 7))
plt.plot(infrastructures_per_year['CreationYear'], infrastructures_per_year['NombreInfrastructures'], label='Number of Infrastructures', marker='o', color='seagreen')
plt.title("Evolution of the Number of Infrastructures Created per Year")
plt.xlabel("Year")
plt.ylabel("Number of Infrastructures Created")
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Afficher le graphique Matplotlib dans Streamlit
st.pyplot(plt)

st.markdown("""
#### Explanations & Observations:
- We see that the number of infrastructures created has increased over the years.
- We see that the number of infrastructures created has increased exponentially from 2010.
- And in 2016, the number of infrastructures created reached its maximum with almost 10,000 infrastructures created.
- It can be assumed that this is due to the preparation for the 2024 Olympic Games.
- We can also assume that this is due to the increase in the sporting population.
- But in 2020, the number of infrastructures created decreased significantly due to covid.
- Finally, we can assume that the number of infrastructures created will increase in the years to come.
""")

st.subheader("Comparaison of  Infrastructures Created and Updated per Year")

# Adjusting the DepCode in installations dataframe to have a two-digit format
installations['DepCode'] = installations['DepCode'].astype(str).str.zfill(2)

# Extract year from creation and update dates
installations['CreationYear'] = pd.to_datetime(installations['InsDateCreation'], errors='coerce').dt.year
installations['UpdateYear'] = pd.to_datetime(installations['InsDateMaj'], errors='coerce').dt.year

# Group by year and count installations
creation_per_year = installations.groupby('CreationYear').size().reset_index(name='NumberCreated')
update_per_year = installations.groupby('UpdateYear').size().reset_index(name='NumberUpdated')

# Merge the two dataframes on year
trends = pd.merge(creation_per_year, update_per_year, left_on='CreationYear', right_on='UpdateYear', how='outer').fillna(0)

# Visualize the trends
plt.figure(figsize=(14, 7))
plt.plot(trends['CreationYear'], trends['NumberCreated'], label='Facilities Created', marker='o')
plt.plot(trends['UpdateYear'], trends['NumberUpdated'], label='Facilities Updates', marker='o')
plt.fill_between(trends['CreationYear'], 
                 trends['NumberCreated'], 
                 trends['NumberUpdated'], 
                 where=(trends['NumberCreated'] > trends['NumberUpdated']), 
                 facecolor='lightcoral', alpha=0.5)
plt.fill_between(trends['CreationYear'], 
                 trends['NumberCreated'], 
                 trends['NumberUpdated'], 
                 where=(trends['NumberCreated'] <= trends['NumberUpdated']), 
                 facecolor='lightblue', alpha=0.5)
plt.title("Trends in Installations Created and Updated by Year")
plt.xlabel("Year")
plt.ylabel("Number of Installations")
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
st.pyplot(plt)

st.markdown("""
#### Explanations & Observations:
- The number of installations created has been increasing over the years.
- The number of installations updated has been increasing over the years.
- The number of installations created has been greater than the number of installations updated since 2010 to 2017.
- And this is not good because some of the installations are not maintained so it is not ecological because they can be abandoned.
- The number of installations updated has been greater than the number of installations created since 2018.
""")

st.title("Analysis of the mean number of equipment")

# Categorize installations based on number of equipments
def categorize_equipments(num):
    if num < 5:
        return "Less than 5 equipments"
    elif 5 <= num < 10:
        return "5-10 equipements"
    else:
        return "More than 10 equipments"

installations['EquipementCategory'] = installations['Nb_Equipements'].apply(categorize_equipments)

# Calculate average equipment for each category
avg_equipment = installations.groupby('EquipementCategory')['Nb_Equipements'].mean().reset_index()

# Bar chart using plotly.express
fig = px.bar(avg_equipment, 
             x='EquipementCategory', 
             y='Nb_Equipements',
             title="Average number of equipment per category",
             labels={'EquipementCategory': "Equipment category", 'Nb_Equipements': 'Average number of equipment'},
             color='EquipementCategory',
             color_discrete_sequence=['red', 'green', 'blue'],
             category_orders={"EquipementCategory": ["Less than 5 equipments", "5-10 equipements"]})

st.plotly_chart(fig)

st.markdown("""
#### Explanations & Observations:
- We see that the average number of equipment per category is greater than 10.
- With a average of 14.4 for the category "More than 10 equipments".
""")


st.title("The top departement for JO 2024")

# Remove DepCode 2A and 2B
installations = installations[~installations['DepCode'].isin(['2A', '2B'])]

def generate_chart(data, category):
    # Convert data to numeric, errors='coerce' will convert invalid parsing to NaN
    data[category] = pd.to_numeric(data[category], errors='coerce')
    
    # Filter out null values
    non_null_data = data[data[category].notnull()]
    
    # Convert the column to float type to ensure proper summation
    non_null_data[category] = non_null_data[category].astype(float)
    
    # Group by department and get the sum for the selected category
    grouped_data = non_null_data.groupby('DepCode')[category].sum().reset_index()
    
    # Sort and take top 5 departments
    sorted_data = grouped_data.sort_values(by=category, ascending=False).head(5)
    
    # Create the bar chart with Plotly Express
    fig = px.bar(sorted_data, 
                 x='DepCode', 
                 y=category,
                 title=f"Top 5 departments for {category}",
                 labels={"DepCode": "Département", category: category},
                 color='DepCode',
                 height=500)
    
    # Update the layout for optimal display
    fig.update_layout(barmode='stack')
    fig.update_traces(texttemplate='%{value}', textposition='inside')
    
    return fig

# Subtitle
st.subheader('Top 5 departments for disabled people')

# Dropdown menu
categories = {
    'Access for the physically disabled': 'InsAccessibiliteHandiMoteur',
    'Number of disabled parking spaces': 'InsNbPlaceParkingHandi',
    'Access for people with sensory disabilities': 'InsAccessibiliteHandiSens',
}
option = st.selectbox(
    'Choose a category',
    list(categories.keys())
)

# Get the corresponding column name
data_category = categories[option]

# Generate the chart
fig = generate_chart(installations, data_category)

# Display the chart
st.plotly_chart(fig)

st.markdown("""
#### Explanations & Observations:
- pour
""")


# Convert InsDateCreation and InsDateMaj to datetime format
installations['InsDateCreation'] = pd.to_datetime(installations['InsDateCreation'], errors='coerce')
installations['InsDateMaj'] = pd.to_datetime(installations['InsDateMaj'], errors='coerce')

# Filter data for installations created or updated after 2015
installations = installations[
    (installations['InsDateCreation'] > '2015-01-01') | 
    (installations['InsDateMaj'] > '2015-01-01')
]


# Group by department and aggregate values
grouped_data = installations.groupby('DepCode').agg({
    'InsAccessibiliteAucun': 'sum',
    'InsNbPlaceParking': 'sum',
    'InsNbLit': 'sum',
    'InsTransportAucun': 'sum'
}).reset_index()

# Create scatter plot
fig = px.scatter(grouped_data, 
                 x='InsAccessibiliteAucun', 
                 y='InsNbPlaceParking',
                 size='InsNbLit',
                 color='InsTransportAucun',
                 hover_name='DepCode',
                 title="Best departments to host the Olympics (Facilities created or updated after 2015)",
                 labels={
                     'InsAccessibiliteAucun': "Accessibility (less is better)",
                     'InsNbPlaceParking': "Parking spaces",
                     'InsNbLit': "Number of beds",
                     'InsTransportAucun': "Transportation restrictions (less is better)"
                 },
                 color_continuous_scale=px.colors.sequential.Plasma_r)  # Use a reversed color scale

# Display the scatter plot
st.plotly_chart(fig)

st.markdown("""
#### Legend :
- The x-axis represents accessibility (where less is better).
- The y-axis shows the number of parking spaces.
- The size of the points is proportional to the number of beds available.
- The color of the dots represents transportation restrictions, where a cooler color (towards purple) indicates fewer restrictions and a warmer color (towards yellow) indicates more restrictions.
- They were all created or renovated after 2015
""")

st.markdown("""
#### Explanations & Observations:
- The majority of departments have accessibility ratings between 0 and 500 and offer up to 40k parking spaces.
- A few departments stand out with exceptionally high parking availability, reaching up to 60k spaces, despite varied accessibility ratings.
- The size of the dots suggests that most departments, especially those clustered around the lower accessibility ratings, provide a significant number of beds.
- Departments with cooler colored dots, indicating fewer transportation restrictions, are scattered across the accessibility scale, while warmer colored dots, indicating more restrictions, are concentrated more towards the higher accessibility ratings.
""")

st.title("Conclusion")

st.markdown("""
- The rise in sports installations from 2010-2017 likely anticipates the 2024 Olympics.
- Since 2018, updating existing facilities has been prioritized, indicating sustainable practices.
- The 2020 dip in infrastructure creation, likely due to COVID, emphasizes adaptable infrastructure needs.
- High use of buses and trains for facility access supports eco-friendly transit choices.
- Disparities in sports facility numbers across regions highlight the need for balanced development.
""")