import os
import httpx

async def enviar_alerta_whatsapp_api(telefone: str, mensagem: str):
    """
    Dispara mensagens automáticas via WhatsApp Cloud API oficial da Meta (Gratuita para testes).
    As chaves são puxadas das variáveis de ambiente do Render ou do sistema local.
    """
    # Credenciais obtidas gratuitamente no painel Meta for Developers
    PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "SEU_PHONE_ID_AQUI")
    TOKEN = os.getenv("WHATSAPP_TOKEN", "SEU_TOKEN_AQUI")
    
    # URL oficial do endpoint da Meta (versão v18.0 ou superior)
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Formato de payload exigido pela Meta Cloud API
    # O telefone deve ir apenas com números (ex: 5519993718849)
    telefone_limpo = telefone.replace("+", "").replace(" ", "").replace("-", "")
    
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone_limpo,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201]:
                print("✅ Mensagem de WhatsApp enviada com sucesso via Meta Cloud API!")
                return True
            else:
                print(f"❌ Erro na Meta Cloud API: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Erro de conexão com a Meta Cloud API: {e}")
        return False
