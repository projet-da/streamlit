import streamlit as st
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import pickle
import numpy as np

def color_row(row):
    if row['Classification'] == 1:
        return ['background-color: lightgreen'] * len(row)
    else:
        return [''] * len(row)

date_debut=datetime.strptime("2023-01-01","%Y-%m-%d").date()
date_fin=datetime.now().date()
pd.set_option('display.max_columns', None)

df=pd.read_pickle('./data_transformees/df3_distances_OSM_60000.pkl')
df_sample=df.sample(n=100)
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection('multiple')
gridOptions = gb.build()
gridOptions['defaultColDef']['width']= 150

st.set_page_config(page_title="Projet DA Pompiers", page_icon=":fire:", layout="wide", initial_sidebar_state="expanded")

##############################################################
# Sommaire
##############################################################
st.sidebar.title("Sommaire")
pages=["Présentation du projet, du contexte et des enjeux","Exploration des données", 
       "Analyse et visualisation des données", "Analyse & Visualisation des corrélations entre variables", 
       "Choix des caractéristiques pertinentes pour la modélisation", "Traitement des valeurs manquantes et des valeurs aberrantes/extrêmes résiduelles",
       "Modélisation / Analyse des résultats", "Prédictions sur de nouvelles données", "Conclusions métier", "Perspectives d'amélioration"]

page=st.sidebar.radio("Aller vers la page :",pages)
##############################################################
# Présentation du projet, du Contexte et des enjeux
##############################################################
if page == pages[0]:
    st.title("Analyse des temps de réponse des pompiers de Londres (LFB)")
    #st.write("### Contexte du projet")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Présentation et contexte du projet</h1>", unsafe_allow_html=True)

    texte = """<p> L’objectif de ce projet est<span style="color:orange;"> d’analyser les temps d'arrivée</span> de la Brigade des Pompiers de Londres (LFB) sur le lieu d'incident, ainsi que les incidents de type<span style="color:orange;"> 'Fausse Alarme'</span> qui représentent plus de la moitié des incidents, puis <span style="color:orange;">d'estimer les temps d'arrivée</span>.</p> """
    st.markdown(texte, unsafe_allow_html=True)
    
    texte = """<p> Les pompiers de Londres sont intervenus chaque année sur environ<span style="color:orange;"> 100 000 incidents</span>.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    
    st.image("images/Carte_incidents_Londres_par_IncidentCategory_2023.png")
    
    st.write("Pour évaluer les performances de la brigade des pompiers de Londres, des normes sont établies pour les différentes parties du processus permettant d'affecter des ressources aux incidents suite à un appel au 999.")
    
    st.write("* Process d'intervention :")
    st.image("images/shéma intervention caserne.png")
    
    st.write("Les objectifs de temps d'arrivée fixés dans le Plan 2023 de la London Fire Brigade sont les suivants :")
    texte = """<p> * Le premier camion de pompiers doit arriver sur le lieu d’incident dans<span style="color:orange;"> un délai moyen de 6 minutes</span> après mobilisation de la caserne sollicitée.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    texte = """<p> * Le deuxième camion de pompiers (si nécessaire) doit arriver dans<span style="color:orange;"> un délai moyen de 8 minutes</span>.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    
    texte = """<p> Comme nous le verrons par la suite,<span style="color:orange;"> l’emplacement des casernes et camions de pompiers</span> détermine la rapidité de réponse de la LFB.</p>"""
    st.markdown(texte, unsafe_allow_html=True)

##############################################################
# Exploration des données
##############################################################
elif page == pages[1]:
    #st.write("### Le jeu de données")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Exploration des données</h1>", unsafe_allow_html=True)
    
    texte = """<p> Pour ce projet, nous avons eu à notre disposition 2 jeux de données : un sur<span style="color:orange;"> les Incidents</span> et l'autre sur<span style="color:orange;"> les Mobilisations</span>.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    
    texte = """<p> <span style="color:orange;">* Le premier jeu de données</span> fourni, contenait les détails de chaque<span style="color:orange;"> incident</span> traité entre janvier 2009 et février 2024. Des informations étaient fournies sur la date, le lieu de l'incident ainsi que sur le type d'incident traité.Soit, 2 DataFrames.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    texte = """<p> <span style="color:orange;">* Le second jeu de données</span> fourni, contenait les détails de chaque<span style="color:orange;"> camion de pompiers mobilisé.</span> Des informations étaient fournies sur le camion mobilisé, son lieu de déploiement, les heures et délais d'arrivée sur les lieux de l'incident. Soit, 3 Dataframes.</p>"""
    st.markdown(texte, unsafe_allow_html=True)

    st.markdown("""---""")

    st.write("**1) Une première étape a consisté à comprendre le contexte et le périmètre du projet, et à découvrir et appréhender les données disponibles.**")
    texte = """<p>* Pour cela, nous avons effectué <span style="color:orange;"> des recherches sur l'organisation</span> de la LFB et sur les différentes<span style="color:orange;"> étapes du processus</span> permettant d'affecter et de mobiliser des ressources sur les incidents identifiés.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    texte = """<p>* Nous avons procédé à<span style="color:orange;"> une analyse des données disponibles</span> afin d'identifier leur signification, le type de variable (catégorielle ou quantitative, continue ou discrète).</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    texte = """<p>* Nous avons <span style="color:orange;">identifié</span> les différentes modalités/valeurs des données et leur distribution, la présence éventuelle de valeurs manquantes, de doublons ou de valeurs aberrantes.</p>"""
    st.markdown(texte, unsafe_allow_html=True)

    st.markdown("""---""")
    
    st.write("**2) Dans un second temps, nous avons travaillé sur l'exploration, la transformation, l'enrichissement, et le nettoyage des données.**")
    texte = """<p>* <span style="color:orange;">Afin de nous assurer une bonne compréhension des données</span> nous avons sollicité à quelques reprises la London Fire Brigade, en la personne de Sophie Prendergast.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    texte = """<p>* <span style="color:orange;">Pour enrichir les données,</span> nous avons recherché des fonds de carte du Grand Londres, et des fichiers comprenant des coordonées géographiques, par exemple : celles des casernes, ou celles qui permettent d'identifier si le quartier du lieu d'incident fait partie de l'Inner London ou de l'Outer London, et également de calculer la distance entre la caserne et le lieu d'incident.</p>"""
    st.markdown(texte, unsafe_allow_html=True)
    
    st.markdown("""---""")

    st.write("**3) Enfin, nous avons concaténé les différents DataFrames, pour aboutir à un DataFrame unique des données d'incident et un DataFrame unique des données de mobilisations des pompiers de Londres. Puis nous avons réunis les DataFrames des incidents et des mobilisations en les fusionnants.**")
    
    st.markdown("""---""")

    df=pd.read_pickle('data_transformees/df_merge_10000.pkl')
    # Elimine les doublons des Incidents Number
    df1=df.drop_duplicates(subset=['IncidentNumber'])
    # Créer un écahntillon de 100 lignes
    df1_sample=df.sample(n=100)
    # Afficher 10 lignes du df
    st.dataframe(df1.head(10), width=1200, height=300)
    # Dimension du df
    #st.write("* Dimensions du dataframe dédupliqué :")
    #st.write(df1.shape)

