# import pytest
# from apps.accounts.tasks import send_activation_email_task
# from apps.notifications.tasks import send_custom_notification
# from apps.notifications.models import Notification


# # 📧 تست ارسال ایمیل فعال‌سازی
# @pytest.mark.django_db
# def test_send_activation_email_task_runs(customer_user):
#     # فقط بررسی می‌کنیم که task بدون خطا اجرا می‌شه
#     send_activation_email_task.delay(customer_user.id, customer_user.email)
#     # اگر ایمیل mock شده باشه، می‌تونی بررسی کنی که ارسال شده


# # 🔔 تست ارسال نوتیفیکیشن
# @pytest.mark.django_db
# def test_send_custom_notification_task_creates_notification(customer_user):
#     send_custom_notification.delay(
#         customer_user.id,
#         message="Welcome to the platform!",
#         priority="info",
#         redirect_url="/dashboard/"
#     )

#     notif = Notification.objects.filter(user=customer_user).first()
#     assert notif is not None
#     assert "welcome" in notif.message.lower()
#     assert notif.priority == "info"
#     assert notif.redirect_url == "/dashboard/"
