from django import template

register = template.Library()


@register.filter
def format_decimal(value):
    """
    Formats an integer value to show the last two digits as decimal places.
    Example: 2127 -> 21.27
    """
    try:
        value = int(value)
        return f"{value // 100}.{value % 100:02d}"
    except (ValueError, TypeError):
        return value