##############################################################
# Analyse et visualisations des données
##############################################################
elif page == pages[2]:
    #st.write("### Quelques visualisations")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Quelques visualisations</h1>", unsafe_allow_html=True)
    #st.markdown('<u>Ce texte est souligné</u>', unsafe_allow_html=True)

    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Evolution du nombre d'incidents de 2009 à 2024</h1></u>", unsafe_allow_html=True)
    st.image("images/Nb incidents par année de 2009 à 2024.png")
    st.write("Après une diminution entre 2009 et 2015, on constate une tendance à la hausse du nombre d'incidents à partir de 2015, à l'exception de l'année 2020, année marquée par le Covid-19.")

    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Répartition en % par catégories d'incidents</h1></u>", unsafe_allow_html=True)
    st.image("images/Incidents 2019 à 2023 en % plotly.png")
    st.write("Les False Alarm représentent en volume plus de la moitié des interventions.")
    if st.checkbox("Special Service"):
        st.write("Effectuer une entrée/sortie d'un bâtiment: 26%, Inondation : 21%, Accidents de la route : 12%, Déverouillage d'ascenseur : 5%...")

    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Histogramme par types d'incidents sur 5 ans</h1></u>", unsafe_allow_html=True)
    st.image("images/incid de 19 à 23.png")
    st.write("Les False Alarm sont en volume les plus nombreux et sont en progression sur les 4 dernières années, ainsi que les Special Service.")
    st.write("On notera encore une fois que l'année 2020 (Covid) est une année en baisse vs 2019, et peu importe la catégorie.")
    if st.checkbox("Coût par incident de 2019 à 2023"):
        st.image("images/Couts par incident de 2019 à 2023.png")
    
    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Histogramme des coûts par types d'incidents sur 5 ans</h1></u>", unsafe_allow_html=True)
    st.image("images/Couts type incidents 2019-2023.png")
    st.write("En valeur, les Fausses Alarmes et les Special Services sont en hausse sur les 4 dernières années.")
    st.write("La dimininution des False Alarm représente donc un enjeu important en terme d'économie pour la LFB.")  
    st.write("L'année 2022 est atypique pour les feux, plusieurs incendies importants ce sont déclarés entre juillet et août 2022 avec des températures inédites outre-Manche : plus de 40 degrés à Londres.") 

    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Boîtes à moustaches des temps d'intervention par types d'incidents</h1></u>", unsafe_allow_html=True)
    st.image("images/Boxplot IncidentGroup Médianes et Moyennes 2019 2023.png")
    st.write("Les médianes et les moyennes sont proches les unes des autres, cependant celles des feux sont légèrement supérieures")
    st.write("L'équipement supplémentaire mis par les pompiers pour lutter contre les feux explique la légère différence à la hausse vs les autres types d'incidents. ces chiffres remplissent le cahier des charges de la LFB, c'est à dire l'arrivée sur le lieu d'incident en moins de 6 minutes.")
    st.write("Les médianes sont respectivement de 317sec(FA), de 329sec(F) et de 314sec(SS). Les moyennes sont respectivement de 340sec(FA), de 357sec(F) et de 337sec(SS).")
    
    st.markdown("<u><h1 style='text-align: left; color: black; font-size: 26px;'>Temps d'arrivee moyen du 1er camion en fonction de la zone d'incident</h1></u>", unsafe_allow_html=True)
    st.image("images/Temps d'arrivee moyen du 1er camion en fonction de la zone d'incident (Inner-Outer London) pour chaque année sur la période de 2017 à 2023.png")
    st.write("Les interventions dans le centre de Londres (Inner) sont plus rapides que dans la périphérie (Outer), l'explication réside dans la concentration des casernes dans le centre de Londres. ")
    

                                            

##############################################################
# Analyse & Visualisation des corrélations entre variables
##############################################################
elif page == pages[3]:
    # st.title("Analyse & Visualisation des corrélations entre variables")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Analyse & Visualisation des corrélations entre variables</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Heatmap de Corrélation entre variables</h2>", unsafe_allow_html=True)
    # st.header("Heatmap de Corrélation entre variables") 
    # st.write("Afin de construire un modèle d'apprentissage automatique et de prédiction des temps d'arrivée des pompiers sur le lieu d'incident, nous avons analysé les corrélations entre les données disponibles, 
    en particulier avec le temps d'arrivée :")
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">La <strong><span style="color: orange;">heatmap</span></strong> ci-dessous permet de visualiser les <strong><span style="color: orange;">corrélations entre les différentes données</span></strong>, </p>
        <p class="custom-p">Chaque variable est représentée par une ligne et une colonne, et les cellules contiennent l'information de corrélation entre variables. </p>
        <p class="custom-p">La valeur de chaque cellule représente la force et la direction de la corrélation, plus elle est <strong><span style="color: orange;">proche de 1 (couleur rouge) plus la corrélation est forte</span></strong>, si la <strong>valeur est négative la corrélation est négative</strong>.</p>
    """, unsafe_allow_html=True)
    
    with st.expander("Détail de la Heatmap de corrélation personnalisée"):
        # st.write("* **Coefficient de corrélation de Pearson**, mesure statistique qui évalue la force (entre 0 et 1) et la direction (positive ou négative) de la relation linéaire entre deux variables quantitatives.")
        # st.write("* **Analyse de variance (ANOVA)**, test statistique destiné à comparer les moyennes d'une variable numérique entre les différentes valeurs d'une variable catégorielle. Dans le contexte de l’ANOVA, l’Eta carré (η²) et l’omega carré (ω²) sont deux indicateurs permettant de mesurer la force de l'association entre une variable catégorielle et une variable numérique.")
        # st.write("* **Test du Khi-2 et V de Cramer** : Le test Khi-2 est un test statistique destiné à évaluer l’existence d’une relation significative entre deux variables catégorielles. Le V de Cramer est indicateur basé sur le test du Khi-2 permettant de mesurer la force de l'association entre ces deux variables catégorielles.")
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <ul class="custom-ul">
            <li><strong>Coefficient de corrélation de Pearson</strong>, mesure statistique qui évalue la force (entre 0 et 1) et la direction (positive ou négative) de la relation linéaire entre <span style="color: orange;"> deux variables quantitatives</span>.</li>
            <li><strong>Analyse de variance (ANOVA)</strong>, test statistique destiné à comparer les moyennes d'une variable numérique entre les <span style="color: orange;">différentes valeurs d'une variable catégorielle.</span><br>
            Dans le contexte de l’<strong>ANOVA</strong>, <strong>l’Eta carré (η²)</strong> et <strong>l’omega carré (ω²)</strong> sont deux indicateurs permettant de mesurer la force de l'association entre <span style="color: orange;">une variable catégorielle et une variable numérique.</span></li>
            <li><strong>Test du Khi-2 et V de Cramer</strong> : Le <strong>test Khi-2</strong> est un test statistique destiné à évaluer l’existence d’une relation significative entre deux variables catégorielles.<br>
            Le <strong>V de Cramer</strong> est un indicateur basé sur le test du Khi-2 permettant de mesurer la force de l'association entre ces <span style="color: orange;">deux variables catégorielles.</li>
            </ul>
            """, unsafe_allow_html=True)

    st.image("images/Heatmap Matrice de corrélation entre variables.png")

    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
            margin-left: 20px;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p"><strong>On constate des <span style="color: orange;">corrélations très fortes (coefficient de corrélation > 0.7)</span> entre les paires de données suivantes :</strong></p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
            margin-left: 20px; 
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <ul class="custom-ul">
        <li><strong>TravelTimeSeconds</strong> (temps de trajet entre la caserne de départ et le lieu d’incident) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)<br></li></ul>
        """, unsafe_allow_html=True)
   
    col1, col2 = st.columns([1, 15])
    with col1:
        st.markdown("")
    with col2:
        with st.expander("**Pour illustrer cette corrélation**"):
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                    margin-left: 20px; 
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Pour illustrer cette corrélation, ci-dessous une visualisation sous forme de nuage de points du temps de trajet et de la distance pour l'ensemble des mobilisations du premier camion de pompiers jusqu'au lieu d'incident sur l'année 2023, en distinguant le cas où la caserne de départ se situe dans le centre de Londres (Inner London) ou dans la périphérie (Outer London). <br>
                On constate que les temps de trajet sont plus élevés en périphérie que dans le centre, ce qui est principalement dû à des distances parcourues entre la caserne de départ et le lieu d'incident plus importantes dans les arrondissements de la périphérie de Londres (Outer London) par rapport à ceux du centre de Londres (Inner London).</p><br>
                """, unsafe_allow_html=True)

            st.image("images/Nuage de points entre le temps de trajet et la distance pour les mobilisations du 1er camion sur 2023 en fonction de la zone incident.png")

        
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
            margin-left: 20px; 
        }
        </style>
        <ul class="custom-ul">
        <li><strong>AttendanceTimeSeconds</strong> (Temps d’arrivée entre la caserne de départ et le lieu d’incident une fois la caserne sollicitée) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)</li>
        <li><strong>IncGeo_WardNameNew</strong> (Nom du quartier de Londres où se situe l’incident) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .custom-ul {line-height: 1.2;margin-left: 20px;}
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p"><br><strong>On constate également des <span style="color: orange;">corrélations modérées à fortes (coefficient de corrélation compris entre 0.25 et 0.7)</span> entre les paires de données suivantes :</strong></p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
            margin-left: 20px;
        }
        </style>
        <ul class="custom-ul">
        <li><strong>DelayCode_Description</strong> (Cause de retard éventuelle) / <strong>AttendanceTimeSeconds</strong> (Temps d’arrivée entre la caserne de départ et le lieu d’incident une fois la caserne sollicitée)</li>
        <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> (Mobilisation ou non de la caserne de liée à la zone de l’incident) / <strong>TravelTimeSeconds</strong> (temps de trajet entre la caserne de départ et le lieu d’incident)<br></li></ul>
        """, unsafe_allow_html=True)
   
    col1, col2 = st.columns([1, 15])
    with col1:
        st.markdown("")
    with col2:
        with st.expander("**Pour illustrer cette corrélation**"):
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                    margin-left: 20px;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Pour illustrer cette corrélation, ci-dessous une visualisation sous forme de nuage de points du temps de trajet et de la distance pour l'ensemble des mobilisations du premier camion sur l'année 2023, en distinguant le cas où la caserne de départ se situe dans la zone d'incident (Cas True) et le cas où la caserne de départ ne se situe pas dans la zone d’incident (Cas False). <br>
                On constate que les temps de trajet sont plus élevés lorsque le camion part d'une caserne en dehors de la zone d'incident, en raison d'une distance généralement plus élevée.</p><br>
                """, unsafe_allow_html=True)

            st.image("images/Nuage de points entre le temps de trajet et la distance pour les mobilisations du 1er camion sur 2023 en fonction de la caserne de départ.png")
    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
            margin-left: 20px;
        }
        </style>
        <ul class="custom-ul">        
        <li><strong>PropertyType</strong> (Type de propriété) / <strong>Inner_Outer</strong> (Situation dans le centre ou en périphérie de Londres)</li>
        <li><strong>PropertyCategory</strong> (Catégorie de propriété) / <strong>IncidentGroup</strong> (Catégorie d’incident)</li>
        <li><strong>PropertyCategory</strong> (Catégorie de propriété) / <strong>stopCodeDescription</strong> (Sous-catégorie d’incident)</li>
        <li><strong>PropertyCategory</strong> (Catégorie de propriété) / <strong>SpecialServiceType</strong> (Type de service spécial)</li>
        <li><strong>IncGeo_WardNameNew</strong> (Nom du quartier de Londres où se situe l’incident) / <strong>DeployedFromStation_Name</strong> (Nom caserne de départ)</li>
        </ul>
        """, unsafe_allow_html=True)


##############################################################
# Choix des caractéristiques pertinentes pour la modélisation
##############################################################
elif page == pages[4]:
    # st.title("Choix des caractéristiques pertinentes pour la modélisation")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Sélection des caractéristiques pertinentes pour la modélisation</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">L'analyse des corrélations entre variables entre variables identifiées, nous a permis d'identifier les <strong><span style="color: orange;">caractéristiques pertinentes</span></strong> à considérer pour <strong><span style="color: orange;">construire, entraîner et tester des modèles de Machine Learning</span></strong>, en vue de pouvoir <strong> prédire les temps d'arrivée</strong>  des pompiers sur le lieu d'incident :</p>
        """, unsafe_allow_html=True)

    with st.expander("**1 - Caractéristiques liées à des données du jeu de données initial**"):
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <ul class="custom-ul">
            <h2 style='text-align: left; color: black; font-size: 22px;'>Caractéristiques liées à des données du jeu de données initial</h2>
            <li><strong>IncidentGroup</strong>  (ex : False Alarm, Fire, Special service) : Nature de l’incident</li>
            <li><strong>DeployedFromStation_Name</strong> : indicateur de départ depuis une autre caserne que celle liée à l’incident. Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>
            <li><strong>IncGeo_BoroughName</strong> : Nom d'arrondissement / circonscription administrative de Londres (borough) du lieu d'incident</li>
            <li><strong>Easting_rounded</strong> : Ordonnée en m du lieu d'incident, arrondie à la cinquantaine dans le système de coordonnées en projection UTM</li>
            <li><strong>Northing_rounded</strong> : Ordonnée en m du lieu d'incident, arrondie à la cinquantaine dans le système de coordonnées en projection UTM</li>
            <li><strong>PropertyCategory</strong> (ex : Non Residential) : Catégorie de propriété concernée par l'incident</li>
            <li><strong>IncidentStationGround</strong>  : Caserne des pompiers liée au lieu de l'incident (pas forcément celle qui déploie les camions sur le lieu d'incident)</li>
            <li><strong>HourOfCall</strong> : Heure de l'appel au 999</li></ul>
            """, unsafe_allow_html=True)
        
    with st.expander("**2 - Caractéristiques créées à partir de données du jeu de données initial**"):
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>   
            <ul class="custom-ul">
            <h2 style='text-align: left; color: black; font-size: 22px;'>Caractéristiques créées à partir de données du jeu de données initial</h2>
            <li><strong>Distance_Incident_DeployedFromStation</strong> : Distance à vol d’oiseau en m calculée entre la caserne de départ et le lieu d’incident. Il s’agit de la distance orthodromique entre les 2 points, sur la base de la latitude et de la longitude à l'aide de la formule Haversine.</li>
            <li><strong>Distance_Incident_IncidentStationGround</strong> : Distance à vol d’oiseau en m entre la caserne de la zone d'incident et le lieu de l'incident.</li>
            <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> : Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>        
            <li><strong>Inner_Outer</strong> : Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
            <li><strong>DepartureOrder</strong>  : Ordre de départ du camion mobilisé sur un incident suite à l’appel au 999</li>
            <li><strong>WeekdayOfCall</strong> : Jour de semaine lié à la date de l'appel au 999 </li>
            <li><strong>MonthOfCall</strong> : N° de mois de l'année liée à la date de l'appel au 999</li>
            <li><strong>WeekOfCall</strong> : N° de semaine de l'année liée à la date de l'appel au 999</li>
            <li><strong>Taux_retard</strong>  : Taux de mobilisations ayant subi un retard associé à la caserne mobilisée sur l’incident suite à l’appel au 999</li></ul>
            """, unsafe_allow_html=True)
        
    with st.expander("**3 - Caractéristiques liées à des nouvelles données non présentes dans le jeu de données initial et ayant une influence sur la variable cible**"):
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <ul class="custom-ul">
            <h2 style='text-align: left; color: black; font-size: 22px;'>Caractéristiques liées à des nouvelles données non présentes dans le jeu de données initial et récupérées à partir de sources tierces</h2>
            <li><strong><span style="color: orange;">Coordonnées</span> des 102 casernes du Grand Londres</strong></li>
            <li><strong>Distance_Incident_DeployedFromStation</strong> : <strong><span style="color: orange;">Distance à vol d'oiseau</span></strong> (en m) entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident. <br>
            <li><strong>Données OpenStreetMap de représentation des <span style="color: orange;">réseaux routiers et des infrastructures urbaines</span> du Grand Londres</strong></li>
            <li><strong>Dist_trajet_Incident_DeployedFromStation</strong> : <strong><span style="color: orange;">Distance</span> (en m) de l'<span style="color: orange;">itinéraire routier le plus court</strong></span> entre la caserne de départ et le lieu de l'incident. <br>
            Ci-dessous un exemple de calcul de distance d’itinéraire routier entre la caserne de départ (Dagenham) et le lieu d’un incident survenu le 03/05/2023 dans le Newham (en bleu la distance à vol d’oiseau - 8655m dans l’exemple, en rouge la distance totale de l’itinéraire - 10068 m dans l’exemple)<br></li>
            """, unsafe_allow_html=True)
   

        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown("")
        with col2:
            st.image("images/Distance itinéraire entre la caserne de Dagenham et le lieu incident dans le Newham.png")
    
        
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <ul class="custom-ul">
            <li><strong>day_temperature,day_sunshine_duration_s,day_precipitation_mm, day_snow_mm, day_nb_precipitation_hours</strong>  : données météo quotidiennes (température moyenne, durée d’ensoleillement, cumul de précipitations en mm, cumul de chute de neige en mm, nombre d’heures de précipitations)</li>
            <li><strong>hour_temperature,hour_sunshine_duration_s, hour_precipitation_mm, hour_snow_mm</strong>  : données météo quotidiennes (température moyenne, durée d’ensoleillement, cumul de précipitations en mm, cumul de chute de neige en mm, nombre d’heures de précipitations)</li>
            </ul>
            """, unsafe_allow_html=True)


