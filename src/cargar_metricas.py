from datetime import datetime, timezone
import os
import socket

import psutil
from google.cloud import bigquery


PROJECT_ID = "project-0d90f606-e1f3-4782-b8e"
DATASET_ID = "ops_automation_dataset"
TABLE_ID = "metricas_servidores"


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


def insertar_en_bigquery(metrica):
    client = bigquery.Client(project=PROJECT_ID)

    tabla = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    errores = client.insert_rows_json(
        tabla,
        [metrica],
    )

    if errores:
        raise RuntimeError(
            f"Error insertando datos en BigQuery: {errores}"
        )


if __name__ == "__main__":
    metrica = obtener_metricas()

    print("Métrica obtenida desde el equipo local:")
    print(metrica)

    insertar_en_bigquery(metrica)

    print("Métrica insertada correctamente en BigQuery.")