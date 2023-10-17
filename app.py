# Importar Bibliotecas ------------------------------------------------------------------------------------------------------

import streamlit as st
import streamlit_folium
import base64

import pandas as pd
import numpy as np
import random

from math import ceil

import folium

# Configurar Página ---------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Optimización de distribución de bicicletas en estaciones de MiBici",
    page_icon="🚲"
)

#st.markdown('images/miBici.gif',unsafe_allow_html = True)
#st.image("images/miBici.gif", caption = 'Este proyecto se realizó con datos abiertos de MiBici', use_column_width=True)

st.title("Optimización de distribución de bicicletas en estaciones de MiBici")

# Cargar datos --------------------------------------------------------------------------------------------------------------

@st.cache_data  # Caché para acelerar la lectura de datos

def cargar_datos(nombre_archivo, encoding):
    data = pd.read_csv(nombre_archivo, encoding=encoding)
    return data

archivo1 = 'data/merge.csv'
data = cargar_datos(archivo1, encoding='utf-8')

archivo2 = 'data/nomenclatura.csv'
data2 = cargar_datos(archivo2, encoding='ISO-8859-1')


# Funciones -----------------------------------------------------------------------------------------------------------------

## Demanda 

def al_dia(n):
    b = ((n / 4) / 7) / 19
    
    if b < 5:
        return 5
    else:
        return ceil(b)

def demanda_por_mes(mes):

    df_mes = data[data['Inicio_del_viaje'] == mes]
    frecuencia_origen = df_mes['Origen_Id'].value_counts()
    frecuencia_origen = frecuencia_origen.reset_index()
    frecuencia_origen.sort_values('index', inplace = True)
        
    frecuencia_destino = df_mes['Destino_Id'].value_counts()
    frecuencia_destino = frecuencia_destino.reset_index()
    frecuencia_destino.sort_values('index', inplace = True)
        
    frecuencias = pd.concat([frecuencia_origen['index'], frecuencia_origen['Origen_Id'],
                         frecuencia_destino['Destino_Id']], axis = 1)
                        
    frecuencias.reset_index(inplace = True)
    
    num_estaciones = 300
    
    num_bicis = [ceil((al_dia(frecuencias['Origen_Id'][x]) + al_dia(frecuencias['Destino_Id'][x])) / 2) for x in range(num_estaciones)]
    
    return num_bicis


n = 300
miu = 5.5

def generar_individuos(n, miu):
    numeros_aleatorios = np.random.normal(miu, 1.0, n)
    #numeros_aleatorios = np.clip(numeros_aleatorios, lower_bound, upper_bound)
    return list(map(int, numeros_aleatorios))

def inicializar_poblacion(tamano_poblacion, num_estaciones, limite_bicicletas):
    poblacion = []
    
    for _ in range(tamano_poblacion):
        asignacion = generar_individuos(300, 5.5)
        while sum(asignacion) != limite_bicicletas:
            asignacion = generar_individuos(300, 5.5)
        poblacion.append(asignacion)
    return poblacion

def evaluar_poblacion(poblacion, demanda_estaciones, limite_bicicletas):
    evaluaciones = []
    for asignacion in poblacion:
        exceso_bicicletas = sum(asignacion) - limite_bicicletas
        evaluacion = sum(np.abs(np.array(asignacion) - np.array(demanda_estaciones)))
        if exceso_bicicletas > 0:
            evaluacion += exceso_bicicletas  # Penaliza el exceso de bicicletas
        evaluaciones.append(evaluacion)
    return evaluaciones


def seleccionar_mejores_padres(poblacion, evaluaciones, num_padres):
    padres = [poblacion[i] for i in np.argsort(evaluaciones)[:num_padres]]
    return padres

