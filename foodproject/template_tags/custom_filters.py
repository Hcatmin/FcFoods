from django import template

register = template.Library()

@register.filter
def split_timesince(value):
    time_parts = value.split(", ")
    return time_parts[0]
