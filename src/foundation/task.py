from datetime import date, datetime
from background_task import background
from django.conf import settings
from django.core.mail import send_mail

from foundation.models import PayDay, Payment
from foundation.utils import get_next_month_date

today = date.today()
tomorrow_at_6_am = datetime(year=today.year, month=today.month, day=today.day + 1, hour=6, minute=0, second=0)

@background(schedule=tomorrow_at_6_am) 
def schedule_payments():
    today = date.today().day
    active_pay_days = (PayDay.objects.filter(active=True, 
                                             day=today, 
                                             deleted=False)
                                     .select_related("project"))
    
    Payment.objects.bulk_create([
        Payment(
            amount=pay_data.project.amount, 
            project=pay_data.project, 
            due_date=get_next_month_date(today)
        ) for pay_data in active_pay_days
    ])
    
    send_mail(
        "Payments scheduling",
        "Payments where scheduled correctly!",
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_USER_EMAIL],
        fail_silently=False,
    )

@background(schedule=60) 
def notify_due_payments():
    today = date.today()
    overdue_payments = (Payment.objects.filter(payed=False, due_date__lt=today)
                                       .select_related("project__client"))
    payments_info = ""
    
    for payment in overdue_payments:   
        payments_info += f'{payment.project.client.name} - {payment.project.name}: ${payment.amount} due on date: {payment.due_date.strftime("%d/%m/%Y")} \n'
    
    send_mail(
        "Overdue payments",
        payments_info,
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_USER_EMAIL],
        fail_silently=False,
    )