def cruzar_padres(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

def mutar(individuo, prob_mutacion):
    for i in range(len(individuo)):
        if random.random() < prob_mutacion:
            individuo[i] = random.randint(1, 20)
    return individuo

def texto_genetico(num_estaciones, demanda_estaciones, 
                   num_generaciones, tamano_poblacion, 
                   prob_mutacion, limite_bicicletas, elitismo_ratio):

    poblacion = inicializar_poblacion(tamano_poblacion, num_estaciones, limite_bicicletas)

    for generacion in range(num_generaciones):
        evaluaciones = evaluar_poblacion(poblacion, demanda_estaciones, limite_bicicletas)
        mejores_padres = seleccionar_mejores_padres(poblacion, evaluaciones, tamano_poblacion // 2)

        # Conservar una parte de los mejores individuos (elitismo)
        num_elitistas = int(tamano_poblacion * elitismo_ratio)
        poblacion_elitista = poblacion[:num_elitistas]

        nueva_generacion = []
        while len(nueva_generacion) < tamano_poblacion - num_elitistas:
            padre1, padre2 = random.sample(mejores_padres, 2)
            hijo1, hijo2 = cruzar_padres(padre1, padre2)
            hijo1 = mutar(hijo1, prob_mutacion)
            hijo2 = mutar(hijo2, prob_mutacion)

            if sum(hijo1) > limite_bicicletas:
                hijo1 = mutar(hijo1, prob_mutacion)
            if sum(hijo2) > limite_bicicletas:
                hijo2 = mutar(hijo2, prob_mutacion)

            nueva_generacion.extend([hijo1, hijo2])

        # Combinar la población elitista con la nueva generación
        poblacion = poblacion_elitista + nueva_generacion

    mejor_asignacion = poblacion[np.argmin(evaluaciones)]
    
    asignacion_df = pd.DataFrame()
    
    ids = [2,
 3,
 4,
 5,
 6,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 23,
 24,
 25,
 26,
 27,
 28,
 29,
 30,
 31,
 32,
 33,
 34,
 35,
 36,
 37,
 38,
 39,
 40,
 41,
 42,
 43,
 44,
 45,
 46,
 47,
 48,
 49,
 50,
 51,
 52,
 53,
 54,
 55,
 56,
 57,
 58,
 59,
 60,
 61,
 62,
 63,
 64,
 65,
 66,
 67,
 68,
 69,
 70,
 71,
 72,
 73,
 74,
 75,
 76,
 77,
 78,
 79,
 80,
 81,
 82,
 83,
 84,
 85,
 86,
 87,
 88,
 91,
 92,
 93,
 94,
 95,
 96,
 98,
 100,
 101,
 102,
 103,
 104,
 105,
 106,
 107,
 108,
 110,
 111,
 112,
 115,
 117,
 118,
 119,
 120,
 125,
 126,
 127,
 128,
 129,
 130,
 131,
 132,
 133,
 134,
 135,
 136,
 137,
 139,
 140,
 141,
 142,
 143,
 144,
 145,
 146,
 148,
 150,
 151,
 152,
 153,
 154,
 155,
 156,
 157,
 158,
 159,
 160,
 161,162,163,164,
 165,
 166,
 167,
 168,
 169,
 170,
 171,
 172,
 173,
 174,
 175,
 176,
 177,
 178,
 179,
 180,
 181,
 182,
 183,
 184,
 185,
 186,
 187,
 188,
 189,
 190,
 191,
 192,
 193,
 194,
 195,
 196,
 197,
 198,
 199,
 200,
 201,
 202,
 203,
 204,
 205,
 206,
 207,
 208,
 209,
 210,
 211,
 212,
 213,
 214,
 215,
 216,
 217,
 218,
 219,
 220,
 221,
 222,
 224,
 225,
 226,
 227,
 228,
 229,
 230,
 231,
 232,
 233,
 234,
 235,
 236,
 237,
 238,
 239,
 240,
 241,
 242,
 243,
 244,
 246,
 247,
 248,
 249,
 251,
 253,
 254,
 255,
 256,
 257,
 258,
 259,
 260,
 261,
 262,
 263,
 264,
 265,
 266,
 267,
 268,
 269,
 270,
 271,
 272,
 273,
 274,
 275,
 276,
 277,
 278,
 279,
 280,
 281,
 282,
 283,
 284,
 285,
 286,
 287,
 288,
 289,
 290,
 291,
 292,
 293,294,
 295,
 296,
 302,
 303,
 304,
 305,
 306,
 307,
 308,
 309,
 310,
 311,
 312,
 313,
 314,
 315,
 316,
 317,
 318,
 319,
 320,
 321,
 322,
 323,
 324,
 325,
 326,
 327]
    
    asignacion_df['id_estacion'] = ids
    asignacion_df['mejor_asignacion'] = mejor_asignacion
    #print(demanda_estaciones)
    st.write(f'La demanda que hay es de: {sum(demanda_estaciones)} bicicletas')
    st.write(f'\nPero la cantidad de bicicletas es de: {limite_bicicletas}')
    st.write("\nMejor asignación de bicicletas en estaciones:", asignacion_df)
    st.write(f"\nDe esa manera, solo queda una deficiencia en la demanda de: {sum(demanda_estaciones) - sum(mejor_asignacion)} bicicletas")

    
    return

def asignacion_genetico(num_estaciones, demanda_estaciones, 
                   num_generaciones, tamano_poblacion, 
                   prob_mutacion, limite_bicicletas, elitismo_ratio):

    poblacion = inicializar_poblacion(tamano_poblacion, num_estaciones, limite_bicicletas)

    for generacion in range(num_generaciones):
        evaluaciones = evaluar_poblacion(poblacion, demanda_estaciones, limite_bicicletas)
        mejores_padres = seleccionar_mejores_padres(poblacion, evaluaciones, tamano_poblacion // 2)

        # Conservar una parte de los mejores individuos (elitismo)
        num_elitistas = int(tamano_poblacion * elitismo_ratio)
        poblacion_elitista = poblacion[:num_elitistas]

        nueva_generacion = []
        while len(nueva_generacion) < tamano_poblacion - num_elitistas:
            padre1, padre2 = random.sample(mejores_padres, 2)
            hijo1, hijo2 = cruzar_padres(padre1, padre2)
            hijo1 = mutar(hijo1, prob_mutacion)
            hijo2 = mutar(hijo2, prob_mutacion)

            if sum(hijo1) > limite_bicicletas:
                hijo1 = mutar(hijo1, prob_mutacion)
            if sum(hijo2) > limite_bicicletas:
                hijo2 = mutar(hijo2, prob_mutacion)

            nueva_generacion.extend([hijo1, hijo2])

        # Combinar la población elitista con la nueva generación
        poblacion = poblacion_elitista + nueva_generacion

    mejor_asignacion = poblacion[np.argmin(evaluaciones)]

    return mejor_asignacion


data2 = pd.read_csv('data/nomenclatura.csv', encoding='ISO-8859-1')

def mapa(data2, num_estaciones, demanda, 
                       num_generaciones, tamano_poblacion, 
                       prob_mutacion, limite_bicicletas, elitismo_ratio):

    data2 = data2.loc[data2['status'] == 'IN_SERVICE']
    data2.reset_index(inplace = True)

    info = ['Número óptimo bicicletas: '+str(x) for x in asignacion_genetico(num_estaciones, demanda, 
                       num_generaciones, tamano_poblacion, 
                       prob_mutacion, limite_bicicletas, elitismo_ratio)]

    data2['asignacion'] = info
    
    lat = 20.66682
    lon = -103.39182

    m = folium.Map(location=(lat,lon),zoom_start=12)
    icon_path = 'data/bike1.ico'

    for i in range(len(data2['latitude'])):
        lat = data2['latitude'][i]
        lon = data2['longitude'][i]
        info = data2['asignacion'].loc[i]
        custom_icon = folium.CustomIcon(
            icon_image=icon_path,
            icon_size=(30, 30)  # Tamaño del icono
        )

        mark = folium.Marker(location=(lat, lon), popup=info, icon=custom_icon)
        mark.add_to(m)

    #display(m)
    return m

def main():
    mensaje_inicial = st.empty()
    
    mensaje_inicial.subheader("Presiona el botón: 'Generar Resultados' en el menú de parámetros para generar la información")
    
    num_estaciones = 300
    #demanda_estaciones = demanda_por_mes(mes)

    # Parámetros del algoritmo genético
    num_generaciones = 100
    tamano_poblacion = 50
    prob_mutacion = 0.1

    limite_bicicletas = 1500 #1600#3200  # Límite de bicicletas

    elitismo_ratio = 0.1  # Porcentaje de individuos elítistas a conservar
    
    # Menú desplegable para seleccionar mes
    st.sidebar.title("Menú de Parámetros")
    
    traduccion = {'Enero':'January', 
                  'Febrero':'February', 
                  'Marzo':'March', 
                  'Abril':'April', 
                  'Mayo':'May', 
                  'Junio':'June', 
                  'Julio':'July', 
                  'Agosto':'August', 
                  'Septiembre':'September'}
    
    mes = st.sidebar.selectbox('Selecciona el mes:', ['Enero', 'Febrero', 'Marzo', 'April', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre'])

    # Botón para generar resultados
    if st.sidebar.button('Generar Resultados'):
        mensaje_inicial.empty()
        col1, col2 = st.columns(2)
        with col1:
            
            texto_genetico(num_estaciones, demanda_por_mes(traduccion[mes]), 
                       num_generaciones, tamano_poblacion, 
                       prob_mutacion, limite_bicicletas, elitismo_ratio)

            m = mapa(data2, num_estaciones, demanda_por_mes(traduccion[mes]), 
                           num_generaciones, tamano_poblacion, 
                           prob_mutacion, limite_bicicletas, elitismo_ratio)

            streamlit_folium.folium_static(m, width=800, height=600)
        
        with col2:
            file_ = open("images/miBici.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            # Especificar el ancho y alto deseados en píxeles
            width = 300  # Ancho deseado
            height = 200  # Alto deseado

            # Usar la etiqueta HTML para mostrar el GIF con el estilo especificado
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="miBici" width={width} height={height} style="display: block; margin: 0 auto; text-align: center;">',
                unsafe_allow_html=True
            )

    # Notas
    st.sidebar.info("Esta aplicación permite calcular la distribución óptima de bicicletas en las estaciones del servicio MiBici en Jalisco acorde a su demanda y a la disponibilidad de bicicletas en un mes determinado")
    # Créditos y fuente de datos
    st.sidebar.subheader("Síguenos en Github: 👇")

    st.sidebar.write("[manuelsolan_o](https://github.com/manuelsolan-o)")

    st.sidebar.write("[Aleevz](https://github.com/Aleevz)")

    st.sidebar.write("[jcyamuni44](https://github.com/josecyamuni)")
    
    st.sidebar.write("[JAJP2203](https://github.com/JAJP2203)")

if __name__ == '__main__':
    
    main()
    
    #main()
        
    
    
    