#######################################################################################
# Traitement des valeurs manquantes et des valeurs aberrantes/extrêmes résiduelles
#######################################################################################
elif page == pages[5]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Traitement des valeurs manquantes et des valeurs aberrantes/extrêmes résiduelles</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Dans le but de <strong>fiabiliser</strong> les données conservées, nous avons procédé à un <strong>traitement des valeurs manquantes et des valeurs aberrantes/extrêmes résiduelles</strong></p>
        <ul class="custom-ul">
        <li><strong>Traitement des <span style="color: orange;">valeurs manquantes</span> résiduelles</strong>, par <span style="color: orange;"><strong>suppression</span></strong> ou par <span style="color: orange;"><strong>remplacement</span></strong>.</li>
        <li><strong>Traitement des <span style="color: orange;">valeurs aberrantes et extrêmes</span></strong> dans certaines données, par <span style="color: orange;"><strong>suppression</span></strong> ou <span style="color: orange;"><strong>remplacement</span></strong>.</li>
        </ul>
        """, unsafe_allow_html=True)
        
    tab1, tab2 = st.tabs(["Gestion des valeurs manquantes", "Gestion des valeurs aberrantes/extrêmes"])
    
    ###########################################################################
    ## Gestion des valeurs manquantes
    ##################################
    with tab1:
        st.markdown("""
            <h2 style='text-align: left; color: black; font-size: 22px;'>Gestion des valeurs manquantes</h2>
    
            Ci-dessous est visualisée la <strong><span style="color: orange;">répartition des valeurs manquantes</span></strong> du DataFrame initial, en nous limitant aux <strong>colonnes comportant des valeurs manquantes</strong> :
            """, unsafe_allow_html=True)
        
        st.image("images/Heatmap valeurs manquantes.png")
    
        with st.expander("**Il existe plusieurs options permettant de gérer les valeurs manquantes**"):
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <ul class="custom-ul">
                <li>La <strong><span style="color: orange;">suppression des lignes</span></strong> contenant <strong>au moins une feature (colonne) avec une valeur manquante</strong>, le risque étant d'écarter un nombre important d'observations (lignes) en cas de feature présentant une proportion importante de valeurs manquantes, et par conséquent de produire un modèle de Machine Learning peu performant en cas d'apprentissage sur un jeu de données réduit.</li>
                <li>Le <strong><span style="color: orange;">remplacement (ou imputation) des valeurs manquantes</span></strong> par des valeurs artificielles (ex: la valeur moyenne ou médiane ou le mode), avec le risque d'altérer sensiblement la distribution et la composition du jeu de données en cas de valeur de remplacement mal choisie ou d'un volume important de valeurs manquantes à remplacer</li>
                <li>La <strong><span style="color: orange;">suppression des colonnes</span></strong> comportant une <strong>proportion importante de valeurs manquantes</strong> et ayant un <strong>intérêt limité</strong> pour la suite du projet.</li></ul>
                """, unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Les <strong>valeurs manquantes</strong> ont été traitées par :</p>
            <ul class="custom-ul">
            <li><strong><span style="color: orange;">suppression des colonnes</span></strong> comportant une <strong>proportion importante de valeurs manquantes et/ou</strong> ayant un <strong>intérêt limité pour la modélisation</strong></li>
            <li>ou par <strong><span style="color: orange;">remplacement (ou imputation)</span></strong> des valeurs manquantes <strong>par des valeurs bien choisies</strong>. </li></ul>
            """, unsafe_allow_html=True)

    ###########################################################################
    ## Gestion des valeurs aberrantes et extrêmes
    #############################################
    with tab2:
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <h2 style='text-align: left; color: black; font-size: 22px;'>Gestion des valeurs aberrantes et extrêmes</h2>
            <p class="custom-p">
            En analysant la <span style="color: orange;"><strong>vitesse des camions de pompiers</strong></span>, calculée à partir du <strong>temps de trajet enregistré</strong></span>
            et de la <strong>distance à vol d'oiseau entre la caserne de départ et le lieu d’incident</strong>, on a constaté des <span style="color: orange;"><strong>valeurs aberrantes</span></strong>, 
            avec des valeurs de vitesse <span style="color: orange;"><strong>dépassant les 100 km/h</strong></span> (<strong>record à 60 000 km/h</strong> pour la plus élevée).<br><br></p>
            <p class="custom-p">Afin de <strong>réduire l’effet de ces valeurs aberrantes</strong> nous avons :</p>
            <ul class="custom-ul">
            <li><strong><span style="color: orange;">Evalué la distance de l’itinéraire routier</span></strong> entre la caserne et le lieu d’incident, à partir des données des réseaux routiers.<br></li>
            <li><strong><span style="color: orange;">Supprimé les lignes du DataFrame comportant des valeurs de vitesse très aberrantes</span></strong> liées à des valeurs de <strong>temps de trajet erronnées</strong><br></li>
            <li><strong><span style="color: orange;">Ajusté les valeurs extrêmes basses à la valeur du 5e percentile (14 km/h) et les valeurs extrêmes hautes à la valeur du 95e percentile (55 km/h)</span></strong>.<br></li>
            <li><span style="color: orange;"><strong>Recalculé la valeur de temps de trajet</strong></span> sur la base de la valeur de distance de l'itinéraire et de la valeur de vitesse ajustée<br><br></li></ul>
            """, unsafe_allow_html=True)


