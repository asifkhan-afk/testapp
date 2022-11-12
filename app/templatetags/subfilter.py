from django import template

register = template.Library()

@register.filter(name='substract')
def subtract(value,args):
     return value-args