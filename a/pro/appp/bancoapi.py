import bcchapi 
import numpy as np
from datetime import datetime
import re

siete = bcchapi.Siete("fa.molinao@duocuc.cl", "F21756060-8")

fec = datetime.now().strftime("%Y-%m-%d")


buscar = siete.cuadro(
        series=["F073.TCO.PRE.Z.D"],  
        nombres=["Tipo_Cambio"],
        desde=fec,
    )

ada=str(buscar)
dolar=(re.findall(r'\b\d+\b',ada)[3])
print(re.findall(r'\b\d+\b',ada)[3])
