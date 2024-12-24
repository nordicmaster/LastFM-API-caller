from django import template

register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")


@register.simple_tag
def number_pp(f_counter, page_number):
    return str(f_counter + page_number - 1).zfill(3)
