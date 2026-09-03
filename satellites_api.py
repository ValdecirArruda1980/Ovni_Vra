import json
from fastapi import APIRouter, Query
from cache_manager import obter_tles_do_cache
from satellite_engine import calcular_satelites_visiveis

# Cria um router isolado para não interferir nas rotas existentes do main.py
router = APIRouter(prefix="/satelites", tags=["Radar de Satélites"])

@router.get("/radar")
async def obter_radar_satelites(
    lat: float = Query(..., description="Latitude do usuário"),
    lng: float = Query(..., description="Longitude do usuário")
):
    """
    Endpoint completo que calcula em tempo real os satélites visíveis 
    acima do horizonte para as coordenadas informadas, utilizando cache no Redis.
    """
    # Arredonda coordenadas (~1.1 km de precisão) para agrupamento inteligente em cache
    lat_geo = round(lat, 2)
    lng_geo = round(lng, 2)
    
    # Importa o cliente Redis configurado no cache_manager
    from cache_manager import redis_client
    cache_key = f"ovnivra:radar:{lat_geo}:{lng_geo}"
    
    # 1. Verifica se já existe um cálculo recente para essa região no Redis (TTL de 30 segundos)
    radar_cached = redis_client.get(cache_key)
    if radar_cached:
        resultado = json.loads(radar_cached)
        resultado["fonte"] = "cache_redis"
        return resultado
        
    # 2. Se não estiver em cache, recupera os TLEs e executa o cálculo orbital
    tle_data = obter_tles_do_cache()
    if not tle_data:
        return {"erro": "Não foi possível carregar os dados orbitais no momento."}
        
    satelites_visiveis = calcular_satelites_visiveis(tle_data, lat, lng)
    
    resposta = {
        "total_visiveis": len(satelites_visiveis),
        "coordenadas_regiao": {"latitude": lat_geo, "longitude": lng_geo},
        "satelites": satelites_visiveis,
        "fonte": "calculado_em_tempo_real"
    }
    
    # 3. Armazena o resultado no Redis por 30 segundos para otimizar performance
    redis_client.set(cache_key, json.dumps(resposta), ex=30)
    return resposta
