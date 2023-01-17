#!/usr/bin/env python3

import django.template
from django.conf import settings

settings.configure(
    DEBUG=True,
    L10N=True,
    LANGUAGE_CODE = 'de-de',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
            ],
        },
    }],
    INSTALLED_APPS = [],
)
django.setup()

ctx = django.template.Context()
ctx.push(a=None, b=12.34)
t = django.template.Template(
    """
    {% load l10n %}
    (1) Localized by default: a={{a}}, b={{b}}, firstof={% firstof a b %}
    (2) Block localize off: {% localize off %}a={{a}}, b={{b}}, firstof={% firstof a b %}{% endlocalize %}
    (3) Filter unlocalize: a={{a|unlocalize}}, b={{b|unlocalize}}, firstof={% firstof a|unlocalize b|unlocalize %}
    """
)
print(t.render(ctx))

# Actual (note the last value in last line):
# (1) Localized by default: a=None, b=12,34, firstof=12,34
# (2) Block localize off: a=None, b=12.34, firstof=12.34
# (3) Filter unlocalize: a=None, b=12.34, firstof=None

# Expected, because why should the position of unlocalization matter?
# (1) Localized by default: a=None, b=12,34, firstof=12,34
# (2) Block localize off: a=None, b=12.34, firstof=12.34
# (3) Filter unlocalize: a=None, b=12.34, firstof=12.34
