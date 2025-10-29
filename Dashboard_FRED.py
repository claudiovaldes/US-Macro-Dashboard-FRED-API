import pandas as pd
from fredapi import Fred
import plotly.express as px
from dash import Dash, dcc, html
import webbrowser
import threading
import plotly.io as pio
#pio.renderers.default = "browser"  # abrirá el plot en tu navegador, sirve como pre-view

### Establecer conexion con FRED
fred_key = "6c8ef27332fc44e581fbd1d35b09f715" ### escribe tu fred API
f = Fred(api_key=fred_key)

### lista de colores bonitos para los graficos
colors = ["blue", "red", "blueviolet", "cadetblue", "darkcyan", "darkblue", "darkgreen","rebeccapurple",
          "turquoise", "darkgoldenrod", "hotpink", "steelblue", "skyblue", "mediumaquamarine"]

###---------------------------------------------------------------------------------------

### ACTIVIDAD ECONOMICA ###

### NON FARM PAYROLLS
nfp = f.get_series("PAYEMS", observation_start="2005-1-1").reset_index().dropna()
nfp.columns = ["Dates","NFP"]
fig_nfp = px.line(nfp, x="Dates", y="NFP", title="Non Farm Payrolls") 
fig_nfp.update_traces(line_color="mediumaquamarine")
fig_nfp.update_layout(template="plotly_white")

### INDICE DE PRODUCCION INDUSTRIAL
indpro = f.get_series("INDPRO", observation_start="2000-1-1", frequency="q").reset_index().dropna()
indpro.columns = ["Date", "Values"]
fig_indpro = px.line(indpro, x="Date", y="Values", title="Industrial Production Index")
fig_indpro.update_traces(line_color="steelblue")  
fig_indpro.update_layout(template="plotly_white")

### REAL GDP
real_gdp = f.get_series("GDPC1", observation_start="2000-1-1", frequency="q").reset_index().dropna()
real_gdp.columns = ["Date", "Values"]
fig_real_gdp = px.line(real_gdp, x="Date", y="Values", title="USA Real GDP")
fig_real_gdp.update_traces(line_color="darkcyan")  
fig_real_gdp.update_layout(template="plotly_white")


###---------------------------------------------------------------------------------------

### INFLACION Y CONSUMO ###

### USA CPI
cpi = f.get_series('CPIAUCSL', observation_start='2010-01-01').reset_index().dropna()
cpi.columns = ['Fecha', 'CPI']
fig_cpi = px.line(cpi, x='Fecha', y='CPI', title='USA CPI')
fig_cpi.update_traces(line_color="red")
fig_cpi.update_layout(template="plotly_white")

### USA CORE CPI 
core_cpi = f.get_series('CPILFESL', observation_start='2010-01-01').reset_index().dropna()
core_cpi.columns = ['Fecha', 'CORE CPI']
fig_core_cpi = px.line(core_cpi , x='Fecha', y='CORE CPI', title='USA CORE CPI')
fig_core_cpi.update_traces(line_color="darkred")
fig_core_cpi.update_layout(template="plotly_white")

### PCE
pce = f.get_series("PCE", observation_start="2000-1-1", frequency="m").reset_index().dropna()
pce.columns = ["Fecha","PCE"]
fig_pce = px.line(pce, x="Fecha", y="PCE", title="USA PCE")
fig_pce.update_traces(line_color="forestgreen")
fig_pce.update_layout(template="plotly_white")

###---------------------------------------------------------------------------------------

### MERCADO LABORAL ###

### USA UNEMPLOYMENT RATE
unrate = f.get_series("UNRATE", observation_start="2000-1-1").reset_index().dropna()
unrate.columns = ['Fecha', 'UNRATE']
fig_unrate = px.line(unrate, x='Fecha', y='UNRATE', title='USA Unemployment Rate')
fig_unrate.update_traces(line_color="hotpink")
fig_unrate.update_layout(template="plotly_white")

### PARTICIPACION LABORAL EN USA
part_lab = f.get_series("CIVPART", observation_start="2000-1-1").reset_index().dropna()
part_lab.columns = ['Fecha', 'Labor Force']
fig_part_lab = px.line(part_lab, x='Fecha', y='Labor Force', title='USA Labor Force Participation Rate')
fig_part_lab.update_traces(line_color="blueviolet")
fig_part_lab.update_layout(template="plotly_white")

### JOB OPENINGS 
job_openings = f.get_series("JTSJOL", observation_start="2000-1-1").reset_index().dropna()
job_openings.columns = ['Fecha', 'Job openings']
fig_job_openings = px.line(job_openings, x='Fecha', y='Job openings', title='USA Job Openings Rate')
fig_job_openings.update_traces(line_color="rebeccapurple")
fig_job_openings.update_layout(template="plotly_white")

###---------------------------------------------------------------------------------------

### POLITICA MONETARIA ###

### FED FUNDS
fed_funds = f.get_series("FEDFUNDS", observation_start="2000-1-1").reset_index().dropna()
fed_funds.columns = ['Fecha', 'rate']
fig_fed_funds = px.line(fed_funds, x='Fecha', y='rate', title='USA FED FUNDS')
fig_fed_funds.update_traces(line_color="darkgreen")
fig_fed_funds.update_layout(template="plotly_white")

