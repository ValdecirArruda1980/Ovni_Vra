import os

main_py = """import os
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
        try:
            opensky_res = await client.get("https://opensky-network.org/api/states/all")
            if opensky_res.status_code == 200:
                data = opensky_res.json()
                states = data.get("states", []) or []
                for s in states:
                    callsign = (s[1] or "").strip()
                    country = (s[2] or "").strip()
                    lat = s[6]
                    lon = s[5]
                    altitude = s[7]
                    velocity = s[9]
                    heading = s[10]
                    
                    if not callsign and lat and lon:
                        speed_kmh = round((velocity or 0) * 3.6)
                        alt_m = round(altitude or 0)
                        trajectory = calc_past_points(lat, lon, speed_kmh, heading)
                        
                        ufo_events.append({
                            "id": f"UAP-RADAR-{s[0].upper()}",
                            "source": "Radar Tático Airspace",
                            "shape": "Vetor Anômalo Não Identificado",
                            "latitude": round(lat, 4),
                            "longitude": round(lon, 4),
                            "altitude_m": alt_m,
                            "speed_kmh": speed_kmh,
                            "country": country if country else "Internacional / Não Registrado",
                            "trajectory": trajectory,
                            "summary": f"Alvo aéreo sem emissão de transponder civil ADS-B."
                        })
        except Exception as e:
            print(f"Erro OpenSky: {e}")
            
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
                            "shape": "Artefato / Corpo Espacial",
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
        
        for i in range(1, 120):
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
"""

