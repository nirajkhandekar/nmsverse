from flask import request, url_for
import string
import random
import logging
import time
import re

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def random_number(a=0,b=9):
    return random.randint(a,b)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def pretty_date(date):
    return date.strftime(FORMAT)

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('utf8')
        if word:
            result.append(word)
    return unicode(delim.join(result))


class StatusCode:

    STATUSOK        = 201
    STATUSERROR     = 404
