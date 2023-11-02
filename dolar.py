import requests
import pandas as pd
from datetime import datetime, date, timedelta
import os

base_url = "https://dolarapi.com"
endpoint_dolar_oficial = "/v1/dolares/oficial"
endpoint_dolar_blue = "/v1/dolares/blue"
endpoint_dolares = "/v1/dolares"

def build_table(json_data):
    df = pd.json_normalize(json_data)
    return df

def get_data(base_url, endpoint, params=None):
   
   try:
         endpoint_url = f"{base_url}/{endpoint}"
         response = requests.get(endpoint_url, params=params)
         response.raise_for_status() 
         
         data=response.json()
         df_data= build_table(data)
         return df_data
   except requests.exceptions.RequestException as e:
        print(f"La petición ha fallado. Código de error : {e}")
        return None 
    
    
dolar_blue = "datasets/dolar_blue"
dolar_oficial = "datasets/dolar_oficial"

os.makedirs(dolar_blue, exist_ok=True)
os.makedirs(dolar_oficial, exist_ok=True)




def ingesta_full_2(base_url, endpoint, folder_path, file_prefix):
    dataframe =get_data(base_url, endpoint, params=None)
    
    if isinstance(dataframe, pd.DataFrame) and not dataframe.empty:
        file_name = f"{file_prefix}.csv"
        file_path = os.path.join(folder_path, file_name)

        # Guarda el DataFrame en el archivo CSV
        dataframe.to_csv(file_path, index=False)
    else:
        print("El DataFrame no es válido o está vacío.")


folder_path = "datasets/dolar_oficial"  # Ruta de la carpeta donde deseas guardar el archivo CSV
file_prefix = 'dolar_oficial'  # Prefijo para el nombre del archivo
endpoint_dolar_oficial = "/v1/dolares/oficial" # endpoint
ingesta_full_2(base_url, endpoint_dolar_oficial, folder_path, file_prefix)



# def ingesta_incremental(base_url, endpoint, folder_path, file_prefix):
#     dataframe =get_data(base_url, endpoint, params=None)
    
#     file_name = f"{file_prefix}.csv"
#     file_path = os.path.join(folder_path, file_name)

#     if os.path.exists(file_path):
#         # Si el archivo ya existe, carga el archivo CSV existente en un DataFrame
#         existing_dataframe = pd.read_csv(file_path)

#         # Compara la columna 'fechaActualizacion' para encontrar filas actualizadas
#         updated_rows = dataframe[~dataframe['fechaActualizacion'].isin(existing_dataframe['fechaActualizacion'])]

#         if not updated_rows.empty:
#             # Agrega las filas actualizadas al DataFrame existente
#             existing_dataframe = pd.concat([existing_dataframe, updated_rows])

#             # Guarda el DataFrame combinado en el archivo CSV
#             existing_dataframe.to_csv(file_path, index=False)
#     else:
#         # Si el archivo no existe, simplemente guarda el DataFrame en un nuevo archivo
#         dataframe.to_csv(file_path, index=False)


        
folder_path_blue = "datasets/dolar_blue"  # Ruta de la carpeta donde deseas guardar el archivo CSV
file_prefix_blue = 'dolar_blue'  # Prefijo para el nombre del archivo
endpoint_dolar_blue = "/v1/dolares/blue" # endpoint
ingesta_full_2(base_url, endpoint_dolar_blue, folder_path_blue, file_prefix_blue)  
