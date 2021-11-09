#import des différentes librairies.
import pandas as pd
import folium 
import geopandas as gpd
import numpy as np
import branca.colormap as cm

import plotly.express as px
import plotly.graph_objs as go

from plotly import __version__ 

import dash  
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)



#----------------------------------------------------------------------------------------
#import des valeurs et de certaines variables
def import_clean():
    """ Crée et retourne (companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog), qui vont nous servir pour la carte et pour les plots"""
    dep = 'DEPnb'
    firm_val = 'FIRM'
    firmlog = 'FIRMLOG'


    companies = pd.read_csv('base_etablissement_par_tranche_effectif.csv', low_memory=False, delimiter=',', encoding="utf-8") 
    geoinf = pd.read_csv('name_geographic_information.csv', low_memory=False, delimiter=',', encoding="utf-8") 
    salaries = pd.read_csv('net_salary_per_town_categories.csv', low_memory=False, delimiter=',', encoding="utf-8") 
      
    l=[companies, geoinf, salaries ] # liste avec nos 3 dataframes

    # Données géographiques
    geo_data = "./departements.geojson"
    geo_dep = gpd.read_file(geo_data)

    # Création d'un dictionnaire avec les futurs noms de nos colonnes
    companies_col = {'CODGEO' : 'CODGEO','LIBGEO' : 'TOWN','REG' : 'REGION_nb','DEP' : 'DEPnb','E14TST' : 'FIRM','E14TS0ND' :' UNKNOW','E14TS1' : '1to5','E14TS6' : '6to9','E14TS10' : '10to19','E14TS20' : '20to49','E14TS50' : '50to99','E14TS100' : '100to199','E14TS200' : '200to499','E14TS500' : '500+'}
    geoinf_col ={'EU_circo' : 'EU_circo','code_région' : 'REGION_nb','nom_région' : 'REGION','chef.lieu_région' : 'chef.lieu_région','numéro_département' : 'DEPnb','nom_département' : 'DEP','préfecture' : 'PREFECTURE','numéro_circonscription' : 'CIRCONSCRIPTION_nb','nom_commune' : 'TOWN','codes_postaux' : 'POSTCODE','code_insee' : 'INSEE','latitude' : 'LAT','longitude' : 'LONG','éloignement' : 'will_suppr'}
    salaries_col= {'CODGEO' : 'CODGEO','LIBGEO' : 'TOWN','SNHM14' : 'MEAN','SNHMC14' : 'EXECUTIVE','SNHMP14' : 'MIDDLEMANAGER','SNHME14' : 'EMPLOYEE','SNHMO14' : 'WORKER','SNHMF14' : 'WOMEN','SNHMFC14' : 'W_EXECUTIVE','SNHMFP14': 'W_MIDDLEMANAGER','SNHMFE14' : 'W_EMPLOYEE','SNHMFO14' : 'W_WORKER','SNHMH14' : 'MEN','SNHMHC14' : 'M_EXECUTIVE','SNHMHP14' : 'M_MIDDLEMANAGER','SNHMHE14' : 'M_EMPLOYEE','SNHMHO14' : 'M_WORKER','SNHM1814': '18to25','SNHM2614' : '26to50','SNHM5014' : '50+','SNHMF1814' : 'W-18to25','SNHMF2614' : 'W_26to50','SNHMF5014' : 'W_50+','SNHMH1814' : 'M_18to25','SNHMH2614' : 'M_26to50','SNHMH5014' : 'M50+'}
    col=[companies_col,geoinf_col,salaries_col]

    # Changement de nom des colonnes
    i=0
    for df in l :
        df = df.rename(columns=col[i], inplace=True)
        i=i+1


    return companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog


#----------------------------------------------------------------------------------------
def dataframe():
    """ Creation/update des dataframe, pour qu'ils aient le bon format pour nos autres fonctions. Retourne (firm, geo_dep, colormap, wage_gap) Tous sont des DataFrame, sauf colormap qui est un branca.colormap.StepColormap"""
    companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog = import_clean()
    #Creation d'un df regroupant les departement, et mise à l'echelle logarithmique pour avoir une carte avec une echelle cohérente
    firm =companies[[dep,firm_val]].groupby(dep)
    firm = firm.sum()
    firm.reset_index(inplace=True)
    firm['FIRMLOG'] = firm['FIRM'].apply(np.log)

    geo_dep.rename(columns={"code":"DEPnb"}, inplace=True)
    geo_dep = geo_dep.merge(firm, on='DEPnb')

    # Création d'une échelle de couleurs pértinentes pour la carte
    colormap = cm.linear.YlGnBu_09.to_step(data=geo_dep[firmlog], method='quant', quantiles=[0,0.5,0.8,0.95,0.99,1])
    
    # Creation d'un dataframe permettant de mesurer l'écart salarial homme-femme
    salaries['wage_gap'] = salaries['MEN'] - salaries['WOMEN']

    wage_gap = pd.DataFrame({'Mean Wages':salaries["MEAN"], 'Wage Gap': salaries["wage_gap"]})



    return firm, geo_dep, colormap, wage_gap

