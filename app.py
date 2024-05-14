import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


df_sector = pd.read_csv("data/emission_sectors.csv")
df_ghg = pd.read_csv("data/emission_gases.csv")
df_eco = pd.read_csv("data/emission_economiques.csv")
df_import = pd.read_csv("data/emission_importation.csv")
df_eco.iloc[:,1:] = df_eco.iloc[:,1:].div(1000).astype('float')
df_import.iloc[:,1:] = df_import.iloc[:,1:].div(1000).astype('float')

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

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)
with st.sidebar:
    st.sidebar.image("data/shifters.png", width=150)

st.sidebar.write(
    """





    """
)

option = st.sidebar.selectbox(
    'Choisissez une option',
    ('Fiche technique', 'Quelles mesures implémenter?','Visualisation graphique')
)


if option == 'Fiche technique':
    st.sidebar.write(
        """
        ### Description
        Cette application a été créée par le groupe de travail [Shift Ta Commune](https://www.theshifters.ch/shift-ta-commune) des Shifters Switzerland. 
        Elle vise à montrer un exemple de visualisation interactive des données d'émissions d'une région (ici la Suisse).

        **Notre objectif est de modifier cet outil pour fournir à chaque commune suisse qui le souhaite une visualisation d'ensemble de ses émissions, afin d'aider dans la mise en place de mesures visant à leur diminution.**

        Si vous êtes intéressé à adapter cet outil à vos données communales, veuillez contacter Shift Ta Commune [ici](https://www.theshifters.ch/shift-ta-commune).
        """
    )
    st.markdown("### **Fiche Technique de la Suisse**")

    # Using HTML and CSS to create a structured and visually appealing box to display the data
    components.html("""
<div style="
    display: flex;
    gap: 20px;
    justify-content: center;
    align-items: start;
    flex-wrap: wrap;
">
    <div style="
        border:2px solid #8fb1aa;
        border-radius: 15px;
        padding: 20px;
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        width: 40%;
        max-width: 100%;
        margin-bottom: 20px;
    ">
        <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 0.5em; color: #2c3e50;">👤 Informations Générales</div>
        <div style="margin-bottom: 1.5em; font-size: 1.1em;">
            <span style="font-weight: bold; color: #2980b9;">Habitants (2022):</span> 8.8154 Millions
        </div>
    </div>

    <div style="
        border:2px solid #8fb1aa;
        border-radius: 15px;
        padding: 20px;
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        width: 40%;
        max-width: 100%;
        margin-bottom: 20px;
    ">
        <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 0.5em; color: #2c3e50;">☁ Émissions en 2021</div>
        <div style="margin-bottom: 1.5em; font-size: 1.1em;">
            <span style="font-weight: bold; color: #2980b9;">Total:</span> 45.25 millions de tonnes eq-CO2 
        </div>
    </div>

    <div style="
        border:2px solid #8fb1aa;
        border-radius: 15px;
        padding: 20px;
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        width: 40%;
        max-width: 100%;
        margin-bottom: 20px;
    ">
        <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 0.5em; color: #2c3e50;">📊 Comparaison avec 2016</div>
        <div style="margin-bottom: 1.5em; font-size: 1.1em;">
            <span style="font-weight: bold; color: #2980b9;">Différence 2016-2021:</span> <span style="color: #228B22;">-8.28%</span>
        </div>
    </div>

    <div style="
        border:2px solid #8fb1aa;
        border-radius: 15px;
        padding: 20px;
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        color: #333;
        width: 40%;
        max-width: 100%;
        margin-bottom: 20px;
    ">
        <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 0.5em; color: #2c3e50;">📊 Comparaison avec 2020</div>
        <div style="margin-bottom: 1.5em; font-size: 1.1em;">
            <span style="font-weight: bold; color: #2980b9;">Différence 2020-2021:</span> <span style="color: #e74c3c;">+1.03%</span> 
        </div>
    </div>
</div>
        """, height=340, width=800)
    st.write("Si vous êtes intéressés d'en savoir plus, sélectionner l'onglet ***Quelles mesures implémenter?*** ou l'onglet ***Visualisation graphique***!")
    
elif option == 'Quelles mesures implémenter?':

    # Line Chart for CO2 Augmentation/Diminution
    st.subheader("Augmentation/Diminution des Emissions CO2 par secteur (%)")
    years_to_compare = st.multiselect("Sélectionner 2 dates pour comparer (le calcul du pourcentage se fait toujours par rapport à la date la plus récente):", list(range(1990, 2022)), default=[2020, 2021])
    available_sectors = list(df_sector.columns)[2:]
    sectors_to_display = st.multiselect("Sélectionner les secteurs à afficher:", available_sectors, default=available_sectors)
    if len(years_to_compare) == 2:
        years_to_compare.sort() 
        compare_data = df_sector[df_sector['Year'].isin(years_to_compare)]
        compare_data = compare_data.set_index('Year').transpose()
        compare_data['% Change'] = (compare_data[years_to_compare[1]] - compare_data[years_to_compare[0]]) / compare_data[years_to_compare[0]] * 100
        compare_data = compare_data.loc[sectors_to_display]
        sector_to_improve = compare_data['% Change'].idxmax()

        fig_line = px.line(compare_data.reset_index(), x='index', y='% Change', title='Percentage Change in CO2 Emissions', labels={'index': 'Sector'})
        st.plotly_chart(fig_line)
        if sector_to_improve == 'Services (bâtiments)':
            link = "https://kdrive.infomaniak.com/app/drive/591131/files/3455/preview/pdf/3515"
        elif sector_to_improve == 'Ménages (bâtiments)':
            link = "https://kdrive.infomaniak.com/app/drive/591131/files/3455/preview/pdf/3515"
        elif sector_to_improve == 'Agriculture':
            link = "https://kdrive.infomaniak.com/app/drive/591131/files/3455/preview/pdf/3512"
        elif sector_to_improve == 'Transports':
            link = "https://kdrive.infomaniak.com/app/drive/591131/files/3455/preview/pdf/3514"
        else:
            link = "https://www.theshifters.ch/shift-ta-commune"
        st.write(
            f"""
            Le secteur **{sector_to_improve}** voit la plus grande augmentation entre ces deux dates, d'une valeur de **{round(compare_data.loc[sector_to_improve]['% Change'],2)}%**.

            Pour aider dans l'implémentation de mesures afin de réduire les émissions CO2 de ce secteur, le groupe de travail Shift Ta Commune a créé une fiche technique correspondante.
            Vous pouvez la consulter [à cette adresse]({link}). 

            Si vous êtes redirigés vers le site des Shifters Switzerland, c'est que la fiche que vous recherchez n'est pas encore finie.
            Le groupe travaille dessus et sera mise en ligne par la suite.

            """)
    else:
        st.warning('Veuillez sélectionner exactement 2 dates pour effectuer la comparaison.')
    
    st.sidebar.write(
            """
            Comme expliqué sur le site [Shift Ta Commune](https://www.theshifters.ch/shift-ta-commune), les actions déclinées selon le type de communes (urbaines, rurales, montagnardes) sont sélectionnées dans les domaines suivants:
            - Bâtiments, logements, rénovations
            - Économie circulaire, utilisation de matériaux locaux, production locale d'aliments
            - Valorisation des déchets
            - Économies d'énergie
            - Mobilité, multimodalité, transfert modal
            - Covoiturage
            - Sensibilisation des employés communaux et des administrés.


            Les livrables fournis aux communes consistent en autant de fiches techniques que de mesures proposées détaillant ces dernières et la manière de les mettre en œuvre.
            Toutes les fiches se trouvent [ici](https://kdrive.infomaniak.com/app/drive/591131/files/3455)."""
        )
    st.sidebar.write("**Source des données:** [Office Fédéral de la Statistique](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.html)")
else:
    year_range = st.sidebar.slider("Sélectionner une plage de dates", 1990, 2021, (1990, 2021))

    st.sidebar.write("**Source des données:** [Office Fédéral de la Statistique](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.html)")

    filtered_data_sector = df_sector[(df_sector["Year"] >= year_range[0]) & (df_sector["Year"] <= year_range[1])]
    filtered_data_ghg = df_ghg[(df_ghg["Year"] >= year_range[0]) & (df_ghg["Year"] <= year_range[1])]
    filtered_data_eco = df_eco[(df_eco["Year"] >= year_range[0]) & (df_eco["Year"] <= year_range[1])]
    filtered_data_import = df_import[(df_import["Year"] >= year_range[0]) & (df_import["Year"] <= year_range[1])]

    
    # Sector Emissions Graph
    st.subheader("Emissions Gaz à Effet de Serre en Suisse par Secteur (Million tons eq-CO2)")
    fig_sector = px.bar(filtered_data_sector, x='Year', y=list(df_sector.columns)[2:])
    st.plotly_chart(fig_sector)
    st.write("###### *Source*: [Emissions de gaz à effet de serre en Suisse. Evolution en équivalents CO2 et émissions par secteur](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.assetdetail.25085617.html)")

    # Greenhouse Gas Types Graph
    st.subheader("Emissions intérieures de Gaz à Effet de Serre en Suisse (Million tons eq-CO2)")
    fig_ghg = px.bar(filtered_data_ghg, x='Year', y=list(df_ghg.columns)[2:-1])
    st.plotly_chart(fig_ghg)
    st.write("###### *Source*: [Emissions de gaz à effet de serre en Suisse. Evolution en équivalents CO2 et émissions par secteur](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.assetdetail.25085617.html)")

    # Economic Emissions Graph
    st.subheader("Emissions Gaz à Effet de Serre en Suisse par Secteur Economique (Million tons eq-CO2)")
    fig_eco = px.bar(filtered_data_eco, x='Year', y=['Secteur tertiaire','Secteur secondaire','Secteur primaire'])
    st.plotly_chart(fig_eco)
    st.write("###### *Note: Total gaz à effet de serre, incl. CO2 biomasse*")
    st.write("###### *Source*: [Comptes des émissions dans l'air des ménages et de l'économie, par secteurs économiques](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.assetdetail.27705285.html)")

    # Economic Emissions Graph
    st.subheader("Emissions de Gaz à Effet de Serre en Suisse liées à l'Importation (Million tons eq-CO2)")
    fig_import = px.bar(filtered_data_import, x='Year', y=['Émissions liées aux importations', 'Émissions intérieures'])
    st.plotly_chart(fig_import)
    st.write("###### *Note: La quantité totale de gaz à effet de serre émis pour satisfaire la demande finale de biens et de services en Suisse*")
    st.write("###### *Source*: [Empreinte gaz à effet de serre – Émissions de gaz à effet de serre induites par la demande intérieure finale – Millions de tonnes d'équivalents CO2](https://www.bfs.admin.ch/bfs/fr/home/statistiques/espace-environnement/indicateurs-environnement/tous-les-indicateurs/emissions-et-dechets/emissions-gaz-effet-de-serre.assetdetail.27705362.html)")






