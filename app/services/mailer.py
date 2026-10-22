import resend
from app.config import settings

def send_morning_alert(edition_date_str: str):
    """Envia alerta simples por e-mail informando que o briefing do dia está pronto."""
    if not settings.RESEND_API_KEY:
        print("RESEND_API_KEY ausente. E-mail simulado com sucesso.")
        return

    resend.api_key = settings.RESEND_API_KEY
    read_url = f"{settings.APP_BASE_URL.rstrip('/')}/"

    params = {
        "from": "BREVE. <onboarding@resend.dev>",
        "to": [settings.NOTIFICATION_EMAIL],
        "subject": f"☀️ BREVE. Seu Resumo Matinal está pronto — {edition_date_str}",
        "html": f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f1115; color: #f3f4f6; padding: 32px 20px; border-radius: 8px; max-width: 480px; margin: 0 auto;">
          <h2 style="font-family: Georgia, serif; font-size: 26px; color: #ffffff; margin-bottom: 8px;">BREVE.</h2>
          <p style="color: #9ca3af; font-size: 15px; line-height: 1.5;">Bom dia, Antônio! O seu briefing do dia ({edition_date_str}) já foi selecionado e compilado com foco em Cultura, Economia, F1, Design e Geral.</p>
          <div style="margin: 28px 0;">
            <a href="{read_url}" style="background-color: #f3f4f6; color: #111827; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; display: inline-block;">Ler resumo de hoje</a>
          </div>
          <p style="color: #6b7280; font-size: 12px; margin-top: 24px;">Leitura estimada: 3 a 5 minutos. Sem algoritmos, direto ao ponto.</p>
        </div>
        """
    }
    try:
        resend.Emails.send(params)
        print("E-mail matinal disparado para:", settings.NOTIFICATION_EMAIL)
    except Exception as e:
        print(f"Erro ao disparar e-mail via Resend: {e}")
