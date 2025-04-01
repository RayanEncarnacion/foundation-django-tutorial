from datetime import date, datetime, timedelta
from background_task import background

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
    
    print(active_pay_days)
    
    Payment.objects.bulk_create([
        Payment(
            amount=pay_data.project.amount, 
            project=pay_data.project, 
            due_date=get_next_month_date(today)
        ) for pay_data in active_pay_days
    ])
   
    print("Payments scheduled correctly!")
