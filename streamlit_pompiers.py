import streamlit as st
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator


date_debut=datetime.strptime("2023-01-01","%Y-%m-%d").date()
date_fin=datetime.now().date()
pd.set_option('display.max_columns', None)

df_merged=pd.read_pickle('./data_transformees/df_merge.pkl')
df_sample=df_merged.sample(n=100)
gb = GridOptionsBuilder.from_dataframe(df_merged)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection('multiple')
gridOptions = gb.build()
gridOptions['defaultColDef']['width']= 150

agree = st.checkbox('l agree' ) 
if agree:
    st.write('Great!')


st.sidebar.title("Sommaire")
pages=["Présentation du projet, du contexte et des enjeux","Exploration des données", "Analyse et visualisation des données", "Analyse & Visualisation des corrélations entre variables / choix des cactéristiques pertinentes avant modélisation", "Preprocessing des données","Modélisation et Analyse des résultats", "Prédictions sur de nouvelles données", "Conclusions métier", "Perspectives d'amélioration"]
page=st.sidebar.radio("Aller vers la page :",pages)
if page == pages[0]:
    st.write("### Présentation du projet et du Contexte")
    st.write("L’objet de ce projet est l’analyse des temps de réponse de la Brigade des Pompiers de Londres.")
    st.write("La London Fire Brigade (abrégé LFB) est le cinquième plus grand corps de sapeurs-pompiers dans le monde avec près de 6 000 employés dont environ 5 000 sapeurs-pompiers professionnels. ")
    st.write("La brigade des pompiers de Londres est le service d'incendie et de sauvetage le plus actif du Royaume-Uni et l'une des plus grandes organisations de lutte contre l'incendie et de sauvetage au monde.")
    st.write("La brigade des pompiers de Londres compte en 2023  :")
    st.write("* Un personnel de 5850 personnes")
    st.write("*	102 casernes de pompiers terrestres, réparties dans les différents arrondissements de Londres")
    st.write("*	142 camions de pompiers stratégiquement placés dans tous les arrondissements de Londres")
    st.image("images/Carte_incidents_Londres_par_IncidentCategory_2023.png")
    
elif page == pages[1]:
    st.write("### Exploration des données")
    # st.dataframe(df_merged.head(10), width=1200, height=300)
    AgGrid(df_sample, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=False)
    st.write("Dimensions du dataframe :")
    st.write(df_sample.shape)
    if st.checkbox("Afficher les valeurs manquantes"):
         st.dataframe(df_sample.isna().sum(), width=700)
    
elif page == pages[2]:
    st.write("### Analyse des données")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.set_style('whitegrid')
    title_font = {
        'fontsize': 14, 
        'fontweight': 'bold', 
    }
    df = df_merged.drop_duplicates(subset='IncidentNumber') 
    sns.countplot(data=df, x='CalYear', hue='CalYear', palette=sns.color_palette("bright", 16), legend=False)
    ax.set_xlabel("Année", fontsize=15)
    ax.set_ylabel("Nb d'incidents", fontsize=15)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.xaxis.set_major_locator(FixedLocator(range(len(df['CalYear'].unique()))))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.title("Nombre d'incidents par année sur la période 2009-2024", 
              **title_font,
              loc='left')
    plt.subplots_adjust(top=0.85)
    st.pyplot(fig)
    
elif page == pages[3]:
    st.title("Analyse & Visualisation des corrélations entre variables / choix des cactéristiques pertinentes avant modélisation")
    st.header("Heatmap de Corrélation entre variables") 
elif page == pages[4]:
    st.write("### Preprocessing des données")
elif page == pages[5]:
    st.write("### Modélisation et Analyse des résultats")
elif page == pages[6]:
    st.write("### Prédictions sur de nouvelles données")
elif page == pages[7]:
    st.write("### Conclusions métier")
elif page == pages[8]:
    st.write("### Perspectives d'amélioration")
             

