from datetime import datetime, timezone
import os
import socket

import psutil
import requests

API_URL = "http://127.0.0.1:8000/metricas"

def obtener_metricas():
    cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory().percent

    unidad = os.getenv("SystemDrive", "C:") + "\\"
    disco = psutil.disk_usage(unidad).percent

    if cpu >= 85 or memoria >= 85 or disco >= 90:
        estado = "CRITICAL"
    elif cpu >= 70 or memoria >= 70 or disco >= 75:
        estado = "WARNING"
    else:
        estado = "OK"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "servidor": socket.gethostname(),
        "ambiente": "local",
        "cpu_porcentaje": round(cpu, 2),
        "memoria_porcentaje": round(memoria, 2),
        "disco_porcentaje": round(disco, 2),
        "estado": estado,
    }


def enviar_metrica(metrica):
    respuesta = requests.post(
        API_URL,
        json=metrica,
        timeout=10
    )

    respuesta.raise_for_status()

    return respuesta.json()


if __name__ == "__main__":
    metrica = obtener_metricas()

    print("Métrica obtenida desde el equipo local:")
    print(metrica)

    resultado = enviar_metrica(metrica)

    print("Respuesta de la API:")
    print(resultado)
    