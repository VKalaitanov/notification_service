from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import NotificationForm
from .tasks import send_notification_task
from .models import User, Notification


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import NotificationForm
from .tasks import send_notification_task
from .models import User, Notification


class NotificationView(View):
    def get(self, request):
        form = NotificationForm()
        return render(request, "main/notification_form.html", {"form": form})

    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            user, _ = User.objects.get_or_create(
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
                telegram_id=form.cleaned_data["telegram_id"],
                defaults={"preferred_channels": form.cleaned_data["preferred_channels"]}
            )
            user.preferred_channels = form.cleaned_data["preferred_channels"]
            user.save()

            notification = Notification.objects.create(
                user=user,
                message=form.cleaned_data["message"]
            )
            send_notification_task.delay(notification.id)
            return redirect("main:notify_success", notification_id=notification.id)
        return render(request, "main/notification_form.html", {"form": form})


class NotificationSuccessView(View):
    def get(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        return render(request, "main/notification_success.html", {"notification": notification})



class NotificationStatusView(View):
    def get(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        return render(request, "main/notification_status.html", {"notification": notification})
