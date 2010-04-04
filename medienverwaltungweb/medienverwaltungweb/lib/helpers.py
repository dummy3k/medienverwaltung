"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from pylons import config
from webhelpers.pylonslib import Flash as _Flash
from routes import url_for
from mako.filters import html_escape

flash = _Flash()

do_debug = True
def ipython():
    """ break and jump into ipython. call it this way:
            h.debug()('foo')
    """

    if not do_debug:
        def noop():
            pass
        return noop

    from IPython.Shell import IPShellEmbed
    # '-pdb',
    args = ['-pi1', 'In <\\#>: ', '-pi2', '   .\\D.: ',
            '-po', 'Out<\\#>: ', '-nosep']
    ipshell = IPShellEmbed(args,
        banner = 'Entering IPython.  Press Ctrl-D to exit. Set h.do_debug=False to never go here again.',
        exit_msg = 'Leaving Interpreter, back to Pylons.')
    return ipshell

def checkboxes(request, id):
    retval = []
    for item in request.params:
        if item.startswith(id):
            retval.append(request.params[item])

    return retval

def iif(expr, a, b):
    if expr:
        return a
    else:
        return b

def tmpl(template_name, def_name):
    return config['pylons.app_globals'].mako_lookup.get_template(template_name).get_def(def_name)
