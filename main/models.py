from django.db import models

class User(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    preferred_channels = models.JSONField(default=list)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, default="pending")  # pending, sent, failed
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    successful_channel = models.CharField(max_length=20, null=True, blank=True)
    attempt_logs = models.JSONField(default=list)