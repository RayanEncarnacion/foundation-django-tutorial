from datetime import date

def get_next_month_date(day: int):
    now = date.today()
    next_month = 1 if now.month == 12 else now.month + 1
    
    return date(year=now.year, month=next_month, day=day)