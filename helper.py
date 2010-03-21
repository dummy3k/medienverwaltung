import math

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

def cos(x):
    """Return the cosine of x (measured in degrees)."""
    return math.cos(x*math.pi/180)

def sin(x):
    """Return the sine of x (measured in degrees)."""
    return math.sin(x*math.pi/180)

def find(haystack, condition):
    for x in haystack:
        if condition(x):
            return x

    raise KeyError("condition did not match")

def reduce_array(input, condition):
    retval = []
    for x in input:
        if condition(x):
            retval.append(x)

    return retval

def step():
     import pdb
     return pdb.set_trace

def equal_float(a, b):
    return abs(a - b) < 1e-6

def between(value, between1, between2):
    if between1 > between2:
        small = between2
        big = between1
    else:
        small = between1
        big = between2

    return (value > small and value < big)
    #~ if value > between1