### TREASURY 2Y
tsy_10 = f.get_series("DGS10", observation_start="2000-1-1").reset_index().dropna()
tsy_10.columns = ['Fecha', 'rate']
fig_tsy_10 = px.line(tsy_10 , x='Fecha', y='rate', title='USA Treasury 10Y')
fig_tsy_10.update_traces(line_color="green")
fig_tsy_10.update_layout(template="plotly_white")

### TREASURY 1OY
tsy_2 = f.get_series("DGS2", observation_start="2000-1-1").reset_index().dropna()
tsy_2.columns = ['Fecha', 'rate']
fig_tsy_2 = px.line(tsy_2 , x='Fecha', y='rate', title='USA Treasury 2Y')
fig_tsy_2.update_traces(line_color="cadetblue")
fig_tsy_2.update_layout(template="plotly_white")

###---------------------------------------------------------------------------------------

### COMMODITIES ###

#### --- OIL ---
wti = f.get_series("DCOILWTICO", observation_start="2000-1-1", frequency="d")
brent = f.get_series("DCOILBRENTEU", observation_start="2000-1-1", frequency="d")

### WTI vs BRENT
oil = pd.concat([wti, brent], axis=1, join="inner").reset_index().dropna()
oil.columns = ["Dates","WTI", "BRENT"]
fig_oil = px.line(oil, x="Dates", y=["WTI", "BRENT"])
fig_oil.update_traces(selector=dict(name="WTI"), line_color="cadetblue")
fig_oil.update_traces(selector=dict(name="BRENT"), line_color="blue")
fig_oil.update_layout(template="plotly_white")
 
###---------------------------------------------------------------------------------------

### STOCK MARKET ###

### S&P 500
sp = f.get_series("SP500", observation_start="2000-1-1", frequency="d").reset_index().dropna()
sp.columns = ["Date", "Points"]
fig_sp = px.line(sp, x="Date", y="Points", title="S&P 500")
fig_sp.update_traces(line_color="mediumaquamarine")  
fig_sp.update_layout(template="plotly_white")

### crypto currencies 
btc = f.get_series("CBBTCUSD", observation_start="2000-1-1", frequency="d").reset_index().dropna()
btc.columns = ["Date", "Points"]
fig_btc = px.line(btc, x="Date", y="Points", title="BITCOIN")
fig_btc.update_traces(line_color="skyblue")  
fig_btc.update_layout(template="plotly_white")


###---------------------------------------------------------------------------------------


### Buscar informacion en FRED 
#buscador = pd.DataFrame(f.search("GDP")) ### Ejemplo


### crear aplicacion Dash
app = Dash(__name__, external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"])
app.layout = html.Div([
    html.H1("US Macro Dashboard — FRED API", style={'textAlign': 'center', 'color': '#1f77b4'}) ,
    html.H3("Simple Dashboard interactivo en Python/Dash que visualiza indicadores macroeconómicos (CPI, PCE, NFP, FEDFUNDS, tasas, commodities y más) con datos en tiempo real desde la API de FRED.", style={"color":"#2C3E50"}),    
    html.H3("Uno de los objetivos del proyecto, es demostrar que con tan solo python, una API publica y un visualizador es posible construir herramientas de análisis potentes sin necesidad de contar con un terminal Bloomberg ni depender de plataformas como Power BI o Tableau." , style={"color":"#2C3E50"}),
    
    html.H2("ACTIVIDAD ECONOMICA", style={"textAlign":"center", "color":"#006C84"}),
    dcc.Graph(figure=fig_nfp),
    dcc.Graph(figure=fig_indpro),
    dcc.Graph(figure=fig_real_gdp),
    html.H2("INFLACION Y CONSUMO", style={"textAlign":"center", "color":"#006C84"}),
    dcc.Graph(figure=fig_cpi),
    dcc.Graph(figure=fig_core_cpi),
    dcc.Graph(figure=fig_pce),
    html.H2("MERCADO LABORAL", style={"textAlign":"center", "color":"#006C84"} ),
    dcc.Graph(figure=fig_unrate),
    dcc.Graph(figure=fig_part_lab),
    dcc.Graph(figure=fig_job_openings),
    html.H2("POLITICA MONETARIA", style={"textAlign":"center", "color":"#006C84"}),
    dcc.Graph(figure=fig_fed_funds),
    dcc.Graph(figure=fig_tsy_10),
    dcc.Graph(figure=fig_tsy_2),
    html.H2("COMMODITIES", style={"textAlign":"center", "color":"#006C84"}),
    dcc.Graph(figure=fig_oil),
    html.H2("STOCK MARKET", style={"textAlign":"center", "color":"#006C84"}),
    dcc.Graph(figure=fig_sp),
    dcc.Graph(figure=fig_btc),
    html.H2("Extras", style={"textAlign":"center", "color":"#006C84"}),
    html.H3('En la variable comentada #buscador, puedes buscas más categorias de datos --> #buscador = pd.DataFrame(f.search("GDP")) ###Ejemplo buscar "GDP"', style={"color":"#2C3E50"})  
    ])

def open_browser():
    webbrowser.open("http://127.0.0.1:8050")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
