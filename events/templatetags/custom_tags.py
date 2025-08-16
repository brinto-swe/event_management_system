from django import template

register = template.Library()

@register.filter
def has_group(user, group_names):
    """
    Check if user is in any of the groups.
    Usage: {% if user|has_group:"Admin,Organizer" %}
    """
    groups = group_names.split(',')
    return user.groups.filter(name__in=groups).exists()
