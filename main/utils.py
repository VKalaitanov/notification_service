import requests
from django.conf import settings
from django.core.mail import send_mail


def send_email(recipient, message):
    if not recipient:
        raise ValueError("No email provided")

    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER

    send_mail(
        subject="Notification",
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
        fail_silently=False,
    )


def send_sms(phone, message):
    if not phone:
        raise ValueError("No phone number provided")

    payload = {
        "login": settings.SMS_AGENT_LOGIN,
        "pass": settings.SMS_AGENT_PASS,
        "sender": settings.SMS_AGENT_SENDER.strip(),
        "text": message,
        "payload": [{"phone": phone}]
    }

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    response = requests.post(settings.SMS_AGENT_API_URL, json=payload, headers=headers)
    try:
        response.raise_for_status()
        return response.json()[0]
    except Exception as e:
        return {"error": str(e), "response": response.text}


def send_telegram(chat_id, message):
    if not chat_id:
        raise ValueError("No Telegram ID provided")

    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    if response.status_code != 200:
        raise Exception(f"Telegram failed: {response.text}")
