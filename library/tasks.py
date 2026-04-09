from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from library.models import Loan


@shared_task
def send_upcoming_due_reminders():
    """Отправляет уведомления о приближающемся сроке сдачи (за 2 дня)"""
    today = timezone.now().date()
    reminder_date = today + timedelta(days=2)

    loans = Loan.objects.filter(
        return_date__isnull=True,
        due_date=reminder_date,
        notified_about_due=False
    ).select_related('book', 'borrower')

    for loan in loans:
        send_reminder_email.delay(
            email=loan.borrower.email,
            subject=f"Напоминание: срок сдачи книги '{loan.book.title}'",
            message=f"""Уважаемый(ая) {loan.borrower.email},
            Напоминаем вам, что срок сдачи книги "{loan.book.title}"
            истекает через 2 дня ({loan.due_date.strftime('%d.%m.%Y')}).
            Пожалуйста, не забудьте вернуть книгу в указанный срок.
            С уважением,
            Библиотечная система"""
        )
        loan.notified_about_due = True
        loan.save()


@shared_task
def send_overdue_notifications():
    """Отправляет уведомления о просроченных книгах"""
    today = timezone.now().date()

    loans = Loan.objects.filter(
        return_date__isnull=True,
        due_date__lt=today,
        notified_about_overdue=False
    ).select_related('book', 'borrower')

    for loan in loans:
        days_overdue = (today - loan.due_date).days
        send_reminder_email.delay(
            email=loan.borrower.email,
            subject=f"СРОЧНО: книга '{loan.book.title}' просрочена на {days_overdue} дней",
            message=f"""Уважаемый(ая) {loan.borrower.email},
            Вы просрочили возврат книги "{loan.book.title}" на {days_overdue} дней.
            Первоначальный срок возврата: {loan.due_date.strftime('%d.%m.%Y')}.
            Пожалуйста, немедленно верните книгу в библиотеку.
            Примечание: дальнейшая задержка может привести к ограничению вашего доступа.
            С уважением,
            Библиотечная система"""
        )
        loan.notified_about_overdue = True
        loan.save()


@shared_task
def send_reminder_email(email, subject, message):
    """Отдельная задача для отправки email"""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )
