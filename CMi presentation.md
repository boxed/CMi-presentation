CMi
===

Hello, name is Anders Hovmöller and I work here at TriOptima. I'm going to talk about CMi, a media center app I wrote.


Background
==========

I tried running XBMC for a long time but was very unhappy with it for many reasons. The worst being:
- problems classifying files, I wrote a lot of python to move files around to make it understand
- really bad skin system
- even when it works as intended it still can't handle series like Doctor Who

So I started looking into fixing it. After all, it's a C++ project and I was a full time C++ coder at the time. Quickly realized that wasn't an option... lines of code:

* C/C++: 2M
* Shell: 328k
* m4: 111k
* XML: 102k
* HTML: 64k
* Assembly: 41k
* Make: 13k
* Pascal: 10k
* Python: 9k
* Objective-C: 7k
* Other: 27k
* Total: 2.7M

Excluding comments and blank lines!

Screw that!

So I decided I should just write my own.


Basic decisions
===============

- GUI should be HTML/Javascript/CSS as far as possible
- I should use whatever video playing library I could get to work. I started out by just using the QuickTime APIs
- The design should be Metro-inspired, party because I like it, but partly because it's pretty easy to look ok
- Should support multiple input methods: mouse, keyboard and IR remote
- Django as backend
	

Architecture
============

I just spawn an external process with the Django development server. This has some cool advantages as I'll show later. 

I catch the stdout of the python process and when I see "Quit the server with CONTROL-C" I tell my WebKit view to load, and put the window into fullscreen.

Getting a WebKit view up and pointing it to a URL is very easy:

NSURLRequest* request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://127.0.0.1:8000/"]];
[[self.webView mainFrame] loadRequest:request];



Interaction
==========

IR Remote (Apple remote)

- I translate the left/right/etc keys to normal keyboard arrow events when in WebKit mode
- Menu-button -> Escape
- Play -> Enter

Keyboard

- Forwards to WebKit when in web view mode
- Library to navigate an HTML table. This part is pretty cool actually!

Mouse

- Don't need to do anything here really :P


Video Player Controls

- This is all done in Objective-C unfortunately with an ugly hack of a transparent window I put on top of the main window. 


Django -> Objective-C communication

- URL handler. KISS. Django code just executes "open CMiVideoplayer://<filename>?<params>"

Objective-C -> Django communication

- URL Access
	- e.g. Periodic callback from Obj-C to Django to save checkpoint where in the video we are
- Execute JavaScript functions inside the WebKit view directly
	- e.g. calls a refresh() function when the menu needs to be updated


How much code?
==============

* Objective-C: 1.6k
* Python: 1k
* JavaScript: 1k
* HTML: 300
* CSS: 300
* Total: ~3k


Database handling
=================

- SQLite
- Stores db in ~/Library/Application Support/CMi/cmi.db
- Ships with a pre-synced copy in the app that is automatically copied over on startup


Plugins
=======

- Scans ~/Library/Application Support/CMi/plugins on startup
- Add folders to INSTALLED_APPLICATIONS
- Modules are loaded like a normal django app from this point
- Syncdb is run
- Upgrades run. Introspects <plugin>.upgrade module for upgrade_<number>() functions
- django.config.settings.plugins == the list of plugins available
- Introspects <plugin>.api module for plugin functions:
	- tiles()
	- urls()
	- should_refresh()

Live development
================

PyCharm ssh deploy directly into remote .app bundle

Runserver in auto reload mode

settings.CODE_CHANGED = 1

AJAX poll:

    def changed_code(request):
        from django.conf import settings
        result = settings.CODE_CHANGED 
        settings.CODE_CHANGED = 0
        return HttpResponse(str(result))


Bits and Pieces
===============

OSX Location APIs enable location aware weather widget.

All animations are done with CSS transformations.

Retina display support with just a different CSS.

BeautifulSoup

theTVDB API

IMDB API
