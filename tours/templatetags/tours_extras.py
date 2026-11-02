from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from tours.context_processors import whatsapp_url

register = template.Library()


@register.simple_tag
def wa_link(message=""):
    return whatsapp_url(message)


@register.filter
def usd(value):
    if value in (None, ""):
        return ""
    return f"${intcomma(int(value))}"
