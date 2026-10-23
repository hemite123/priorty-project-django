from django import template

register = template.Library()
arrayalre = []

@register.filter
def plusadd(value,autoescape=True):
    return value + 1

@register.filter
def appendarray(value):
    arrayalre.append(value)
    return arrayalre
