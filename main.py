from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
import subprocess

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
subprocess.call(["python", "dolar.py"])

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.on_event('startup')
def startup():
    global df_dolar_blue, df_dolar_oficial
    df_dolar_blue = pd.read_csv("datasets/dolar_blue/dolar_blue.csv")
    df_dolar_oficial = pd.read_csv("datasets/dolar_oficial/dolar_oficial.csv")
    
@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}

# @app.on_event('startup')
# def startup():
#     global df_dolar_blue, df_dolar_oficial
#     df_dolar_blue = pd.read_csv("datasets/dolar_blue/dolar_blue.csv")
#     df_dolar_oficial = pd.read_csv("datasets/dolar_oficial/dolar_oficial.csv")

# @app.get("/")
# async def root():
#     return HTMLResponse(html)

@app.get('/get_tipo_cambio/{tipo}')
def obrtener_tipo_cambio_oficial_blue(tipo: str):
    
    if tipo == 'oficial':
        dolar_oficial_compra = df_dolar_oficial['compra'].iloc[0]
        dolar_oficial_venta = df_dolar_oficial['venta'].iloc[0]
        dolar_oficial_fecha = df_dolar_oficial['fechaActualizacion'].iloc[0]
        return f'El dólar {tipo} es para compra: {dolar_oficial_compra}  Venta: {dolar_oficial_venta}. Ultima fecha de actualizacion: {dolar_oficial_fecha}'

    elif tipo == 'blue':
        dolar_blue_compra = df_dolar_blue['compra'].iloc[-1]
        dolar_blue_venta = df_dolar_blue['venta'].iloc[-1]
        dolar_blue_fecha = df_dolar_blue['fechaActualizacion'].iloc[-1]
        
        return f'El dólar {tipo} es para la Compra: {dolar_blue_compra} y para la Venta: {dolar_blue_venta}. Ultima fecha de actaulizacion: {dolar_blue_fecha}'
