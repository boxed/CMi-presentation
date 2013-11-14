from django.shortcuts import render
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import os


def hilight_str(s):
    return highlight(s, PythonLexer(), HtmlFormatter())


def hilight_file(filename):
    if filename.endswith('pyc'):
        filename = filename[:-1]
    return hilight_str(open(filename, 'r').read())


def index(request, page='0'):
    page = int(page)
    slides = [
        ('Background', [
            'Unhappy user of XBMC for several years',
            'File classification',
            'Skins',
            'Incorrect handling of some shows',
        ]),
        ('XBMC Stats', """
C/C++: 2M
Shell: 328k
m4: 111k
XML: 102k
HTML: 64k
Assembly: 41k
Make: 13k
Pascal: 10k
Python: 9k
Objective-C: 7k
Other: 27k
Total: 2.7M
        """),
        ('Basic decisions', """
GUI should be HTML/Javascript/CSS as far as possible
I should use whatever video playing library I could get to work. I started out by just using the QuickTime APIs
The design should be Metro-inspired, party because I like it, but partly because it's pretty easy to look ok
Should support multiple input methods: mouse, keyboard and IR remote
Django as backend
"""),
        ('Architecture', [
            ('Spawn Django development server', "I'll talk about the advantages of this later"),
            'Grab stdout and use it to figure out when server has started',
            ('When server is started, point WebKit view to it:', '', hilight_str("""
NSURLRequest* request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://127.0.0.1:8000/"]];
[[self.webView mainFrame] loadRequest:request];
            """))
        ]),
        ('Interaction', [
            ('IR Remote', '(Apple remote)'),
            'Keyboard',
            'Mouse',
            'Video Player Controls',
            'Django -> Objective-C communication',
            'Objective-C -> Django communication',
        ]),
        ('CMi Stats', """
Objective-C: 1.6k
Python: 1k
JavaScript: 1k
HTML: 300
CSS: 300
Total: ~3k
        """),
        ('Database', """
SQLite
Stores db in ~/Library/Application Support/CMi/cmi.db
Ships with a pre-synced copy in the app that is automatically copied over on startup
        """),
        ('Plugins', [
            'Scans ~/Library/Application Support/CMi/plugins on startup',
            'Add folders to INSTALLED_APPLICATIONS',
            'Modules are loaded like a normal django app from this point',
            'Syncdb is run',
            'Upgrades run. Introspects <plugin>.upgrade module for upgrade_<number>() functions',
            'django.con.settings.plugins == the list of plugins available',
            ('Introspects <plugin>.api module for plugin functions:', '',
                '<ul><li>tiles()</li><li>urls()</li><li>should_refresh()</li></ul>'),
        ]),
        ('Live development', [
            'PyCharm ssh deploy directly into remote .app bundle',
            'Runserver in auto reload mode',
            'settings.CODE_CHANGED = 1',
            ('AJAX poll:', '', hilight_str("""
def changed_code(request):
    from django.conf import settings
    result = settings.CODE_CHANGED
    settings.CODE_CHANGED = 0
    return HttpResponse(str(result))""".strip()))
        ]),
        ('Misc', """
OSX Location APIs enable location aware weather widget.
All animations are done with CSS transformations.
Retina display support with just a different CSS.
BeautifulSoup
theTVDB API
IMDB API
        """),

        ('This presentation is a CMi plugin!', [
            ('', '', hilight_file(os.path.join(__file__.rsplit('/', 1)[0], 'api.py'))),
        ]),
        ('CMi: Getting Involved', [
            'github.com/boxed/cmi',
            'MIT License',
            'boxed@killingar.net',
        ]),
    ]

    title, points = slides[page]

    points = points.strip().split('\n') if type(points) == str else points

    def prepare_point(point):
        if type(point) == tuple:
            if len(point) > 2:
                return {'title': point[0], 'subtitle': point[1], 'image': point[2]}
            else:
                return {'title': point[0], 'subtitle': point[1]}
        else:
            return {'title': point}

    slide = {
        'title': title,
        'points': [prepare_point(x) for x in points],
        'next': '/presentation/%s/' % (page + 1),
    }

    return render(request, 'presentation/points.html', slide)
