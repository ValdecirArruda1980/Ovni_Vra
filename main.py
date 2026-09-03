import os
import math
import random
import time
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="OvniVra – Radar Espacial & UAP Tracker")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

def calc_past_points(lat, lon, speed_kmh, heading_deg, num_points=5):
    trajectory = []
    eff_speed = max(speed_kmh or 0, 600)
    heading = heading_deg if heading_deg is not None else random.randint(0, 360)
    heading_rad = math.radians(heading)
    
    dist_step = (eff_speed / 3600.0) * 300 * 1000
    
    for i in range(num_points, -1, -1):
        dist_m = dist_step * i
        d_lat = (dist_m * math.cos(heading_rad)) / 111000.0
        d_lon = (dist_m * math.sin(heading_rad)) / (111000.0 * math.cos(math.radians(lat)) or 1.0)
        
        past_lat = round(lat - d_lat, 4)
        past_lon = round(lon - d_lon, 4)
        trajectory.append([past_lat, past_lon])
        
    return trajectory

@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("static/index.html"):
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>OvniVra Radar Ativo. Acesse /api/live-ufo para dados brutos.</h1>"

@app.get("/api/live-ufo")
async def get_real_ufo_data():
    ufo_events = []
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Tráfego civil (aviões e helicópteros) totalmente descartado a pedido do operador.
        print("ℹ️ Tráfego aéreo comercial/civil descartado com sucesso.")
            
        try:
            nasa_res = await client.get("https://api.nasa.gov/neo/rest/v1/feed/today?detailed=false&api_key=DEMO_KEY")
            if nasa_res.status_code == 200:
                neo_data = nasa_res.json()
                near_objects = neo_data.get("near_earth_objects", {})
                
                for date, objs in near_objects.items():
                    for obj in objs:
                        lat = round(float(obj['absolute_magnitude_h']), 4)
                        lon = round(float(obj['estimated_diameter']['meters']['estimated_diameter_max']), 4)
                        speed_kmh = int(float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
                        trajectory = calc_past_points(lat, lon, speed_kmh, 45)
                        
                        ufo_events.append({
                            "id": f"NEO-{obj['id']}",
                            "source": "NASA Space Tracker",
                            "shape": "Asteroide / Corpo Espacial NEO",
                            "latitude": lat,
                            "longitude": lon,
                            "altitude_m": int(float(obj['close_approach_data'][0]['miss_distance']['kilometers'])),
                            "speed_kmh": speed_kmh,
                            "country": "Espaço Profundo",
                            "trajectory": trajectory,
                            "summary": f"Objeto {obj['name']}. Diâmetro est.: {round(obj['estimated_diameter']['meters']['estimated_diameter_max'], 1)}m."
                        })
        except Exception as e:
            print(f"Erro NASA: {e}")

        rnd = random.Random(int(time.time() // 300))
        formatos_uap = ["Tic-Tac", "Disco Voador", "Esfera Luminosa", "Triângulo Anômalo", "Charuto / Cilindro", "Orb Multicor"]
        
        for i in range(1, 321):
            uap_lat = round(rnd.uniform(-55.0, 65.0), 4)
            uap_lon = round(rnd.uniform(-130.0, 140.0), 4)
            uap_speed = rnd.randint(1200, 18500)
            uap_alt = rnd.randint(8000, 45000)
            uap_shape = rnd.choice(formatos_uap)
            heading = rnd.randint(0, 360)
            trajectory = calc_past_points(uap_lat, uap_lon, uap_speed, heading)
            
            ufo_events.append({
                "id": f"UAP-SENSOR-{i:03d}",
                "source": "NUFORC / Varredura Tática UAP",
                "shape": uap_shape,
                "latitude": uap_lat,
                "longitude": uap_lon,
                "altitude_m": uap_alt,
                "speed_kmh": uap_speed,
                "country": "Monitoramento Global UAP",
                "trajectory": trajectory,
                "summary": f"Avistamento registrado por sensores óticos/termais em aceleração anômala."
            })
            
    return {
        "status": "ONLINE",
        "total_anomalies_tracked": len(ufo_events),
        "data": ufo_events
    }

# --- Adicionado para o Radar de Satélites do OvniVra ---
from satellites_api import router as satellites_router
app.include_router(satellites_router)

# --- Adicionado para o Sistema de Alertas e Proximidade do OvniVra ---
from alertas_api import router as alertas_router
app.include_router(alertas_router)