#----------------------------------------------------------------------------------------
def chloro_map():
    """ Creation de notre carte, qui sera créee et stockée dans un fichier html avant d'être réutilisée. Ne retourne rien"""
    companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog = import_clean()
    firm, geo_dep, colormap, wage_gap = dataframe()

    sample_map = folium.Map(location=[47, 3.5], zoom_start=6,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(sample_map)
    colormap.caption = "Firmes par departements (base logarithmique)"

    style_function = lambda x: {"weight":0.5, 
                                'color':'black',
                                'fillColor':colormap(x['properties'][firmlog]), 
                                'fillOpacity':0.75}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    DISP = folium.features.GeoJson(
        data=geo_dep,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=[dep,firm_val],
            aliases=['Departement: ','Nombre de firmes:'],
            style=("background-color: #DFE0FA; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
            sticky=True
        )
    )
    colormap.add_to(sample_map)
    sample_map.add_child(DISP)
    sample_map.save('map.html')
    return None


#----------------------------------------------------------------------------------------
def bar_plot():
    """ Creation d'un bar plot regroupant les salaires horaires en fonction des différents postes. retourne une figure (fig) de type plotly.graph_objs._figure.Figure"""
    companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog = import_clean()
    # Definition et formatage des différents postes
    positions = ["Executive", "Middle manager", "Employee", "Worker"]
    woman_positions = ["W_EXECUTIVE", "W_MIDDLEMANAGER", "W_EMPLOYEE", "W_WORKER"]
    woman_salary_positions = salaries[woman_positions].mean().tolist()
    man_positions = ["M_EXECUTIVE", "M_MIDDLEMANAGER", "M_EMPLOYEE", "M_WORKER"]
    man_salary_positions = salaries[man_positions].mean().tolist()
    positions_men_women=["EXECUTIVE", "MIDDLEMANAGER", "EMPLOYEE", "WORKER"]
    salary_positions = salaries[positions_men_women].mean().tolist()


    # Création des différentes grandeurs que nous allons tracer (homme/ femme/ global)
    trace = go.Bar(x = positions,y = woman_salary_positions,name='Femme',
    marker=dict(
        color='rgb(55, 83, 109)'
    ))
    trace2 = go.Bar(x = positions,y = man_salary_positions,name='Homme',
        marker=dict(
            color='rgb(26, 118, 255)'
        ))

    trace3 = go.Bar(x = positions,y = salary_positions,name='Global',
        marker=dict(
            color='rgb(0, 83, 230)'
        ))


    data = [trace, trace2, trace3]
    # Création et affichage de la figure
    layout = go.Layout(
        title='Salaires moyens horaires',
        xaxis=dict(
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='Salaire net par heure',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
        )
    fig = go.Figure(data=data, layout=layout)

    return fig

#----------------------------------------------------------------------------------------
def dashboard():
    """ Création du dashboard avec dash et affichagee des différents éléments. Ne retourne rien"""
    firm, geo_dep, colormap, wage_gap = dataframe()
    companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog = import_clean()
    salaries_list = salaries.columns.values.tolist()

    gap = px.line(wage_gap)
    fig = bar_plot()

    app.layout = html.Div(style={'backgroundColor': '#2F336E'}, children=[
        html.H1("L'emploi en France", style={'text-align': 'center', 'color' : '#FFFFFF', 'backgroundColor': '#1D2941'}),

        html.Br(),

        html.H2("Répartition des salaire à l'heure en fonction de l'âge", style={'text-align': 'center','color' : '#DFE0FA'}),


        dcc.Dropdown(id='slct_age',
                    options=[
                        {"label": "Salaire 18-25 ans", "value": '18to25'}, 
                        {"label": "Salaire 26-50 ans", "value": '26to50'}, 
                        {"label": "Salaire 50 ans ou plus", "value": '50+'} 
                            ],
                    multi=False,
                    value='18to25',
                    style={'width': "35%"}
                    ),

        
        # Affichage des histogrammes
        dcc.Graph(id='histo', figure={}),


        html.Br(),

        # Affichage des écarts salariales
        html.H2("Ecarts salariales Homme-Femme sur les différentes villes", style={'text-align': 'center','color' : '#DFE0FA'}),
        dcc.Graph(figure=gap),

        html.Br(),

        html.H2("Salaires moyens en fonction du poste", style={'text-align': 'center','color' : '#DFE0FA'}),


        # Affichage du barplot
        dcc.Graph(figure=fig, style={'margin-left': '20%', 'margin-right': '20%'}),




        html.Br(),

        # Affichage de la map
        html.H2("Nombre de firmes par départements", style={'text-align': 'center','color' : '#DFE0FA'}),
        html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='80%', height='600', style={'margin-left': '10%', 'margin-right': '10%', "border":{"width":"10px", "color":"#2c418e"},'border-radius':'8%'})

        
    ])
    @app.callback(
        [Output(component_id='histo', component_property='figure')],
        [Input(component_id='slct_age', component_property='value')]
    )


    def update_graph(option_slctd):
        """ Fonction permettant l'update de l'histogramme. Elle prend en argument l'age choisi(chaine de caractères). Retourne une liste contenant notre figure (histogramme)"""
        histo = px.histogram(salaries,
                            x=option_slctd, 
                            range_x=[7.5,30],
                            range_y=[0,600])

        
        return [histo]

    return None

#----------------------------------------------------------------------------------------
def main():
    """ Fonction permettant de lancer les fonctions principales"""
    # Création / nettoyage / organisation des DataFrames
    dataframe()
    # Création et stockage de la carte
    chloro_map()
    # Création du dashboard
    dashboard()


if __name__ == '__main__':
    # Lancement des fonctions principales
    main()
    # Lancement du serveur
    app.run_server(debug=False)