##############################################################
# Modélisation
##############################################################
elif page == pages[6]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Modélisation</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Jeux d'entrainement/test", "Standardisation/Encodage", "Modèles de régression", "Modèles de classification"])
    
    ###########################################################################
    with tab1:
        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Pour entraîner les différents modèles de Machine Learning, nous nous sommes basés sur un jeu de données limité à <strong>60 000 mobilisations sélectionnées aléatoirement sur 2023</strong>, 
            pour lesquelles nous avions calculé l'itinéraire le plus court entre la caserne de départ et le lieu d'incident et la distance associée.</p>
            """, unsafe_allow_html=True)
        
        ######## Séparation du jeu de données liées aux caractéristiques sélectionnées en un jeu d’entraînement et un jeu de test ################
        st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Séparation du jeu de données liées aux caractéristiques sélectionnées en un jeu d’entraînement et un jeu de test</h2>", unsafe_allow_html=True)
        st.markdown("""  
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Nous avons découpé cet ensemble de données en :</p>
            <ul class="custom-ul">
            <li>Un <strong><span style="color: orange;">jeu de données d’entraînement</span></strong> contenant 80% des données, à la fois les valeurs des caractéristiques d'entrée et de la variable cible, utilisées
            pour entraîner les modèles de Machine Learning.</li>
            <li>Un <strong><span style="color: orange;">jeu de données de test</span></strong> contenant 20% des données, à la fois les valeurs des caractéristiques d'entrée et de la variable cible, utilisées 
            pour évaluer les performances des modèles entraînés, par comparaison entre les valeurs réelles et les valeurs prédites par les modèles.<br></li>
            </ul>
            """, unsafe_allow_html=True)

    ######################################################################################################################
    with tab2:
    ######## Séparation des différents types de caractéristiques (catégorielles, numériques, cycliques) ################
        # st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Séparation des différents types de caractéristiques (catégorielles, numériques, cycliques)</h2>", unsafe_allow_html=True)
        # st.markdown("""
        #     <style>
        #     .custom-ul {
        #         line-height: 1.2;
        #     }
        #     </style>
        #     <style>
        #     .custom-p {margin-bottom: -0.1em;}
        #     </style>
        #     <p class="custom-p">En fonction Les caractéristiques candidates retenues pour construire nos modèles de régression et de classification peuvent être classées en différents types principaux que nous nous sommes attachés à identifier :</p>
        #     <ul class="custom-ul">
        #     <li>Caractéristiques <strong><span style="color: orange;">numériques quantitatives</span></strong> représentant une mesure (continues ou discrètes).</li>
        #     <li>Caractéristiques <strong><span style="color: orange;">catégorielles qualitatives</span></strong> représentant des catégories ou des classes.</li>
        #     <li>Caractéristiques <strong><span style="color: orange;">cycliques</span></strong> qui se répètent de manière périodique, comme les jours de la semaine, les mois, les heures de la journée, les numéros de semaines liés à une saison.</li>
        #     </ul>
        #     """, unsafe_allow_html=True)
            
        # st.markdown("""
        #     Une fois les types identifiés, nous avons découpé les jeux de données d’entraînement et de test, contenant les données des différentes caractéristiques, en sous-ensembles liés à chaque type de donnée, afin de pouvoir leur appliquer un traitement différencié (<strong><span style="color: orange;">standardisation</span></strong>  des caractéristiques <strong>numériques et cycliques</strong>, <strong><span style="color: orange;">encodage</span></strong> des caractéristiques <strong>catégorielles</strong>).<br>
        #     L'objectif de cette démarche est de traiter chaque type de caractéristique de manière optimale pour améliorer la performance du modèle de machine learning, tout en conservant les informations importantes et en réduisant les biais potentiels.<br>
        #     """, unsafe_allow_html=True)

    ######## Transformation des données (standardisation, encodage) ################
        st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Transformation des données avant modélisation (standardisation, encodage)</h2>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Afin que les données d'entrée sélectionnées soient pleinement exploitables par les modèles de Machine Learning, nous avons :</p>
            <ul class="custom-ul">
            <li><strong><span style="color: orange;">Standardisé les caractéristiques numériques et cycliques </span></strong> (de nature périodique) pour les mettre sur la même échelle, afin que le modèle ne soit pas biaisé par l'échelle des variables.</li>
            <li><strong><span style="color: orange;">Encodé les variables catégorielles nominales</span></strong>, pour les convertir en variables binaires (0 ou 1), en utilisant le <strong>One-Hot Encoding</strong>.<br>
            Cela concerne par exemple les caractéristiques catégorielles comme le nom de la caserne de départ, l'existence de retards associés aux mobilisations de la caserne, ou la nature d'incident, etc</li>
            </ul>
            """, unsafe_allow_html=True)
        
    
    ###########################################################################
    with tab3:
    ######## Modélisation de type régression ################   
        st.markdown("<h3 style='text-align: left; color: blue; font-size: 20px;'>Modélisation de type régression</h3>", unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Dans un premier temps, nous avons utilisé des <strong><span style="color: orange;">modèles de régression</span></strong> afin de <strong>prédire la valeur du temps d’arrivée d’un camion de pompiers sur le lieu d’incident</strong>. <br>
            Pour ce type de modélisation, il s'agit d'une <strong><span style="color: orange;">variable cible de type numérique</span></strong>, en l'occurence la variable <strong>AttendanceTimeSeconds</strong> correspondant au <strong>Temps d'arrivée des pompiers sur le lieu d'incident</strong>, incluant le temps de mobilisation de l’équipage et le temps de trajet entre la caserne et le lieu de l’incident,
             dont la <strong>distribution</strong> sur le jeu de données est la suivante :
            </p>
            """, unsafe_allow_html=True)
    
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown("")
        with col2:
            st.image("images/Boxplot Distribution des temps d'arrivée du 1er camion sur 2023_annotations.png")

        with st.expander("**Nous avons entrainé, testé et évalué différents modèles de régression**"):
            st.markdown("""
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Dans le cadre de cette modélisation de type régression, nous avons entrainé et testé les <strong>modèles de régression</strong> suivants :</p>
                <ul class="custom-ul">
                <li><strong>Régression Linéaire</strong> : Ce modèle suppose une relation linéaire entre les caractéristiques et la cible, ce qui n'est pas toujours le cas dans les données réelles.  Il peut être influencé par les valeurs aberrantes.</li>
                <li><strong>Régression Polynomiale</strong> : Ce modèle est une extension de la régression linéaire tout en permettant de capturer des relations non linéaires entre les caractéristiques et la variable cible en ajoutant des termes polynomiaux.</li>
                <li><strong>Régression Ridge</strong> : Ce modèle permet une réduction de l'overfitting et est efficace lorsque les caractéristiques sont fortement corrélées entre elles.</li>
                <li><strong>Régression Lasso</strong></li>
                <li><strong>Forêts aléatoires et Arbres de décision</strong> : Ce sont deux modèles qui permettent de modéliser des relations non linéaires sans nécessiter de transformation des données. Ils sont peu sensibles à la mise à l'échelle des caractéristiques et gèrent bien les caractéristiques catégorielles.</li>
                <li><strong>XGBoost Regressor (eXtreme Gradient Boosting Regressor)</strong> : Ce modèle est réputé pour sa performance, sa vitesse et sa précision. XGBoost utilise une série d'optimisations en termes de calcul pour améliorer la vitesse et l'efficacité, comme le parallélisme et la gestion efficace de la mémoire. Comme les autres modèles de gradient boosting, XGBRegressor construit de nombreux arbres de décision de manière séquentielle, où chaque nouvel arbre corrige les erreurs des arbres précédents.</li>
                <li><strong>SGD Regressor (Stochastic Gradient Descent)</strong> : Ce modèle est un modèle de régression linéaire très efficace pour des ensembles de données de grande taille grâce à son approche incrémentale.</li>
                <li><strong>Huber Regressor</strong> : C'est un modèle est plus robuste aux valeurs aberrantes que la régression linéaire classique grâce à sa fonction de perte moins sensible aux erreurs importantes.</li>
                </ul>
                """, unsafe_allow_html=True)

        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Pour <strong>évaluer et comparer la performance</strong> de ces différents modèles de régression nous avons utilisé différentes <strong><span style="color: orange;">métriques</span></strong> : <strong>MAE, MSE, RMSE, R²</strong>.<br><br>
            <h4 style='text-align: left; color: darkblue; font-size: 16px;'>Résultats / Classement des modèles de régression</h4>
            Ci-dessous le classement (du plus performant au moins performant) des différents modèles de régression entrainés et testés, en fonction du <strong><span style="color: orange;">coefficient de détermination R²</span></strong> :</p>
            """, unsafe_allow_html=True)
    
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown("")
        with col2:
            st.image("images/Scores modeles de regression.png")
    
    
        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p"><strong><span style="color: orange;">>>></span></strong>  Le <strong>modèle de régression le plus performant</strong> (avec le meilleur R²) est le modèle <strong><span style="color: orange;">XGBRegressor</span></strong>, suivi des modèles DecisionTreeRegressor et RandomForestRegressor.<br>
            Pour le modèle le plus performant, <strong>XGBRegressor</strong>,</p>
            <ul class="custom-ul">
            <li>le <strong><span style="color: orange;">R²</span> (i.e. coefficient de détermination)</strong> est de <strong><span style="color: orange;">0.66</span></strong>,</li>
            <li>la <strong><span style="color: orange;">MAE</span> (i.e. écart moyen entre les valeurs prédites et réelles de temps d’arrivée)</strong> est de <strong><span style="color: orange;">57,5 secondes</span></strong> pour un <strong>temps d'arrivée moyen de 357 secondes</strong>, soit un <strong><span style="color: orange;">écart moyen d’environ 16%</span> par rapport au temps moyen</strong>, ce qui représente un <strong>écart significatif</strong>, surtout dans un contexte où chaque seconde peut être critique, comme dans les interventions d'urgence.</li>
            </ul>
            """, unsafe_allow_html=True)
    
        with st.expander("**Graphe des résidus (écarts entre valeur prédite et valeur réelle)**"):
            st.markdown("""
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <h4 style='text-align: left; color: darkblue; font-size: 16px;'>Graphe des résidus (écarts entre valeur prédite et valeur réelle)</h4>
                <p class="custom-p">Ci-dessous le <strong><span style="color: orange;">graphe des résidus</span></strong> liés au modèle <strong>XGBRegressor</strong>.<br>
                On constate que les <strong>écarts entre la valeur prédite et la valeur réelle peuvent être très importants</strong>, parfois de quelques centaines de secondes.</p>
                """, unsafe_allow_html=True)
        
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown("")
            with col2:
                st.image("images/Graphe des residus XGBoostRegressor.png")
    
    
        with st.expander("**Graphe des caractéristiques les plus importantes/influentes**"):
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <h4 style='text-align: left; color: darkblue; font-size: 16px;'>Importance des caractéristiques</h4>
                <p class="custom-p">Ci-dessous un graphe visualisant par ordre d'importance décroissante les <strong><span style="color: orange;">caractéristiques les plus influentes</span></strong> dans les prédictions du modèle <strong>XGBRegressor</strong>.</p>
                """, unsafe_allow_html=True)
        
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown("")
            with col2:
                st.image("images/Features Importance XGBoostRegressor.png")
        
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Sans surprise, on retrouve en tête les 3 caractéristiques suivantes :</p>
                <ul class="custom-ul">
                <li><strong><span style="color: orange;">Dist_trajet_Incident_DeployedFromStation</span></strong> : <strong>Distance en m de l'itinéraire le plus court</strong> entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident./li>      
                <li><strong><span style="color: orange;">Inner_Outer</span></strong> : <strong>Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres</strong>. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
                <li><strong><span style="color: orange;">DeployedFrom_egalA_IncidentGround_Station</span></strong> : Permet d’identifier <strong>si le camion déployé</strong> sur le lieu d’incident suite à l’appel au 999 <strong>part d'une caserne différente de celle liée au lieu d’incident</strong>.</li>  
                </ul>
                """, unsafe_allow_html=True)


    ###########################################################################
    with tab4:
    ######## Modélisation de type classification ################       
        st.markdown("<h3 style='text-align: left; color: blue; font-size: 20px;'><br>Modélisation de type classification</h3>", unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p">Malgré</p>
            <ul class="custom-ul">
            <li>l'enrichissement du jeu de données initial avec <strong> de nouvelles caractéristiques</strong> (ex : <strong>distance de trajet le plus court</strong>, <strong>données météo</strong>),</li> 
            <li>l'<strong>optimisation des hyperparamètres</strong> des modèles de régression,</li> 
            <li>l’utilisation de techniques d’<strong>ensemble learning</strong> comme le <strong>bagging</strong>,</li> 
            </ul>
            <span style="color: red;"><strong>Nous ne sommes pas parvenus à améliorer significativement les résultats des modèles de régression</strong></span>.<br><br>
            Nous avons alors complété notre modélisation par l'utilisation de <strong><span style="color: orange;">modèles de classification</span></strong>, 
            afin de <strong>prédire</strong> cette fois-ci une <strong><span style="color: orange;">classe binaire</span> indiquant si le temps d’arrivée sur un lieu d’incident sera inférieur ou supérieur à 6 min</strong>.<br>
            La <strong><span style="color: orange;">variable cible</span></strong> est alors une <strong><span style="color: orange;">classe binaire</span> indiquant l'atteinte (classe 1) ou non (classe 0) de l’objectif de temps d’arrivée < 6 min</strong>, 
             dont la <strong>distribution</strong> sur le jeu de données est la suivante :
            </p>
            """, unsafe_allow_html=True)
    
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown("")
        with col2:
            st.image("images/Distribution des classes.png")
         
        with st.expander("**Nous avons entrainé, testé et évalué différents modèles de classification**"):
            st.markdown("""
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Dans le cadre de cette modélisation de type classification, nous avons entrainé et testé les <strong><span style="color: orange;">modèles de classification</span></strong> suivants :</p>
                <ul class="custom-ul">
                <li><strong>XGBoostClassifier</strong></li>
                <li><strong>LogisticRegression</strong></li>
                <li><strong>DecisionTreeClassifier</strong></li>
                <li><strong>RandomForestClassifier</strong></li>
                <li><strong>SupportVectorMachine</strong></li>
                </ul>   
                """, unsafe_allow_html=True)

        st.markdown("""
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p"> Pour <strong>évaluer et comparer la performance</strong> de ces différents modèles de classification nous avons utilisé différentes <strong><span style="color: orange;">métriques</span></strong> : <strong>Exactitude (Accuracy), Rappel (Recall), Précision, F1-Score, AUC-ROC</strong>.<p>
            <h4 style='text-align: left; color: darkblue; font-size: 16px;'>Résultats / Classement des modèles de classification</h4>
            <p>Ci-dessous le classement (du plus performant au moins performant) des modèles de classification finaux entrainés et testés, en fonction de l'<strong><span style="color: orange;">exactitude (ou accuracy)</span></strong> :</p>
            """, unsafe_allow_html=True)
    
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown("")
        with col2:
            st.image("images/Scores modeles de classification.png")
    
    
        st.markdown("""
            <style>
            .custom-ul {
                line-height: 1.2;
            }
            </style>
            <style>
            .custom-p {margin-bottom: -0.1em;}
            </style>
            <p class="custom-p"><strong><span style="color: orange;">>>></span></strong> Le <strong>modèle de classification le plus performant</strong> est le modèle <strong><span style="color: orange;">XGBClassifier</span></strong>. Avec :<br></p>
            <ul class="custom-ul">
            <li><strong>Exactitude (Accuracy) : <span style="color: orange;">82.93%</span> </strong> - Cela signifie que le modèle <strong>prédit correctement</strong> la classe liée à l’objectif d’un temps d'arrivée inférieur à 6 min <strong>dans environ 83% des cas</strong>.</li>
            <li><strong>Rappel (Recall) : <span style="color: orange;">88.06%</span> </strong> - Une valeur élevée indique que le modèle est <strong>particulièrement bon pour prédire correctement les cas où les camions de pompiers arrivent rapidement (classe positive)</strong> et <strong>minimise le nombre de Faux Négatifs</strong> (Nb de positifs classés négatifs lors de la prédiction).</li>
            <li><strong>Précision : <span style="color: orange;">83.29%</span> </strong> - Cela montre que <strong>parmi les prédictions de classe positive</strong> du modèle, environ <strong>83% sont correctes</strong>.</li>
            <li><strong>F1 Score : <span style="color: orange;">85.61%</span> </strong> - Cette métrique combinant le Recall et la Precision indique une efficacité globale élevée du modèle, de 85.61%.</li>
            <li><strong>AUC-ROC : <span style="color: orange;">82.01%</span> </strong> - Cette métrique, qui mesure la capacité du modèle à distinguer entre les classes, est également assez élevée, à 82.01%.</li>
            </ul>
            """, unsafe_allow_html=True)
    
    
        with st.expander("**Graphe des caractéristiques les plus importantes/influentes**"):
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <h4 style='text-align: left; color: darkblue; font-size: 16px;'>Importance des caractéristiques</h4>
                <p class="custom-p">Ci-dessous un graphe visualisant par ordre d'importance décroissante les <strong><span style="color: orange;">caractéristiques les plus influentes</span></strong> dans les prédictions du modèle <strong>XGBClassifier</strong>.</p>
                """, unsafe_allow_html=True)
        
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown("")
            with col2:
                st.image("images/Features Importance XGBoostClassifier.png")
        
            st.markdown("""
                <style>
                .custom-ul {
                    line-height: 1.2;
                }
                </style>
                <style>
                .custom-p {margin-bottom: -0.1em;}
                </style>
                <p class="custom-p">Sans surprise, on retrouve en tête les 3 caractéristiques suivantes :</p>
                <ul class="custom-ul">
                <li><strong><span style="color: orange;">Dist_trajet_Incident_DeployedFromStation</span></strong> : <strong>Distance en m de l'itinéraire le plus court</strong> entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident./li>      
                <li><strong><span style="color: orange;">DeployedFrom_egalA_IncidentGround_Station</span></strong> : Permet d’identifier <strong>si le camion déployé</strong> sur le lieu d’incident suite à l’appel au 999 <strong>part d'une caserne différente de celle liée au lieu d’incident</strong>.</li>  
                <li><strong><span style="color: orange;">Inner_Outer</span></strong> : <strong>Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres</strong>. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
                </ul>
                """, unsafe_allow_html=True)