index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OvniVra – Monitor de Objetos Não Identificados</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #050811; color: #00ffaa; font-family: 'Consolas', 'Courier New', monospace; height: 100vh; overflow: hidden; }
        #app { display: flex; height: 100vh; width: 100vw; }
        #map { flex: 3; background: #020408; }
        #sidebar { flex: 1; min-width: 340px; max-width: 440px; background: #09101f; border-left: 2px solid #00ffaa; padding: 20px; overflow-y: auto; }
        h1 { font-size: 20px; color: #00ffaa; border-bottom: 1px solid #00ffaa; padding-bottom: 8px; margin-bottom: 15px; text-shadow: 0 0 8px #00ffaa; }
        .ufo-card { background: #0e1a30; border: 1px solid #00ffaa; border-radius: 4px; padding: 12px; margin-bottom: 12px; font-size: 12px; line-height: 1.6; cursor: pointer; transition: all 0.2s; }
        .ufo-card:hover { background: #132748; border-color: #38bdf8; }
        .ufo-card.warning { border-color: #ff0055; color: #ff6688; }
        .ufo-card.warning:hover { border-color: #ff3377; }
        .ufo-title { font-weight: bold; font-size: 14px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: #00ffaa; color: #000; padding: 2px 6px; font-weight: bold; border-radius: 3px; font-size: 10px; }
        .badge-warn { background: #ff0055; color: #fff; }
        .refresh-btn { width: 100%; padding: 10px; background: #00ffaa; color: #000; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 15px; }
        .refresh-btn:hover { background: #00cc88; }
        .coord-txt { color: #38bdf8; font-weight: bold; }
        .city-txt { color: #facc15; font-weight: bold; }
        .city-start-txt { color: #38bdf8; font-weight: bold; }
    </style>
</head>
<body>
    <div id="app">
        <div id="map"></div>
        <div id="sidebar">
            <h1>🛸 OVNIVRA MONITOR</h1>
            <button class="refresh-btn" onclick="loadUfoData()">VARREDURA RADAR EM TEMPO REAL</button>
            <div id="status-box">Buscando sinais de anomalias...</div>
            <hr style="border-color: #00ffaa; margin: 15px 0;">
            <div id="ufo-list"></div>
        </div>
    </div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const map = L.map('map', { preferCanvas: true }).setView([0, 0], 2);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap'
        }).addTo(map);

        let markers = [];
        let trajectoryGroup = L.featureGroup().addTo(map);

        map.on('click', () => {
            trajectoryGroup.clearLayers();
        });

        async function obterNomeCidade(lat, lon, countryFallback) {
            if (countryFallback === "Espaço Profundo") return "Órbita Terrestre";
            try {
                const resp = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=pt`);
                if (resp.ok) {
                    const d = await resp.json();
                    const cidade = d.city || d.locality || d.principalSubdivision;
                    if (cidade) return cidade;
                }
            } catch(e) {}
            return countryFallback || "Área Oceânica / Não Mapeada";
        }

        async function carregarCidadesVoo(item, prefix) {
            const startPoint = item.trajectory && item.trajectory.length > 0 ? item.trajectory[0] : [item.latitude, item.longitude];
            const currPoint = [item.latitude, item.longitude];

            const [cidadeInicio, cidadeAtual] = await Promise.all([
                obterNomeCidade(startPoint[0], startPoint[1], item.country),
                obterNomeCidade(currPoint[0], currPoint[1], item.country)
            ]);

            const elStart = document.getElementById(`${prefix}-start`);
            if (elStart) elStart.innerText = cidadeInicio;

            const elCurr = document.getElementById(`${prefix}-curr`);
            if (elCurr) elCurr.innerText = cidadeAtual;

            return { cidadeInicio, cidadeAtual };
        }

        async function desenharTrajeto(item, cidades = {}) {
            trajectoryGroup.clearLayers();

            if (item.trajectory && item.trajectory.length > 1) {
                const isNasa = item.source.includes("NASA");
                const color = isNasa ? '#ff0055' : '#00ffaa';

                L.polyline(item.trajectory, {
                    color: '#000000',
                    weight: 7,
                    opacity: 0.8
                }).addTo(trajectoryGroup);

                L.polyline(item.trajectory, {
                    color: color,
                    weight: 4,
                    dashArray: '8, 10',
                    opacity: 1.0
                }).addTo(trajectoryGroup);

                const pontoOrigem = item.trajectory[0];
                const labelOrigem = cidades.cidadeInicio ? `Início: ${cidades.cidadeInicio}` : 'Início da Trajetória';

                L.circleMarker(pontoOrigem, {
                    radius: 6,
                    color: '#ffffff',
                    fillColor: color,
                    fillOpacity: 1
                }).bindTooltip(labelOrigem, { permanent: true, direction: 'top' }).addTo(trajectoryGroup);

                trajectoryGroup.bringToFront();
            }
        }

        async function loadUfoData() {
            const statusBox = document.getElementById('status-box');
            const listContainer = document.getElementById('ufo-list');
            statusBox.innerHTML = "🛰️ Conectando com radares e sensores de espaço...";
            try {
                const response = await fetch('/api/live-ufo');
                const result = await response.json();
                statusBox.innerHTML = `
                    <b>ANOMALIAS RASTREADAS:</b> <span style="color:#facc15; font-size:16px;">${result.total_anomalies_tracked}</span><br>
                    <b>FILTRO AÉREO:</b> Tráfego Civil Descartado.<br>
                    <small style="color:#38bdf8;">Clique em qualquer objeto para ver origem e cidade atual.</small>
                `;
                
                markers.forEach(m => map.removeLayer(m));
                markers = [];
                listContainer.innerHTML = '';

                result.data.forEach((item, idx) => {
                    const isNasa = item.source.includes("NASA");
                    const markerColor = isNasa ? '#ff0055' : '#00ffaa';
                    const keyId = `ufo-${idx}`;

                    if (item.latitude && item.longitude) {
                        const marker = L.circleMarker([item.latitude, item.longitude], {
                            radius: 6,
                            color: markerColor,
                            fillColor: markerColor,
                            fillOpacity: 0.8
                        }).addTo(map);

                        const popupContent = `
                            <b style="color:${markerColor}">${item.id}</b><br>
                            <b>CIDADE INÍCIO:</b> <span class="city-start-txt" id="pop-${keyId}-start">Clique p/ localizar</span><br>
                            <b>CIDADE ATUAL:</b> <span class="city-txt" id="pop-${keyId}-curr">Clique p/ localizar</span><br>
                            <b>PAÍS / REGIÃO:</b> ${item.country}<br>
                            <b>COORDENADAS:</b> ${item.latitude}, ${item.longitude}<br>
                            <b>FORMA/TIPO:</b> ${item.shape}<br>
                            <b>VELOCIDADE:</b> ${item.speed_kmh.toLocaleString()} km/h<br>
                            <b>ALTITUDE:</b> ${item.altitude_m.toLocaleString()} m<br>
                            <b>FONTE:</b> ${item.source}
                        `;

                        marker.bindPopup(popupContent);
                        
                        marker.on('popupopen', async () => {
                            const resCidades = await carregarCidadesVoo(item, `pop-${keyId}`);
                            carregarCidadesVoo(item, `card-${keyId}`);
                            desenharTrajeto(item, resCidades);
                        });

                        markers.push(marker);
                    }

                    const card = document.createElement('div');
                    card.className = `ufo-card ${isNasa ? 'warning' : ''}`;
                    card.innerHTML = `
                        <div class="ufo-title">
                            <span>${item.id}</span>
                            <span class="badge ${isNasa ? 'badge-warn' : ''}">${item.source}</span>
                        </div>
                        <b>CIDADE INÍCIO:</b> <span class="city-start-txt" id="card-${keyId}-start">${item.country}</span><br>
                        <b>CIDADE ATUAL:</b> <span class="city-txt" id="card-${keyId}-curr">${item.country}</span><br>
                        <b>PAÍS / REGIÃO:</b> ${item.country}<br>
                        <b>COORDENADAS:</b> <span class="coord-txt">${item.latitude}, ${item.longitude}</span><br>
                        <b>FORMA:</b> ${item.shape}<br>
                        <b>VELOCIDADE:</b> ${item.speed_kmh.toLocaleString()} km/h<br>
                        <b>ALTITUDE:</b> ${item.altitude_m.toLocaleString()} m<br>
                        <p style="margin-top: 5px; opacity: 0.85;">${item.summary}</p>
                    `;

                    card.onclick = async (e) => {
                        e.stopPropagation();
                        const resCidades = await carregarCidadesVoo(item, `card-${keyId}`);
                        desenharTrajeto(item, resCidades);
                        map.flyTo([item.latitude, item.longitude], Math.max(map.getZoom(), 6), { duration: 1 });
                    };

                    listContainer.appendChild(card);
                });
            } catch (err) {
                statusBox.innerHTML = "❌ Erro ao atualizar radar. Tente novamente.";
                console.error(err);
            }
        }

        loadUfoData();
        setInterval(loadUfoData, 30000);
    </script>
</body>
</html>
"""

os.makedirs("static", exist_ok=True)
with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_py)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ Cidade de início e cidade atual configuradas com sucesso!")
