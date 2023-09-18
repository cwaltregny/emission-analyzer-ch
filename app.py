import streamlit as st
import pandas as pd
import plotly.express as px

df_sector = pd.read_csv("data/emission_sectors.csv")
df_ghg = pd.read_csv("data/emission_gases.csv")

#choice = st.sidebar.radio("Select data view:", ["Sectoral Emissions", "Greenhouse Gas Types"])
st.title("Emissions de Gaz à Effet de Serre")

st.sidebar.markdown(
    """
    <style>
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """, unsafe_allow_html=True,
)

st.sidebar.markdown(
    """<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/2560px-Flag_of_Switzerland.svg.png' class='center' width='100'/>""",
    unsafe_allow_html=True,
)


st.sidebar.write(
    """





    """
)

year_range = st.sidebar.slider("Sélectionner une plage de dates", 1990, 2021, (1990, 2021))

st.sidebar.write(
    """
    ### Description
    Cette application a été créée par les Shifters Switzerland à travers l'initiative [Shift Ta Commune](https://www.theshifters.ch/shift-ta-commune). 
    Elle vise à montrer un exemple de visualisation interactive des données d'émissions d'une région (ici la Suisse).

    Notre objectif est de modifier cet outil pour fournir à chaque commune suisse qui le souhaite une visualisation d'ensemble de leurs émissions, afin d'aider dans la mise en place de mesures visant à leur diminution.
    Si vous êtes intéressé à adapter cet outil à vos données communales, veuillez contacter les Shifters Switzerland [ici](https://www.theshifters.ch/shift-ta-commune)

    **Source des données:** 
    [Office Fédéral de la Statistique](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.html)
    """
)


filtered_data_sector = df_sector[(df_sector["Year"] >= year_range[0]) & (df_sector["Year"] <= year_range[1])]
filtered_data_ghg = df_ghg[(df_ghg["Year"] >= year_range[0]) & (df_ghg["Year"] <= year_range[1])]

# Sector Emissions Graph
st.subheader("Emissions CO2 en Suisse par Secteur (Million tons)")
fig_sector = px.bar(filtered_data_sector, x='Year', y=list(df_sector.columns)[2:])
st.plotly_chart(fig_sector)

# Greenhouse Gas Types Graph
st.subheader("Emissions de Gaz à Effet de Serre en Suisse (Million tons)")
fig_ghg = px.bar(filtered_data_ghg, x='Year', y=list(df_ghg.columns)[2:-1])
st.plotly_chart(fig_ghg)


# Line Chart for CO2 Augmentation/Diminution
st.subheader("Augmentation/Diminution des Emissions CO2 par secteur (%)")
years_to_compare = st.multiselect("Sélectionner 2 dates pour comparer (le calcul du pourcentage se fait toujours par rapport à la date la plus récente):", list(range(1990, 2022)), default=[2020, 2021])
if len(years_to_compare) == 2:
    years_to_compare.sort() 
    compare_data = df_sector[df_sector['Year'].isin(years_to_compare)]
    compare_data = compare_data.set_index('Year').transpose()
    compare_data['% Change'] = (compare_data[years_to_compare[1]] - compare_data[years_to_compare[0]]) / compare_data[years_to_compare[0]] * 100
    fig_line = px.line(compare_data.reset_index(), x='index', y='% Change', title='Percentage Change in CO2 Emissions', labels={'index': 'Sector'})
    st.plotly_chart(fig_line)
else:
    st.warning('Veuillez sélectionner exactement 2 dates pour effectuer la comparaison.')
st.write("**Source des données:** [Office Fédéral de la Statistique](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.html)")