##############################################################
# Prédictions sur de nouvelles données
##############################################################
elif page == pages[7]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Prédictions sur de nouvelles données, mise en situation</h1>", unsafe_allow_html=True)
    #st.write("### Prédictions sur de nouvelles données, mise en situation")

    X_sim_all=pd.read_csv('./simulation/simulation.csv',sep=';')
 
    tab1, tab2, tab3, tab4, tab5, tab5bis = st.tabs(["Etape 1", "Etape 2", "Etape 3","Etape 4","Etape 5","Etape 5 bis"])

    with tab1:
        st.image("images/soho2.png")

    with tab2:        
        #st.audio("sounds/fire.mp3", format="audio/mpeg", autoplay=True)
        st.audio("sounds/fire.mp3", format="audio/mpeg")
        st.image("images/bm4.png")

    with tab3:
        #st.write("### Soho n’a pas les ressources, quelle station choisir ?")
        st.image("images/soho3.png")
        st.write("Soho n’a pas les ressources, quelle station choisir ?")
        st.write("L'objectif de la Brigade des Pompiers de Londres est d'arriver en moins de 6 minutes")
    
    with tab4:
        st.write("Identifier une caserne dont le camion mettra moins de 6 minutes") 
        st.image("images/stations2.png",width=900)

    with tab5: 
        # Préparation
        enc=pickle.load(open("./simulation/sim_enc.pkl", "rb"))
        sca=pickle.load(open("./simulation/sim_sca.pkl", "rb"))           

        circular_cols3 = ['HourOfCall', 'MonthOfCall', 'WeekOfCall', 'WeekdayOfCall']
        num_cols3 = ['Easting_rounded', 'Northing_rounded', 'Distance_Incident_IncidentStationGround', 'DepartureOrder', 'Dist_trajet_Incident_DeployedFromStation', 'day_temperature', 'day_sunshine_duration_s', 'day_precipitation_mm', 'day_snow_mm', 'day_nb_precipitation_hours', 'hour_temperature', 'hour_sunshine_duration_s', 'hour_precipitation_mm', 'hour_snow_mm', 'Taux_retard']
        cat_cols3 = ['IncidentGroup', 'PropertyCategory', 'IncGeo_BoroughName', 'IncidentStationGround', 'DeployedFromStation_Name', 'Inner_Outer', 'DeployedFrom_egalA_IncidentGround_Station']


        list_station=['caserne']
        list_station.extend(X_sim_all['DeployedFromStation_Name'])
        station = st.selectbox(
            "##### Choisir une caserne",
            list_station)
        if station!='caserne':
            X_sim=X_sim_all.loc[X_sim_all['DeployedFromStation_Name']==station]

            cat_sim = X_sim[cat_cols3]
            num_sim = X_sim[num_cols3]
            circular_sim = X_sim[circular_cols3]
            cat_sim_encoded = enc.transform(cat_sim)

            if 'HourOfCall' in circular_cols3:
                circular_sim.loc[:, 'sin_HourOfCall'] = circular_sim.loc[:, 'HourOfCall'].apply(lambda h : np.sin(2 * np.pi * h / 24))
                circular_sim.loc[:, 'cos_HourOfCall'] = circular_sim.loc[:, 'HourOfCall'].apply(lambda h : np.cos(2 * np.pi * h / 24))
                circular_sim = circular_sim.drop(['HourOfCall'],axis = 1)
                            
            if 'MonthOfCall' in circular_cols3:
                circular_sim.loc[:, 'sin_MonthOfCall'] = circular_sim.loc[:, 'MonthOfCall'].apply(lambda m : np.sin(2 * np.pi * m / 12))
                circular_sim.loc[:, 'cos_MonthOfCall'] = circular_sim.loc[:, 'MonthOfCall'].apply(lambda m : np.cos(2 * np.pi * m / 12))
                circular_sim = circular_sim.drop(['MonthOfCall'],axis = 1)
                
            if 'WeekOfCall' in circular_cols3:
                circular_sim.loc[:, 'sin_WeekOfCall'] = circular_sim.loc[:, 'WeekOfCall'].apply(lambda w : np.sin(2 * np.pi * w / 23))
                circular_sim.loc[:, 'cos_WeekOfCall'] = circular_sim.loc[:, 'WeekOfCall'].apply(lambda w : np.cos(2 * np.pi * w / 23))
                circular_sim = circular_sim.drop(['WeekOfCall'],axis = 1)
                
            if 'WeekdayOfCall' in circular_cols3:
                circular_sim.loc[:, 'sin_WeekdayOfCall'] = circular_sim.loc[:, 'WeekdayOfCall'].replace({'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 
                                                                                                        'Friday' : 5, 'Saturday' : 6, 'Sunday' : 7}).apply(lambda d : np.sin(2 * np.pi * d / 7))
                circular_sim.loc[:, 'cos_WeekdayOfCall'] = circular_sim.loc[:, 'WeekdayOfCall'].replace({'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 
                                                                                                        'Friday' : 5, 'Saturday' : 6, 'Sunday' : 7}).apply(lambda d : np.cos(2 * np.pi * d / 7))
                circular_sim = circular_sim.drop(['WeekdayOfCall'],axis = 1)

            num_sim_scaled=sca.transform(num_sim)


            sca.get_feature_names_out(num_cols3)
            num_sim_scaled=pd.DataFrame(num_sim_scaled, columns = sca.get_feature_names_out(num_cols3))
            cat_sim_encoded=pd.DataFrame(cat_sim_encoded, columns = enc.get_feature_names_out(cat_cols3))
            circular_sim=circular_sim.reset_index().drop('index',axis=1)

            X_sim_encoded = pd.concat([pd.DataFrame(num_sim_scaled), pd.DataFrame(cat_sim_encoded), pd.DataFrame(circular_sim)], axis = 1)

            st.write("")
            st.write("")
            st.write("##### Modèle de Classification")
            cla=pickle.load(open("./simulation/sim_class.pkl", "rb"))
            res_cla=cla.predict(X_sim_encoded)
            result='Résultat de la prédiction : **objectif atteint**, le camion mettra moins de 6 minutes' if res_cla[0]==1 else 'Résultat de la prédiction : **objectif non atteint**, le camion mettra plus de 6 minutes'
            st.write(result)         

            st.write("")
            st.write("##### Modèle de Régression")
            reg=pickle.load(open("./simulation/sim_reg.pkl", "rb"))
            res_reg=reg.predict(X_sim_encoded)

            from datetime import timedelta        
            st.write("Estimation du temps pour se rendre sur le lieu de l'incident depuis " + station)
            res_sec=int(res_reg[0])
            td=timedelta(seconds=res_sec)
            nb_min=td.seconds//60
            nb_sec=td.seconds%60
            st.write(str(res_sec) + " secondes soit " + str(nb_min) + " minutes et " + str(nb_sec) + " secondes")           

    with tab5bis:
        
        X_sim=X_sim_all

        cat_sim = X_sim[cat_cols3]
        num_sim = X_sim[num_cols3]
        circular_sim = X_sim[circular_cols3]
        cat_sim_encoded = enc.transform(cat_sim)

        if 'HourOfCall' in circular_cols3:
            circular_sim.loc[:, 'sin_HourOfCall'] = circular_sim.loc[:, 'HourOfCall'].apply(lambda h : np.sin(2 * np.pi * h / 24))
            circular_sim.loc[:, 'cos_HourOfCall'] = circular_sim.loc[:, 'HourOfCall'].apply(lambda h : np.cos(2 * np.pi * h / 24))
            circular_sim = circular_sim.drop(['HourOfCall'],axis = 1)
                        
        if 'MonthOfCall' in circular_cols3:
            circular_sim.loc[:, 'sin_MonthOfCall'] = circular_sim.loc[:, 'MonthOfCall'].apply(lambda m : np.sin(2 * np.pi * m / 12))
            circular_sim.loc[:, 'cos_MonthOfCall'] = circular_sim.loc[:, 'MonthOfCall'].apply(lambda m : np.cos(2 * np.pi * m / 12))
            circular_sim = circular_sim.drop(['MonthOfCall'],axis = 1)
            
        if 'WeekOfCall' in circular_cols3:
            circular_sim.loc[:, 'sin_WeekOfCall'] = circular_sim.loc[:, 'WeekOfCall'].apply(lambda w : np.sin(2 * np.pi * w / 23))
            circular_sim.loc[:, 'cos_WeekOfCall'] = circular_sim.loc[:, 'WeekOfCall'].apply(lambda w : np.cos(2 * np.pi * w / 23))
            circular_sim = circular_sim.drop(['WeekOfCall'],axis = 1)
            
        if 'WeekdayOfCall' in circular_cols3:
            circular_sim.loc[:, 'sin_WeekdayOfCall'] = circular_sim.loc[:, 'WeekdayOfCall'].replace({'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 
                                                                                                    'Friday' : 5, 'Saturday' : 6, 'Sunday' : 7}).apply(lambda d : np.sin(2 * np.pi * d / 7))
            circular_sim.loc[:, 'cos_WeekdayOfCall'] = circular_sim.loc[:, 'WeekdayOfCall'].replace({'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 
                                                                                                    'Friday' : 5, 'Saturday' : 6, 'Sunday' : 7}).apply(lambda d : np.cos(2 * np.pi * d / 7))
            circular_sim = circular_sim.drop(['WeekdayOfCall'],axis = 1)

        num_sim_scaled=sca.transform(num_sim)


        sca.get_feature_names_out(num_cols3)
        num_sim_scaled=pd.DataFrame(num_sim_scaled, columns = sca.get_feature_names_out(num_cols3))
        cat_sim_encoded=pd.DataFrame(cat_sim_encoded, columns = enc.get_feature_names_out(cat_cols3))
        circular_sim=circular_sim.reset_index().drop('index',axis=1)

        X_sim_encoded = pd.concat([pd.DataFrame(num_sim_scaled), pd.DataFrame(cat_sim_encoded), pd.DataFrame(circular_sim)], axis = 1)

        # régression
        reg=pickle.load(open("./simulation/sim_reg.pkl", "rb"))
        res_reg=reg.predict(X_sim_encoded)

        # classification        
        cla=pickle.load(open("./simulation/sim_class.pkl", "rb"))
        res_cla=cla.predict(X_sim_encoded)

        st.write("##### Identification de la caserne à mobiliser")
        df_res_all=pd.DataFrame({
            'Caserne':X_sim['DeployedFromStation_Name'],
            'Classification':res_cla,
            'Régression':res_reg
             })
        st.dataframe(df_res_all.style.apply(color_row, axis=1),hide_index=True)


