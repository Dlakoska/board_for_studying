from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from courses.models import Course, Subscription


@shared_task
def send_info(course_id: int) -> None:
    """Отправляет сообщение пользователю об обновлении материалов курса"""

    course = Course.objects.get(id=course_id)
    course_subscriptions = Subscription.objects.filter(course=course)
    emails_list = course_subscriptions.values_list('user__email', flat=True)
    message = f'Изменен курс {course.name}'
    send_mail(subject=f'Курс {course_id} обновлен',
              message=message,
              from_email=EMAIL_HOST_USER,
              recipient_list=emails_list)
