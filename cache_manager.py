import redis
import json
import requests

# Conexão com a instância local do Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# URL oficial do catálogo completo de satélites ativos da CelesTrak
CELESTRAK_ALL_ACTIVE = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
REDIS_KEY_TLE = "ovnivra:tles_active"

def atualizar_cache_tle():
    """Baixa os TLEs da CelesTrak e atualiza o Redis (Executado periodicamente)"""
    try:
        response = requests.get(CELESTRAK_ALL_ACTIVE, timeout=15)
        if response.status_code == 200:
            linhas = response.text.strip().split('\n')
            satelites = []
            
            for i in range(0, len(linhas) - 2, 3):
                nome_real = linhas[i].strip()
                l1 = linhas[i+1].strip()
                l2 = linhas[i+2].strip()
                norad_id = l1[2:7].strip()
                
                satelites.append({
                    "norad_id": norad_id,
                    "nome": nome_real,
                    "line1": l1,
                    "line2": l2
                })
            
            # Salva no Redis expirando em 24 horas (86400 segundos)
            redis_client.set(REDIS_KEY_TLE, json.dumps(satelites), ex=86400)
            print("✅ [Redis] TLEs de satélites atualizados com sucesso!")
            return satelites
    except Exception as e:
        print(f"❌ Erro ao atualizar TLEs no Redis: {e}")
        return None

def obter_tles_do_cache():
    """Recupera a lista de TLEs do Redis ou busca imediatamente se estiver vazio"""
    dados = redis_client.get(REDIS_KEY_TLE)
    if dados:
        return json.loads(dados)
    return atualizar_cache_tle()
