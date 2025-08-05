from django.utils import timezone

from .models import Notification
from .utils import send_email, send_sms, send_telegram
from celery import shared_task


@shared_task
def send_notification_task(notification_id):
    notification = Notification.objects.select_related("user").get(id=notification_id)
    user = notification.user
    message = notification.message
    channels = user.preferred_channels or ["email", "sms", "telegram"]
    attempt_logs = []

    for channel in channels:
        try:
            if channel == "email":
                send_email(user.email, message)
            elif channel == "sms":
                send_sms(user.phone_number, message)
            elif channel == "telegram":
                send_telegram(user.telegram_id, message)
            notification.status = "sent"
            notification.successful_channel = channel
            notification.sent_at = timezone.now()
            break
        except Exception as e:
            attempt_logs.append({"channel": channel, "error": str(e)})
            continue
    else:
        notification.status = "failed"

    notification.attempt_logs = attempt_logs
    notification.save()

