from webpush import send_user_notification
import json

def disparar_alerta_agendamento(user, agendamento):
    payload = {
        "head": "🚨 Novo Agendamento na Oficina!",
        "body": f"Cliente: {agendamento.cliente.nome} | Veículo: {agendamento.veiculo.modelo}",
        "icon": "/static/img/icon-ncs.png",  # Opcional: ícone da notificação
        "url": f"/agendamentos/" # Para onde o usuário vai ao clicar na notificação
    }
    
    try:
        send_user_notification(user=user, payload=json.dumps(payload), ttl=1000)
    except Exception as e:
        print(f"Erro ao enviar push notification: {e}")