from django import template
from django.template.defaultfilters import date
import jdatetime

register = template.Library()

@register.filter(name='jalali_date')
def jalali_date(value, arg=None):
    if value is None:
        return ''
    
    try:
        j_date = jdatetime.datetime.fromgregorian(datetime=value)
        if arg is None:
            return j_date.strftime('%d %B %Y')
        return date(j_date, arg)
    except:
        return ''
