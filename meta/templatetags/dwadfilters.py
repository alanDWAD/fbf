from django import template
from django.template.defaultfilters import stringfilter, truncatewords_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def headlinewrap(headline):
    '''Template filter that tries to insert intelligent line-breaks into a
    string. Used to wrap headlines more sensibly than the default wrapping.'''
    if ' - ' in headline:
        return mark_safe(headline.replace(' - ', '<span class="visible-sm-inline"> - </span><br class="hidden-sm"/>', 1))
    elif ': ' in headline:
        return mark_safe(headline.replace(': ', ': <br class="hidden-sm"/>', 1))
    elif headline.count(', ') == 1:
        return mark_safe(headline.replace(', ', ', <br class="hidden-sm"/>', 1))
    else:
        # If we can't find a suitable place to wrap, just defer to the default.
        return mark_safe(headline)


@register.filter(is_safe=True)
@stringfilter
def firstpara(article):
    '''Truncate an article by excluding everything after the first paragraph.'''
    try:
        index = article.index('</p>')
        return article[:index + 4]
    except ValueError:
        # Fall-back to default truncatewords_html tag if we can't identify a
        # paragraph.
        return truncatewords_html(article, 80)


@register.filter(is_safe=True)
@stringfilter
def formaturl(url):
    '''Trim a URL for display (removes http(s) prefix).'''
    return url.replace('http://', '').replace('https://', '').replace('twitter.com/', '@')
