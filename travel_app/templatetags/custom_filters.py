from django import template

register = template.Library()

@register.filter
def model_name(obj):
    """Returns the model name of an object in lowercase."""
    return obj._meta.model_name

@register.filter
def model_name(obj):
    """Returns the model name of an object in lowercase."""
    return obj._meta.model_name.lower() 