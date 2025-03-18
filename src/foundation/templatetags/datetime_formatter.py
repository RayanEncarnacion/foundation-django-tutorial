from django import template

register = template.Library()  # Create a Library instance

@register.filter  # Register the function as a template filter
def format_datetime(value):
    """
    Custom template filter to format a datetime object as "mm/dd/yyyy hh:mm AM/PM".
    """
    if value:
        return value.strftime("%m/%d/%Y %I:%M %p")
    return "" 