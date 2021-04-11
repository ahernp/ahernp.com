from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=settings.MARKDOWN_EXTENSIONS)
