from dateutil.relativedelta import relativedelta
from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def deactivate_user():
    """Деактивирует пользователей, которые не входили в систему более 30 дней."""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    month_ago = today - relativedelta(months=1)
    users = User.objects.filter(last_login__lte=month_ago, is_active=True)
    users.update(is_active=False)
