import os
import requests
import base64
import zipfile
import garth
from garminconnect import Garmin

email = os.environ.get("GARMIN_EMAIL")
senha = os.environ.get("GARMIN_PASSWORD")
webhook_n8n = os.environ.get("N8N_WEBHOOK")
token_b64 = os.environ.get("GARMIN_TOKEN")

try:
    client = Garmin(email, senha)

    if token_b64:
        
        with open("tokens.zip", "wb") as f:
            f.write(base64.b64decode(token_b64))
            
        with zipfile.ZipFile("tokens.zip", 'r') as zip_ref:
            zip_ref.extractall("garmin_tokens")
            
        garth.resume("garmin_tokens")
        client.garth = garth.client
        
    else:
        client.login()
        
    treinos = client.get_activities(0, 5) 

    if treinos:
        payload = []
        for treino in treinos:
            duracao_segundos = treino.get("duration")
            
            payload.append({
                "id_treino": str(treino.get("activityId")), 
                "nome_treino": treino.get("activityName"),
                "distancia_metros": treino.get("distance"),
                "tempo_minutos": round(duracao_segundos / 60, 2) if duracao_segundos else None,
                "calorias": treino.get("calories"),
                "data_inicio": treino.get("startTimeLocal"),
                "bpm_medio": treino.get("averageHR"),
                "bpm_maximo": treino.get("maxHR") 
            })
            
        resposta = requests.post(webhook_n8n, json={"treinos": payload})

except Exception as e:
    print(f"Erro na sincronização: {e}")
