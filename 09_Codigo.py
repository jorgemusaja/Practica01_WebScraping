# -*- coding: utf-8 -*-
__author__ = 'JorgeCutipaMusaja'

#Importamos las librerías a utilzar
from bs4 import BeautifulSoup
import requests
import pandas as pd  

#Establecemos losvalores iniciales antes del scrapeo
url_base = "https://www.ecartelera.com/listas/mejores-peliculas/"
maximo = 7+1
contador = 0

#Creamos un objeto vacío para apilar los datos
datos = []

#Construimos un bucle
for i in range(1, maximo):

    #Bucle para la URL de cada página web
    if i>1:
        url = "%s%d/" % (url_base,i)
    else:
        url = url_base

    #Hacemos la solicitud a la página web
    get = requests.get(url)
    #Comprobamos el estado de cada página web
    estado = get.status_code
    
    #Solo se aplica "if" para un resultado satisfactorio = 200
    if estado == 200:

        #Convertimos la información html a un objeto tipo BeautifulSoup
        html = BeautifulSoup(get.text, "html.parser")
        
        sopa = html.find_all('a', {'class': 'list-gen'})

        #Construimos un bucle para capturar la información de título de la película, puesto en el ranking, año y puntaje
        for fila in sopa:
            contador += 1
            titulo = fila.find('p', {'class': 'title'}).getText()
            puesto = fila.find('div', {'class': 'count'}).getText()
            year = fila.find('div', {'class': 'year'}).getText()
            puntaje = fila.find('div', {'class': 'cgrade'}).getText()
            
            #Reemoplazamos la "," por el "." como separador de decimales
            puntaje = puntaje.replace(",",".")
            
            #Agregamos iteradamente los datos al objeto vacío
            datos.append((contador, titulo, puesto, year, puntaje))
                                               
    else:
        #Se impŕime un mensaje del tipo de error en caso que la página web no esté disponible
        print "Status Code %d" % estado

#Exportamos el contenido del objeto a un dataframe
df = pd.DataFrame(datos, columns=['ID', 'Título', 'Puesto', 'Año', 'Puntaje'])  
#Convertimos algunas variables string a numeric 
df.to_csv('10_Dataset.csv', index=False, encoding='utf-8')         



