from datetime import datetime

from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from pydantic import BaseModel


PROJECT_ID = "project-0d90f606-e1f3-4782-b8e"
DATASET_ID = "ops_automation_dataset"
TABLE_ID = "metricas_servidores"


app = FastAPI(
    title="CloudOps Metrics API",
    version="1.0.0"
)


class MetricaServidor(BaseModel):
    timestamp: datetime
    servidor: str
    ambiente: str
    cpu_porcentaje: float
    memoria_porcentaje: float
    disco_porcentaje: float
    estado: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/metricas")
def recibir_metrica(metrica: MetricaServidor):
    client = bigquery.Client(project=PROJECT_ID)

    tabla = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    datos = metrica.model_dump(mode="json")

    errores = client.insert_rows_json(
        tabla,
        [datos]
    )

    if errores:
        raise HTTPException(
            status_code=500,
            detail=errores
        )

    return {
        "mensaje": "Métrica almacenada correctamente",
        "servidor": metrica.servidor
    }