import math
import os
import requests

DADOS_PADRAO_USUARIO = {
    'usuario_id': 'valdecir_piracicaba',
    'telefone': '5519993718849',
    'email': 'valdecirrogerio@gmail.com'
}

def calcular_distancia_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def enviar_whatsapp_real(numero_destino: str, texto: str):
    """Envia mensagem real via Meta Cloud API usando requisição HTTP"""
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID", "1372681535918103")
    
    if not token:
        print("[ERRO WHATSAPP] Variável WHATSAPP_TOKEN não encontrada no ambiente do Render!")
        return
        
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": texto}
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"[WHATSAPP REAL ENVIADO] Mensagem entregue para {numero_destino}!")
        else:
            print(f"[ERRO META API] Falha status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERRO WHATSAPP] Exceção ao conectar com a Meta: {e}")

def verificar_e_notificar_proximidade(ovni_lat: float, ovni_lng: float, usuario=None):
    if usuario is None:
        class UserMock:
            def __init__(self):
                self.lat = -22.7253
                self.lng = -47.6492
                self.telefone = DADOS_PADRAO_USUARIO['telefone']
                self.email = DADOS_PADRAO_USUARIO['email']
        usuario = UserMock()
    
    u_lat = getattr(usuario, 'lat', None) or (usuario.get('lat', -22.7253) if isinstance(usuario, dict) else -22.7253)
    u_lng = getattr(usuario, 'lng', None) or (usuario.get('lng', -47.6492) if isinstance(usuario, dict) else -47.6492)
    u_tel = getattr(usuario, 'telefone', None) or (usuario.get('telefone', DADOS_PADRAO_USUARIO['telefone']) if isinstance(usuario, dict) else DADOS_PADRAO_USUARIO['telefone'])
    
    distancia = calcular_distancia_km(u_lat, u_lng, ovni_lat, ovni_lng)
    RAIO_ALERTA_KM = 50.0
    
    if distancia <= RAIO_ALERTA_KM:
        mensagem = f'ALERTA OVNIVRA! Objeto detectado a {distancia:.1f}km de Piracicaba!'
        
        # Disparo real do WhatsApp via HTTP
        enviar_whatsapp_real(u_tel, mensagem)
        
        return {'status': 'alerta_disparado', 'distancia_km': round(distancia, 2)}
        
    return {'status': 'fora_do_raio', 'distancia_km': round(distancia, 2)}
