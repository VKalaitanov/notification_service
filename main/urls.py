from django.urls import path

from .views import NotificationView, NotificationSuccessView, NotificationStatusView

app_name = 'main'

urlpatterns = [
    path("", NotificationView.as_view(), name="notify"),
    path("success/<int:notification_id>/", NotificationSuccessView.as_view(), name="notify_success"),
    # path("status/<int:notification_id>/", NotificationStatusView.as_view(), name="notify_status"),
]