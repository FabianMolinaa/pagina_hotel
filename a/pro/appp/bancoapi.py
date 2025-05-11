# Importación de la librería bcchapi para interactuar con la API del Banco Central de Chile
import bcchapi #(Pip install bcchapi
# Importación de numpy (aunque no se utiliza en este código, podría ser para futuras operaciones numéricas)
import numpy as np
# Importación de datetime para manejo de fechas
from datetime import datetime
# Importación del módulo de expresiones regulares para procesamiento de texto
import re
# Creación de una instancia de conexión con la API del BCCH
# Se autentica con email y contraseña
siete = bcchapi.Siete("fa.molinao@duocuc.cl", "")
# Obtención de la fecha actual en formato YYYY-MM-DD para usarla en la consulta
fec = datetime.now().strftime("%Y-%m-%d")
# Realización de la consulta al BCCH para obtener el tipo de cambio:
# - series=["F073.TCO.PRE.Z.D"]: Consulta la serie de tipo de cambio pesos por dólar
# - nombres=["Tipo_Cambio"]: Asigna este nombre a la columna de resultados
# - desde=fec: Filtra los datos desde la fecha actual
buscar = siete.cuadro(
        series=["F073.TCO.PRE.Z.D"],  
        nombres=["Tipo_Cambio"],
        desde=fec,
)
# Conversión del resultado a string para poder procesarlo con expresiones regulares
ada = str(buscar)
# Extracción del valor numérico del tipo de cambio:
# 1. re.findall(r'\b\d+\b', ada): Busca todos los números enteros en el string
# 2. [3]: Selecciona el cuarto número encontrado (índice 3)
#    (Los primeros son probablemente el año, mes y día de la fecha)
dolar = (re.findall(r'\b\d+\b', ada)[3])
# Impresión del valor del dólar obtenido
print(re.findall(r'\b\d+\b', ada)[3])
