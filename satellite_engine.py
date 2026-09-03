import math
from skyfield.api import load, EarthSatellite, Topos

def normalizar_longitude(lng: float) -> float:
    """Normaliza qualquer longitude para o intervalo padrão entre -180 e 180 graus."""
    return (lng + 180) % 360 - 180

def calcular_posicao_objeto(satelite: EarthSatellite, ts, t, observer_topos: Topos):
    geocentric = satelite.at(t)
    subpoint = geocentric.subpoint()
    lat = subpoint.latitude.degrees
    lng = normalizar_longitude(subpoint.longitude.degrees)
    altitude_km = subpoint.elevation.km
    difference = satelite - observer_topos
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    return {
        "latitude": round(lat, 4),
        "longitude": round(lng, 4),
        "altitude_km": round(altitude_km, 2),
        "elevacao_graus": round(alt.degrees, 2),
        "azimute_graus": round(az.degrees, 2),
        "distancia_km": round(distance.km, 2)
    }

def calcular_satelites_visiveis(observer_lat: float, observer_lng: float):
    ts = load.timescale()
    t = ts.now()
    observer_topos = Topos(latitude_degrees=observer_lat, longitude_degrees=observer_lng)
    
    stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
    satellites = load.tle_file(stations_url)
    
    resultados = []
    for sat in satellites[:20]:
        pos = calcular_posicao_objeto(sat, ts, t, observer_topos)
        resultados.append({
            "nome": sat.name,
            **pos
        })
    return resultados
