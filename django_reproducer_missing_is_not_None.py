#!/usr/bin/env python3

import django.template
from django.conf import settings

settings.configure(
    DEBUG=True,
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
ctx.push(var_exists="you", var_none=None)
t = django.template.Template(
    """
    varname: »literal« »is None« »default_if_none«
    var_exists: »{{var_exists}}« »{%if var_exists is None%}True{%else%}False{%endif%}« »{{var_exists|default_if_none:"NONE"}}«
    var_none: »{{var_none}}« »{%if var_none is None%}True{%else%}False{%endif%}« »{{var_none|default_if_none:"NONE"}}«
    var_miss: »{{var_miss}}« »{%if var_miss is None%}True{%else%}False{%endif%}« »{{var_miss|default_if_none:"NONE"}}«
    """
)
print(t.render(ctx))

# Actual:
# varname: »literal« »is None« »default_if_none«
# var_exists: »you« »False« »you«
# var_none: »None« »True« »NONE«
# var_miss: »« »True« »«

# Expected, because why should default_if_none behave differently than {%if foo is None%}?
# varname: »literal« »is None« »default_if_none«
# var_exists: »you« »False« »you«
# var_none: »None« »True« »NONE«
# var_miss: »« »True« »NONE«