##############################################################
# Conclusions métier
##############################################################
elif page == pages[8]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Conclusions métier</h1>", unsafe_allow_html=True)
    #st.write("### Conclusions métier")
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Fausses Alarmes</h2>", unsafe_allow_html=True)
    #st.write("#### Analyse des False Alarms :")
    st.markdown("""
                - Les Fausses Alarmes représentent près de la moitié des incidents <strong><span style="color:orange;">dont 80% sont des Fausses Alarmes Automatiques (AFA)</span></strong>
                """, unsafe_allow_html=True)
    st.markdown("""
                - Les conséquences : 
                    - Sollicitation des pompiers sur des lieux où il n’y a pas d’incidents
                    - Perturbation sur le lieu de l'incident : évacuation ...
                    - En 2023, les AFA représentent un coût de presque 25 millions de £ (sur près de 56 millions de £ en tout)
                """)
    st.markdown("""
                - Exemples de propositions d'amélioration métier :
                    - Comprendre la cause de AFA pour les limiter : 
                        - Mieux former les installateurs d'appareil de détection de fumée
                        - Contrôler les appareils plus régulièrement
                    - Envoyer un drône pour confirmer l'incident
                """)
    
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Qualité des données saisies</h2>", unsafe_allow_html=True)
    #st.write("#### Qualité des données saisies :")
    st.markdown("""      
                Certaines valeurs des temps d'arrivée sont <strong><span style="color:orange;">aberrantes</span></strong> : dans plusieurs cas la vitesse correspondante dépasse les 100 km/h, avec un record à 60 000 km/h.                                        
                A contrario d'autres valeurs <strong><span style="color:orange;">extrêmes</span></strong> sont très faibles : plusieurs cas en dessous de 4 km/h (vitesse d'un marcheur).                                        
                Il faudrait en comprendre la cause pour les limiter : erreur de saisie, problème de calcul ...                                                                  
                """, unsafe_allow_html=True)
 

##############################################################
# Perspectives d'amélioration
##############################################################
elif page == pages[9]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Perspectives d'amélioration</h1>", unsafe_allow_html=True)    
    #st.write("### Perspectives d'amélioration")
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Automatiser les traitements</h2>", unsafe_allow_html=True)
    st.markdown("""
                - Automatiser la collecte des données sources depuis le site de la LFB (web scrapping)
                - Créer un pipeline enchainant les étapes de préparation des données, d'entrainement du modèle et de prédiction
                """)    
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Enrichir le jeu de données</h2>", unsafe_allow_html=True)
    st.markdown("""
                - Utiliser une méthode de calcul d'itinéraire s'affranchissant des sens interdits
                - Intégrer les ralentissements, routes fermée, travaux en cours et tout obstacle impactant le temps de trajet (ces données sont présentes dans le motif des retards mais pas au moment de la mobilisation)
                """)
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Améliorer la Feature Engineering et la Modélisation</h2>", unsafe_allow_html=True)
    st.markdown("""
                - Essayer d'autres transformations de features que celles déjà tentées (transformations polynomiales, logarithmiques)
                - Essayer d'autres modèles de Deep Learning 
                """)

    
