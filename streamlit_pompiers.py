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

st.set_page_config(page_title="Projet DA Pompiers", page_icon=":fire:", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Sommaire")
pages=["Présentation du projet, du contexte et des enjeux","Exploration des données", "Analyse et visualisation des données", "Analyse & Visualisation des corrélations entre variables", "Choix des caractéristiques pertinentes pour la modélisation", "Nettoyage et prétraitement des données","Modélisation / Analyse des résultats", "Prédictions sur de nouvelles données", "Conclusions métier", "Perspectives d'amélioration"]
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


##############################################################
# Analyse & Visualisation des corrélations entre variables
##############################################################
elif page == pages[3]:
    # st.title("Analyse & Visualisation des corrélations entre variables")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Analyse & Visualisation des corrélations entre variables</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Heatmap de Corrélation entre variables</h2>", unsafe_allow_html=True)
    # st.header("Heatmap de Corrélation entre variables") 
    # st.write("Pour visualiser l’existence de relations entre différentes paires de variables catégorielles et numériques et mesurer la force de cette corrélation, nous avons construit une **heatmap de corrélation personnalisée**, construite à partir d'une matrice de corrélation basée sur des mesures de corrélation appropriées pour chaque type de variable :")
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Pour visualiser l’existence de relations entre différentes paires de variables catégorielles et numériques et mesurer la force de cette corrélation, nous avons construit une **heatmap de corrélation personnalisée**, construite à partir d'une matrice de corrélation basée sur des mesures de corrélation appropriées pour chaque type de variable :</p>
    """, unsafe_allow_html=True)
    
    detail = st.checkbox('Afficher les détails' ) 
    if detail:
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
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">On constate des <strong><span style="color: orange;">corrélations fortes (coefficient de corrélation > 0.7)</span></strong> entre les paires de données suivantes :</p>
        <ul class="custom-ul">
        <li><strong>TravelTimeSeconds</strong> (temps de trajet entre la caserne de départ et le lieu d’incident) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)<br>
        Pour illustrer cette corrélation, ci-dessous une visualisation sous forme de nuage de points du temps de trajet et de la distance pour l'ensemble des mobilisations du premier camion de pompiers jusqu'au lieu d'incident sur l'année 2023, en distinguant le cas où la caserne de départ se situe dans le centre de Londres (Inner London) ou dans la périphérie (Outer London). <br>
        On constate que les temps de trajet sont plus élevés en périphérie que dans le centre, ce qui est principalement dû à des distances parcourues entre la caserne de départ et le lieu d'incident plus importantes dans les arrondissements de la périphérie de Londres (Outer London) par rapport à ceux du centre de Londres (Inner London).<br></li></ul>
        """, unsafe_allow_html=True)
   

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("")
    with col2:
        st.image("images/Nuage de points entre le temps de trajet et la distance pour les mobilisations du 1er camion sur 2023 en fonction de la zone incident.png")

    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <ul class="custom-ul">
        <li><strong>AttendanceTimeSeconds</strong> (Temps d’arrivée entre la caserne de départ et le lieu d’incident une fois la caserne sollicitée) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)</li>
        <li><strong>IncGeo_WardNameNew</strong> (Nom du quartier de Londres où se situe l’incident) / <strong>Distance_Incident_DeployedFromStation</strong> (Distance entre caserne de départ et lieu d’incident)</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .custom-ul {line-height: 1.2;}
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">On constate également des <strong><span style="color: orange;">corrélations modérées (coefficient de corrélation compris entre 0.25 et 0.7)</span></strong> entre les paires de données suivantes :</p>
        <ul class="custom-ul">
        <li><strong>DelayCode_Description</strong> (Cause de retard éventuelle) / <strong>AttendanceTimeSeconds</strong> (Temps d’arrivée entre la caserne de départ et le lieu d’incident une fois la caserne sollicitée)</li>
        <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> (Mobilisation ou non de la caserne de liée à la zone de l’incident) / <strong>TravelTimeSeconds</strong> (temps de trajet entre la caserne de départ et le lieu d’incident)<br>
        Pour illustrer cette corrélation, ci-dessous une visualisation sous forme de nuage de points du temps de trajet et de la distance pour l'ensemble des mobilisations du premier camion sur l'année 2023, en distinguant le cas où la caserne de départ se situe dans la zone d'incident (Cas True) et le cas où la caserne de départ ne se situe pas dans la zone d’incident (Cas False). <br>
        On constate que les temps de trajet sont plus élevés lorsque le camion part d'une caserne en dehors de la zone d'incident, en raison d'une distance généralement plus élevée.<br></li></ul>
        """, unsafe_allow_html=True)
   

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("")
    with col2:
        st.image("images/Nuage de points entre le temps de trajet et la distance pour les mobilisations du 1er camion sur 2023 en fonction de la caserne de départ.png")

    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
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
    detail = st.checkbox('Détails' ) 
    # st.title("Choix des caractéristiques pertinentes pour la modélisation")
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Sélection des caractéristiques pertinentes pour la modélisation</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">sur la base des analyses de données, des visualisation et des tests statistiques réalisées dans la phase précédente, nous avons décider de sélectionner les <strong><span style="color: orange;"> caractéristiques< /span></strong> suivantes pour construire, entraîner et tester nos modèles :</p>

        <ul class="custom-ul">
        <h2 style='text-align: left; color: black; font-size: 22px;'>Ajout de caractéristiques utiles liées à des données existantes </h2>
        <li><strong>IncidentGroup</strong>  (ex : False Alarm, Fire, Special service) : Nature de l’incident</li>
        <li><strong>DeployedFromStation_Name</strong> : indicateur de départ depuis une autre caserne que celle liée à l’incident. Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>
        <li><strong>IncGeo_BoroughName</strong> : Nom d'arrondissement / circonscription administrative de Londres (borough) du lieu d'incident</li>
        <li><strong>Easting_rounded</strong> : Ordonnée en m du lieu d'incident, arrondie à la cinquantaine dans le système de coordonnées en projection UTM</li>
        <li><strong>Northing_rounded</strong> : Ordonnée en m du lieu d'incident, arrondie à la cinquantaine dans le système de coordonnées en projection UTM</li>
        <li><strong>PropertyCategory</strong> (ex : Non Residential) : Catégorie de propriété concernée par l'incident</li>
        <li><strong>IncidentStationGround</strong>  : Caserne des pompiers liée au lieu de l'incident (pas forcément celle qui déploie les camions sur le lieu d'incident)</li>
        <li><strong>HourOfCall</strong> : Heure de l'appel au 999</li>
        
        <h2 style='text-align: left; color: black; font-size: 22px;'>Ajout de nouvelles caractéristiques utiles créées à partir des données existantes </h2>
        <li><strong>Distance_Incident_DeployedFromStation</strong> : Distance à vol d’oiseau en m calculée entre la caserne de départ et le lieu d’incident. Il s’agit de la distance orthodromique entre les 2 points, sur la base de la latitude et de la longitude à l'aide de la formule Haversine.</li>
        <li><strong>Distance_Incident_IncidentStationGround</strong> : Distance à vol d’oiseau en m entre la caserne de la zone d'incident et le lieu de l'incident.</li>
        <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> : Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>        
        <li><strong>Inner_Outer</strong> : Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
        <li><strong>DepartureOrder</strong>  : Ordre de départ du camion mobilisé sur un incident suite à l’appel au 999</li>
        <li><strong>WeekdayOfCall</strong> : Jour de semaine lié à la date de l'appel au 999 </li>
        <li><strong>MonthOfCall</strong> : N° de mois de l'année liée à la date de l'appel au 999</li>
        <li><strong>WeekOfCall</strong> : N° de semaine de l'année liée à la date de l'appel au 999</li>
        <li><strong>Taux_retard</strong>  : Taux de mobilisations ayant subi un retard associé à la caserne mobilisée sur l’incident suite à l’appel au 999</li>
        
        <h2 style='text-align: left; color: black; font-size: 22px;'>Ajout de nouvelles données non existantes ayant une influence sur la variable cible et sur les performances des modèles de Machine Learning</h2>
        <li><strong>Dist_trajet_Incident_DeployedFromStation</strong> : Distance en m du trajet entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident. Il s’agit de la distance la plus courte de l’itinéraire calculé entre les 2 points en s’appuyant sur les données OpenStreetMap (OSM) de représentation des réseaux routiers et des infrastructures urbaines du monde entier, notamment du Grand Londres, en utilisant les packages python OSMnx, Networkx.<br>La distance de cet itinéraire est calculée en additionnant les longueurs des segments entre les nœuds consécutifs.<br>Ci-dessous un exemple de calcul de distance d’itinéraire entre la caserne de départ (Dagenham) et le lieu d’un incident survenu le 03/05/2023 dans le Newham, en se basant sur le réseau routier OpenStreetMap du Grand Londres (en bleu la distance à vol d’oiseau - 8655m dans l’exemple, en rouge la distance totale de l’itinéraire - 10068 m dans l’exemple)<br></li>
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


##############################################################
# Nettoyage & Prétraitement des données
##############################################################
elif page == pages[5]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Nettoyage & Prétraitement des données</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Dans le but de conserver un maximum de données fiables et cohérentes, nous avons procédé à un <strong>nettoyage</strong> et à un <strong>prétraitement des données</strong>, en particulier en</p>
        <ul class="custom-ul">
        <li>Traitant les <strong><span style="color: orange;">valeurs manquantes</span></strong> résiduelles par suppression ou remplacement.</li>
        <li>Traitant les <strong><span style="color: orange;">erreurs ou valeurs aberrantes/extrêmes</span></strong> dans les données, par suppression ou remplacement des valeurs.</li>
        </ul>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <h2 style='text-align: left; color: black; font-size: 22px;'>Gestion des valeurs manquantes</h2>

        L'utilisation de la méthode heatmap de la bibliothèque seaborn permet de visualiser la répartition des valeurs manquantes du DataFrame, en nous limitant ci-dessous aux colonnes comportant des valeurs manquantes :
        """, unsafe_allow_html=True)
    
    st.image("images/Heatmap valeurs manquantes.png")
    
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">La majorité des <strong>valeurs manquantes</strong> ont été traitées par <strong>suppression des colonnes</strong> comportant une proportion importante de valeurs manquantes et/ou ayant un intérêt limité pour la modélisation ou par <strong>remplacement (ou imputation)</strong> des valeurs manquantes par des valeurs bien choisies. </p>
        <ul class="custom-ul">
        <li>La <strong><span style="color: orange;">suppression des lignes</span></strong> contenant <strong>au moins une feature (colonne) avec une valeur manquante</strong>, le risque étant d'écarter un nombre important d'observations (lignes) en cas de feature présentant une proportion importante de valeurs manquantes, et par conséquent de produire un modèle de Machine Learning peu performant en cas d'apprentissage sur un jeu de données réduit.</li>
        <li>Le <strong><span style="color: orange;">remplacement (ou imputation) des valeurs manquantes</span></strong> par des valeurs artificielles (ex: la valeur moyenne ou médiane ou le mode), avec le risque d'altérer sensiblement la distribution et la composition du jeu de données en cas de valeur de remplacement mal choisie ou d'un volume important de valeurs manquantes à remplacer</li>
        <li>La <strong><span style="color: orange;">suppression des colonnes</span></strong> comportant une <strong>proportion importante de valeurs manquantes</strong> et ayant un <strong>intérêt limité</strong> pour la suite du projet.</li>
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
        <h2 style='text-align: left; color: black; font-size: 22px;'>Gestion des valeurs aberrantes et extrêmes</h2>
        <p class="custom-p">La donnée de distance à vol d’oiseau calculée entre la caserne de départ et le lieu d’incident et la donnée de temps de trajet nous avaient permis de calculer une donnée Vitesse_Incident_DeployedFromStation correspondant à une estimation de la vitesse du camion déployé sur le lieu de l'incident.<br> 
        Nous avons alors constaté que pour une partie des mobilisations de la brigade des pompiers de Londres la vitesse du camion déployé sur le lieu d'incident dépassait les 100 km/h (avec un record à 60 000 km/h pour la vitesse la plus élevée enregistrée), notamment en raison d'un délai de trajet enregistré anormalement faible au regard de la distance séparant la caserne de départ du lieu d'incident.
        Nous avons tout d'abord <strong><span style="color: orange;">supprimé les lignes du DataFrame comportant ces valeurs de vitesse aberrantes</span></strong> , c'est-à-dire au-delà de 100 km/h.<br>
        Puis le calcul de la <strong><span style="color: orange;">distance de l’itinéraire estimé le plus court</span></strong>  entre la caserne et le lieu d’incident a permis d’affiner l’estimation de la vitesse.
        Afin de réduire l’effet des valeurs aberrantes et rendre le jeu de données plus robuste face aux anomalies concernant les valeurs de certains temps de trajet enregistrés et la valeur de vitesse en résultant, nous avons utilisé la <strong><span style="color: orange;">technique de winsorisation pour winsoriser (i.e. ajuster) au 5e et au 95e percentile</span></strong>  les valeurs de vitesse situées en dessous du 5e percentile (14 km/h) et au-dessus du 95e percentile (55 km/h).<br>
        Puis nous avons recalculé une valeur de temps de trajet ajusté à partir de la valeur de vitesse ajustée et de la valeur de distance de l’itinéraire.<br>
        Ci-dessous un graphe de type boxplot montrant la distribution des valeurs de vitesse avant/après winsorisation</p>
        """, unsafe_allow_html=True)

    st.image("images/Winsorisation des valeurs extremes de vitesses de trajet.png")


##############################################################
# Modélisation
##############################################################
elif page == pages[6]:
    st.markdown("<h1 style='text-align: left; color: orange; font-size: 26px;'>Modélisation</h1>", unsafe_allow_html=True)

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
        <p class="custom-p">Nous avons découpé notre ensemble de données en :</p>
        <ul class="custom-ul">
        <li>Un <strong><span style="color: orange;">jeu de données d’entraînement</span></strong> contenant des données exemples pour les caractéristiques et pour la variable cible utilisées pour entraîner/ajuster les modèles à l’aide d’un algorithme d’apprentissage supervisé.</li>
        <li>Un <strong><span style="color: orange;">jeu de données de test</span></strong> contenant des données exemples pour les caractéristiques et pour la variable cible utilisées pour fournir une évaluation des performances du modèle précédemment entraîné à partir des données d’entraînement/apprentissage.<br>
        Les valeurs des caractéristiques du jeu de test sont utilisées pour effectuer des prédictions sur la valeur de la variable cible et les comparer aux véritables valeurs de la variable cible du jeu de test, ce qui permet d’évaluer la précision du modèle.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Séparation des différents types de caractéristiques (catégorielles, numériques, cycliques)</h2>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Les caractéristiques candidates retenues pour construire nos modèles de régression et de classification peuvent être classées en différents types principaux que nous nous sommes attachés à identifier :</p>
        <ul class="custom-ul">
        <li>Caractéristiques <strong><span style="color: orange;">numériques quantitatives</span></strong> représentant une mesure (continues ou discrètes).</li>
        <li>Caractéristiques <strong><span style="color: orange;">catégorielles qualitatives</span></strong> représentant des catégories ou des classes.</li>
        <li>Caractéristiques <strong><span style="color: orange;">cycliques</span></strong> qui se répètent de manière périodique, comme les jours de la semaine, les mois, les heures de la journée, les numéros de semaines liés à une saison.</li>
        </ul>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        Une fois les types identifiés, nous avons découpé les jeux de données d’entraînement et de test, contenant les données des différentes caractéristiques, en sous-ensembles liés à chaque type de donnée, afin de pouvoir leur appliquer un traitement différencié (<strong><span style="color: orange;">standardisation</span></strong>  des caractéristiques <strong>numériques et cycliques</strong>, <strong><span style="color: orange;">encodage</span></strong> des caractéristiques <strong>catégorielles</strong>).<br>
        L'objectif de cette démarche est de traiter chaque type de caractéristique de manière optimale pour améliorer la performance du modèle de machine learning, tout en conservant les informations importantes et en réduisant les biais potentiels.<br>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Transformation des données (standardisation, encodage)</h2>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Les transformations suivantes ont été effectuées sur les caractéristiques des jeux de données destinées à entraîner et tester les modèles de Machine Learning :</p>
        <ul class="custom-ul">
        <li><strong><span style="color: orange;">Standardiser les caractéristiques numériques et cycliques </span></strong> (de nature périodique) pour les mettre sur la même échelle, afin que le modèle ne soit pas biaisé par l'échelle des variables.</li>
        <li><strong><span style="color: orange;">Encoder les variables catégorielles </span></strong> en utilisant le <strong>One-Hot Encoding</strong> (conversion en caractéristiques binaires) pour qu’elles soient exploitables par les modèles de Machine Learning.<br>
        Cela concerne les caractéristiques catégorielles comme le nom de la caserne de départ, l'existence de retards associés aux mobilisations de la caserne, la nature d'incident, etc</li>
        </ul>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        Une fois ces traitements réalisés nous avons réassemblé les caractéristiques transformées en un seul DataFrame utilisé pour entrainer, optimiser et tester les modèles de machine learning.<br>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<h2 style='text-align: left; color: black; font-size: 22px;'>Sélection du type de modélisation (classification ou régression) et des modèles associés</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Pour la modélisation nous avons utilisé un jeu de données contenant les caractéristiques liées à <strong>60 000 mobilisations sélectionnées aléatoirement sur 2023</strong>, pour lesquelles nous avons calculé la distance de l'itinéraire le plus court entre la caserne de départ et le lieu d'incident.</p>
        """, unsafe_allow_html=True)

    
    st.markdown("<h3 style='text-align: left; color: blue; font-size: 20px;'>Modélisation de type régression</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Nous avons dans un premier temps choisi de travailler sur un problème de <strong>régression</strong> pour <strong><span style="color: orange;">prédire le temps d’arrivée d’un camion de pompiers sur le lieu d’incident</span></strong> à partir du moment où la caserne a été sollicitée pour intervenir. <br>
        Pour ce problème de régression, la variable cible est la variable AttendanceTimeSeconds, incluant le temps de mobilisation de l’équipage et le temps de trajet entre la caserne mobilisée et le lieu de l’incident. La distribution des valeurs de cette variable cible sur le jeu de données est la suivante :</p>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown("")
    with col2:
        st.image("images/Boxplot Distribution des temps d'arrivée du 1er camion sur 2023_annotations.png")
     
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Pour résoudre ce problème de régression, nous avons entrainé et testé les modèles de régression suivants :</p>
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
        <p class="custom-p"> Pour évaluer et comparer la performance de ces différents modèles de régression nous avons calculé différentes métriques : MAE, MSE, RMSE, R².<br>
        Ci-dessous le classement (du plus performant au moins performant) des différents modèles de régression entrainés et testés :</p>
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
        <p class="custom-p"><strong>>>></strong> Le modèle de régression le plus performant est le modèle <strong>XGBRegressor</strong>, suivi des modèles DecisionTreeRegressor et RandomForestRegressor.<br>
        Pour le modèle le plus performant, XGBRegressor, la <strong>MAE (écart moyen entre le temps d’arrivée prédit et le temps d’arrivée réel)</strong> est de <strong>57,5 secondes</strong> pour un <strong>temps d'arrivée moyen de 357 secondes</strong>, soit un <strong>écart moyen d’environ 16%</strong> par rapport au temps moyen, ce qui représente un écart significatif, surtout dans un contexte où chaque seconde peut être critique, comme dans les interventions d'urgence.</p>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <br>
        <p class="custom-p">Ci-dessous le <strong>graphe des résidus</strong> liés au modèle XGBRegressor.<br>
        On constate que les écarts entre la valeur prédite et la valeur réelle peut être très importante, parfois de quelques centaines de secondes.</p>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown("")
    with col2:
        st.image("images/Graphe des residus XGBoostRegressor.png")


    st.markdown("""
        <style>
        .custom-ul {
            line-height: 1.2;
        }
        </style>
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Ci-dessous un graphe visualisant par ordre d'importance décroissante les <strong>caractéristiques les plus influentes</strong> dans les prédictions du modèle XGBRegressor.</p>
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
        <li><strong>Dist_trajet_Incident_DeployedFromStation</strong> : Distance en m de l'itinéraire le plus court entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident./li>      
        <li><strong>Inner_Outer</strong> : Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
        <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> : Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>  
        </ul>
        """, unsafe_allow_html=True)


    
    st.markdown("<h3 style='text-align: left; color: blue; font-size: 20px;'>Modélisation de type classification</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Malgré l'<strong>ajout de nouvelles caractéristiques</strong> par rapport au jeu de données initial de la LFB, telles que la distance de trajet et les conditions météo, malgré l'<strong>optimisation des hyperparamètres</strong> des modèles, malgré l’utilisation de techniques d’<strong>ensemble learning</strong> comme le <strong>bagging</strong>, nous ne sommes pas parvenus à améliorer significativement les performances des modèles de régression.
        Au regard du relativement faible niveau de performance (R2, résidus) observé sur les modèles de régression testés, nous avons décidés de compléter notre modélisation par la mise en œuvre de modèles de classification permettant de prédire par exemple si le temps d’arrivée sur un lieu d’incident sera inférieur ou supérieur à 6 min.<br>
        Pour ce problème de classification, la variable cible est l'atteinte ou non de l’objectif de temps d’arrivée < 6 min. La distribution des valeurs de cette variable cible sur le jeu de données est la suivante :</p>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown("")
    with col2:
        st.image("images/Distribution des classes.png")
     
    st.markdown("""
        <style>
        .custom-p {margin-bottom: -0.1em;}
        </style>
        <p class="custom-p">Pour résoudre ce problème de régression, nous avons entrainé et testé les modèles de régression suivants :</p>
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
        <p class="custom-p"> Pour évaluer et comparer la performance de ces différents modèles de régression nous avons calculé différentes métriques : Exactitude (Accuracy), Rappel (Recall), Précision, F1-Score, AUC-ROC.<br>
        Ci-dessous le classement (du plus performant au moins performant) des modèles de classification finaux entrainés et testés :</p>
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
        <p class="custom-p"><strong>>>></strong> Le modèle de classification le plus performant est le modèle <strong>XGBClassifier</strong>.<br>
        Pour le modèle le plus performant, XGBClassifier, on obtient :</p>
        <ul class="custom-ul">
        <li><strong>Exactitude (Accuracy) : 82.93% </strong> - Cela signifie que le modèle prédit correctement la catégorie liée à l’objectif d’un temps d'arrivée inférieur à 6 min dans environ 83% des cas.</li>
        <li><strong>Rappel (Recall) : 88.06% </strong> - Une valeur élevée indique que le modèle est particulièrement bon pour prédire correctement les cas où les camions de pompiers arrivent rapidement (classe positive) et minimise le nombre de Faux Négatifs (Nb de positifs classés négatifs lors de la prédiction).</li>
        <li><strong>Précision : 83.29% </strong> - Cela montre que parmi les prédictions de classe positive du modèle, environ 83% sont correctes.</li>
        <li><strong>F1 Score : 85.61% </strong> - Cette métrique combinant le Recall et la Precision indique une efficacité globale élevée du modèle, de 85.61%.</li>
        <li><strong>AUC-ROC : 82.01% </strong> - Cette métrique, qui mesure la capacité du modèle à distinguer entre les classes, est également assez élevée, à 82.01%.</li>
        </ul>
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
        <p class="custom-p">Ci-dessous un graphe visualisant par ordre d'importance décroissante les <strong>caractéristiques les plus influentes</strong> dans les prédictions du modèle XGBClassifier.</p>
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
        <li><strong>Dist_trajet_Incident_DeployedFromStation</strong> : Distance en m de l'itinéraire le plus court entre la caserne de départ (mobilisée suite à l'appel au 999) et le lieu de l'incident./li>
        <li><strong>DeployedFrom_egalA_IncidentGround_Station</strong> : Permet d’identifier si le camion déployé sur le lieu d’incident suite à l’appel au 999 part d'une caserne différente de celle liée au lieu d’incident.</li>  
        <li><strong>Inner_Outer</strong> : Situation de l’incident dans un arrondissement du centre ou en périphérie de Londres. Permet d'identifier si le district (borough) du lieu d'incident fait partie de l'Inner London ou de l'Outer London.</li>
        </ul>
        """, unsafe_allow_html=True)



#############################################
elif page == pages[7]:
    st.write("### Prédictions sur de nouvelles données")


#############################################
elif page == pages[8]:
    st.write("### Conclusions métier")


#############################################
elif page == pages[9]:
    st.write("### Perspectives d'amélioration")
             

