from django import template

register = template.Library()


@register.filter(name='to_hex')
def to_hex(value):
    return format(value, '02x')
