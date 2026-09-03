import os
import httpx

async def enviar_alerta_whatsapp_api(telefone: str, mensagem: str):
    """
    Dispara mensagens automáticas via API HTTP de Gateway (compatível com Render).
    As chaves são puxadas de forma segura pelas variáveis de ambiente do servidor.
    """
    # URL do Gateway e Token configurados via variáveis de ambiente
    GATEWAY_URL = os.getenv("WHATSAPP_GATEWAY_URL", "https://api.exemplo-gateway.com/send")
    TOKEN = os.getenv("WHATSAPP_GATEWAY_TOKEN", "SEU_TOKEN_DO_GATEWAY")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "phone": telefone,
        "message": mensagem
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(GATEWAY_URL, json=payload, headers=headers)
            if response.status_code in [200, 201]:
                print("✅ Alerta de WhatsApp disparado com sucesso via Gateway HTTP!")
                return True
            else:
                print(f"❌ Erro no Gateway de WhatsApp: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Erro de conexão com o Gateway de WhatsApp: {e}")
        return False
