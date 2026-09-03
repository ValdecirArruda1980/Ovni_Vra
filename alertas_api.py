from fastapi import APIRouter
from pydantic import BaseModel
from alertas_engine import verificar_e_notificar_proximidade

router = APIRouter(prefix='/alertas', tags=['Alertas e Proximidade'])

class UsuarioLocalizacao(BaseModel):
    usuario_id: str
    lat: float
    lng: float
    telefone: str = 'indefinido'
    email: str = 'indefinido'

@router.post('/localizacao')
async def receber_localizacao_usuario(dados: UsuarioLocalizacao, ovni_lat: float = -22.7, ovni_lng: float = -47.6):
    resultado = verificar_e_notificar_proximidade(ovni_lat, ovni_lng, dados)
    return {
        'usuario_id': dados.usuario_id,
        'coordenadas_recebidas': {'lat': dados.lat, 'lng': dados.lng},
        'analise_proximidade': resultado
    }
