from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(round(number))


@register.filter(name='times_minus')
def times_minus(number):
    rating = 5 - round(number)
    return range(rating)
