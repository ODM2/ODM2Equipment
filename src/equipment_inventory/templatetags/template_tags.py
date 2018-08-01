from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='http_to_https')
@stringfilter
def http_to_https(url):

    url = url.replace('http://', 'https://')

    return url
