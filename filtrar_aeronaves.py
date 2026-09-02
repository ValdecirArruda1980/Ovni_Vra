with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Substitui a lógica que puxava o OpenSky Network (aviões civis) para ignorá-lo completamente
old_opensky = """        try:
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
            print(f"Erro OpenSky: {e}")"""

new_opensky = """        # Tráfego civil (aviões e helicópteros) totalmente descartado a pedido do operador.
        print("ℹ️ Tráfego aéreo comercial/civil descartado com sucesso.")"""

content = content.replace(old_opensky, new_opensky)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Código atualizado para descartar aviões e helicópteros!")
