import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DADOS_PADRAO_USUARIO = {
    'usuario_id': 'valdecir_piracicaba',
    'telefone': '+5519993718849',
    'email': 'valdecirrogerio@gmail.com'
}

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_REMETENTE = 'valdecirrogerio@gmail.com'
SENHA_EMAIL = 'fjwhraokjauetght'

def calcular_distancia_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def enviar_sms(numero_destino: str, texto: str):
    print(f'[SMS SIMULADO] Enviando para {numero_destino}: {texto}')

def enviar_whatsapp(numero_destino: str, texto: str):
    print(f'[WHATSAPP SIMULADO] Enviando para whatsapp:{numero_destino}: {texto}')

def enviar_email(destino: str, assunto: str, corpo: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destino
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_EMAIL)
        server.sendmail(EMAIL_REMETENTE, destino, msg.as_string())
        server.quit()
        print(f'[EMAIL REAL ENVIADO] E-mail enviado com sucesso para {destino}!')
    except Exception as e:
        print(f'[ERRO SMTP] Falha ao enviar e-mail real: {e}')

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
    u_email = getattr(usuario, 'email', None) or (usuario.get('email', DADOS_PADRAO_USUARIO['email']) if isinstance(usuario, dict) else DADOS_PADRAO_USUARIO['email'])
    distancia = calcular_distancia_km(u_lat, u_lng, ovni_lat, ovni_lng)
    RAIO_ALERTA_KM = 50.0
    if distancia <= RAIO_ALERTA_KM:
        mensagem = f'ALERTA OVNIVRA! Objeto detectado a {distancia:.1f}km de Piracicaba!'
        enviar_sms(u_tel, mensagem)
        enviar_whatsapp(u_tel, mensagem)
        enviar_email(u_email, 'Alerta de OVNI Proximo - OvniVra', mensagem)
        return {'status': 'alerta_disparado', 'distancia_km': round(distancia, 2)}
    return {'status': 'fora_do_raio', 'distancia_km': round(distancia, 2)}
