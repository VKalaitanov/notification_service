from django import forms


CHANNEL_CHOICES = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('telegram', 'Telegram'),
]

class NotificationForm(forms.Form):
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    telegram_id = forms.CharField(max_length=50, required=False)
    preferred_channels = forms.MultipleChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    message = forms.CharField(widget=forms.Textarea)