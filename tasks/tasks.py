from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task


@shared_task
def send_task_notification_email(to_email, subject, message):
    """
    Sends a single email notification.
    """
    send_mail(
        subject,
        message,
        None,  
        [to_email],
        fail_silently=False,
    )


@shared_task
def send_daily_overdue_summary():
    """
    Sends a daily summary email of overdue tasks to each user.
    """
    today = timezone.now().date()
    overdue_tasks = Task.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'in_progress']
    )

 
    users = set(overdue_tasks.values_list('assigned_to__email', flat=True))

    for email in users:
        if not email:
            continue

        user_tasks = overdue_tasks.filter(assigned_to__email=email)
        task_list = "\n".join([f"- {t.title} (Due {t.due_date})" for t in user_tasks])

        send_task_notification_email.delay(
            email,
            "Overdue Task Summary",
            f"These tasks are overdue:\n{task_list}"
        )
