"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    #~ map.connect('/{controller}/{id}/page/{page}', controller='feed', action='show_feed')
    map.connect('/', controller='medium', action='list_gallery')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/page/{page}')
    map.connect('/{controller}/{action}/type/{type}')
    map.connect('/{controller}/{action}/tagged/{tag}')
    map.connect('/{controller}/{action}/tagged/{tag}/page/{page}')
    map.connect('/{controller}/{action}/type/{type}/page/{page}')
    map.connect('/{controller}/{action}/type/{type}/tagged/{tag}')
    map.connect('/{controller}/{action}/type/{type}/tagged/{tag}/page/{page}')
    #~ map.connect('/{controller}/{action}/{type}')
    #~ map.connect('/{controller}/{action}/books', type='books')
    #~ map.connect('/{controller}/{action}/dvds', type='dvds')
    map.connect('/{controller}/{action}/{id}')
    map.connect('/{controller}/{action}/{id}/{width}/{height}')

    return map
