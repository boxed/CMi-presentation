from django.template.loader import render_to_string
from django.conf.urls import patterns, url


def tiles():
    return [
        (0, render_to_string('tile.html', {
            'url': '/presentation/',
            'image': '/site-media/tv.svg',
            'title': 'Presentation',
            'content': 'Replacing XBMC',
        })),
    ]


def urls():
    return patterns('presentation.views',
        (r'^presentation/$', 'index'),
        (r'^presentation/(?P<page>\d+)?/$', 'index'),
        )+patterns('',
        url(
            r'^presentation/static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': __file__.rsplit('/', 1)[0]+'/static/'}),
    )